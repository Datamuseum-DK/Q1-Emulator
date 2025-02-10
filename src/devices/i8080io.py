"""Module to provide IO hooks for the Q1 LMC"""

import sys
import devices.disk as disk
import devices.display as display
import devices.printer as printer
import utils.udptx as udp

#

udptx = udp.UdpTx(port=5007, timestamp=True, nl=True)

def isprintable(c):
    """True if character is printable ASCII"""
    return 0x20 <= c <= 0x7D


class IO:
    def __init__(self, m, floppys, hds):
        self.floppy = disk.Control('floppy', floppys)
        #self.hdd = disk.Control('hdd', hds)
        self.display = display.Display()
        self.printer = printer.SerialImpactPrinter()

        self.prtbuf = "" # temporary hack for 'printer'

        self.m = m
        self.incb = {}
        self.outcb = {}
        self.keyin = 0
        self.go = 0
        self.stop = 0
        self.timeout = False
        self.in0count = 0
        self.timeron = False

        self.register_in_cb( 0x00, self.handle_rtc_in)
        # self.register_out_cb(0x00, self.handle_rtc_out)
        self.register_in_cb( 0x01, self.handle_key_in)
        self.register_out_cb(0x01, self.handle_key_out)
        self.register_out_cb(0x03, self.handle_display_out)
        self.register_out_cb(0x04, self.handle_display_out_ctrl)
        self.register_in_cb( 0x04, self.handle_display_in)

        # Serial impact printer
        self.register_in_cb( 0x05, self.handle_printer_in_5)
        # self.register_out_cb(0x05, self.handle_printer_out_5)
        # self.register_out_cb(0x06, self.handle_printer_out_6)
        self.register_out_cb(0x07, self.handle_printer_out_7)
        # Dot Matrix Printer
        # self.register_in_cb( 0x08, self.handle_printer_in_8)
        # Floppy disk - 8" ?
        # self.register_in_cb( 0x09, self.handle_disk_in_09)
        # self.register_out_cb(0x09, self.handle_disk_out_09)
        # self.register_in_cb( 0x0a, self.handle_disk_in_0a)
        # self.register_out_cb(0x0a, self.handle_disk_out_0a)
        # self.register_out_cb(0x0b, self.handle_disk_out_0b)
        # Unknown IO - could this be printer (see DINDEX F5)?
        # self.register_in_cb( 0x0c, self.handle_unkn_in_0c)
        # self.register_out_cb(0x0c, self.handle_unkn_out_0c)

        # First seen wirh IWS ROMs.
        # self.register_out_cb(0x10, self.handle_out_10)
        # self.register_in_cb( 0x11, self.handle_in_11)
        # self.register_out_cb(0x11, self.handle_out_11)

        # Floppy Disk - 8" ?
        # self.register_in_cb( 0x19, self.handle_disk_in_19)
        self.register_out_cb( 0x19, self.handle_disk_out_19)
        self.register_in_cb( 0x1a, self.handle_disk_in_1a)
        self.register_out_cb(0x1a, self.handle_disk_out_1a)
        self.register_out_cb(0x1b, self.handle_disk_out_1b)
        self.register_out_cb(0x1c, self.handle_disk_out_1c)


    ### Functions for registering and handling IO

    def register_out_cb(self, outaddr: int, outfunc):
        self.outcb[outaddr] = outfunc

    def register_in_cb(self, inaddr: int, infunc):
        self.incb[inaddr] = infunc

    def handle_io_in(self, value) -> int:
        #reg = value >> 8
        inaddr = value & 0xFF
        if inaddr in self.incb:
            return self.incb[inaddr]()

        msg = f'0x{inaddr:02x} - unregistered input address at pc {self.m.pc:04x}, exiting'
        udptx.send(msg)
        print(msg)
        print()
        sys.exit()


    def handle_io_out(self, outaddr, outval):
        outaddr = outaddr & 0xff
        if outaddr in self.outcb:
            self.outcb[outaddr](outval)
        else:
            msg = f'0x{outaddr:02x} - unregistered output address, value (0x{outval:02x})'
            udptx.send(msg)
            print(msg)
            sys.exit()


    ### IO Handling functions


    ### Real Time Clock (RTC)

    def handle_rtc_in(self) -> int:
        msg =''
        if self.in0count == 0:
            self.in0count = 1
        else:
            self.timeron = True

        retval = 0
        if self.timeout:
            self.timeout = False
            retval += 1
            msg += 'timeout'
        else:
            msg += 'no timeout'

        if not self.timeron:
            retval += 2
            msg += ', not running'
        else:
            msg += ', running'
        udptx.send(f"0x00 in  - timer {retval}: {msg}")
        return retval



    def handle_rtc_out(self, val):
        udptx.send(f"0x00 out - rtc: setting timeout value {val} not supported")


    ### Keyboard
    def handle_key_in(self) -> int:
        retval = self.keyin
        self.keyin = 0
        if self.go:
            retval = 0x0e
            self.go = 0
        if self.stop:
            retval = 0x0f
            self.stop = 0
        if retval:
            udptx.send(f'0x01 in  - key: 0x{retval:02x}')
        return retval


    def handle_key_out(self, val):
        modes ={0: 'mode 1 - lower case', 1: 'mode 2 - upper case',
                2: 'mode 3 - upper legends', 4: 'mode 4 - additional chars'}
        desc = ''
        if val & 0x01: # click
            print('\a')
            desc += 'click '
        if val & 0x02: # beep
            print('\a')
            desc += 'beep '
        mode = (val >> 2) & 0x3 + 1
        desc += f'mode {modes[mode]}'
        if val & 0x10:
            desc += 'K1 '
        if val & 0x20:
            desc += 'K2 '
        if val & 0x40:
            desc += 'K3 '
        if val & 0x80:
            desc += 'INS '
        udptx.send(f'0x01 out - {val} key: [{desc}]')


    ### Display

    def handle_display_out(self, val):
        if val > 127:
            print(f'0x03 out - extended ascii: {chr(val)}')
        # if val not in [0x00, 0x20]:
        #     udptx.send(f'0x03 out - display out: 0x{val:02x}, {chr(val)}')
        self.display.data(chr(val))
        self.display.update()


    def handle_display_in(self) -> int:
        udptx.send('0x04 in  - display status: 32 + 16 (Lite, 40 char)')
        return 0x00


    def handle_display_out_ctrl(self, val) -> str:
        self.display.control(val)
        if val == 0x05:
            desc = 'unblank, reset to (1,1)'
        elif val == 0x08:
            desc = 'advance right (or new line)'
        else:
            desc = f'0x{val:02}'
        udptx.send(f"0x05 out - display control - {desc}")


    ### Printer 5,6,7 - Serial Impact Printer

    # Get printer status
    # Bit 0 seems to need to be 1 for selected printer, even if manual does not
    # mention this. See
    # "Q1 ASM IO addresses usage Q1 Lite" p. 77
    def handle_printer_in_5(self) -> int:
        status = self.printer.status()
        udptx.send(f'0x05 in  - printer status -  {status} (1 == selected)')
        return status


    # Print character at current position
    def handle_printer_out_5(self, val : int):
        udptx.send(f'0x05 out - printer output - {val}')
        self.printer.output(val)


    def handle_printer_out_6(self, val):
        udptx.send(f'0x06 out - printer ctrl 1   - {val}')
        self.printer.ctrl_06(val)


    def handle_printer_out_7(self, val):
        udptx.send(f'0x07 out - printer ctrl 2   - {val}')
        self.printer.ctrl_07(val)


    ### Printer 8 - Dot Matrix Printer
    # Printer needs to be selected, see
    # From "Q1 ASM IO addresses usage Q1 Lite" p. 77
    def handle_printer_in_8(self) -> int:
        status = 0x01
        udptx.send(f'0x08 in  - printer status -  {status} (1 == selected)')
        return status


    ### Disk 1? Data and Control
    ### From "Q1 ASM IO addresses usage Q1 Lite" p. 77 - 80
    def handle_disk_in_09(self):
        retval = self.floppy.data_in()
        #udptx.send(f'0x09 in - floppy (data) - (0x{retval:02x})')
        return retval


    def handle_disk_out_09(self, val):
        #udptx.send(f'0x09 out - floppy (data) - (0x{val:02x})')
        self.floppy.data_out(val)


    def handle_disk_out_0a(self, val):
        if val:
            udptx.send(f'0x0a out - floppy (control 1 ) - (0x{val:02x})')
        self.floppy.control1(val)


    def handle_disk_in_0a(self):
        retval = self.floppy.status()
        #udptx.send(f'0x0a in  - floppy status - (0x{retval:02x})')
        return retval


    def handle_disk_out_0b(self, val):
        if val:
            udptx.send(f'0x0b out - floppy (control 2 ) - (0x{val:02x})')
        self.floppy.control2(val)



    # not disk, possibly printer
    def handle_unkn_in_0c(self):
        # status 0x80 - program stuck in start up
        # status 0x40 - DINDEX stuck in F5
        status = 0x00
        udptx.send(f'0x0c in  - unknown in for 0xc - (return {status})')
        return status


    def handle_unkn_out_0c(self, val):
        udptx.send(f'0x0c out - unknown device - (0x{val:02x})')
        if val == 0xa:
            print(self.prtbuf)
            self.prtbuf=""
        else:
            self.prtbuf += chr(val)


    # Used in both peeldk and iws imafe, but not jdc

    def handle_out_10(self, value):
        baud = {14:9600}
        res = {0:'Sel. ctrl reg 1',
               1:'reset interrupt line',
               2:'Sel. ctrl reg 2',
               4:'Sel. status reg.'}
        msg =''
        if value & 0x08 == 0: # bit 3 clear
            id = value & 0x7
            msg += f'REGSEL {res[id]}'

        else: # bit 3 set
            id = value >> 4
            msg += f'MODSEL {baud[id]} baud'

        udptx.send(f'0x10 out - value 0x{value:02x}: {msg}')

    def handle_in_11(self) -> int:
        status = 0x40 # data set ready? ASM IO addr p. 70
        status = 0x00
        udptx.send(f'0x11 in  - status {status}')
        return status

    def handle_out_11(self, value):
        udptx.send(f'0x11 out - value 0x{value:02x}')


    ### Disk 2 Data and Control
    ### From "Q1 Assembler" p. 52 - 54
    def handle_disk_in_19(self):
        # retval = self.hdd.data_in()
        # udptx.send(f'0x19 in  - hdd (data): {retval}')
        # return retval
        return 0

    def handle_disk_out_19(self, val):
        # if val:
        #     udptx.send(f'0x1a out - hdd (control 1 ) - (0x{val:02x})')
        # self.hdd.control1(val)
        pass


    def handle_disk_in_1a(self):
        # retval = self.hdd.status()
        # udptx.send(f'0x1a in  - hdd (status): {retval}')
        # return retval
        return 0x7f


    def handle_disk_out_1a(self, val):
        # if val:
        #     udptx.send(f'0x1a out - hdd (control 1 ) - (0x{val:02x})')
        # self.hdd.control1(val)
        pass


    def handle_disk_out_1b(self, val):
        # if val != 0:
        #     udptx.send(f'0x1b out - hdd (control 2 ) - (0x{val:02x})')
        # self.hdd.control2(val)
        pass

    def handle_disk_out_1c(self, val):
        # if val != 0:
        #     udptx.send(f'0x1b out - hdd (control 2 ) - (0x{val:02x})')
        # self.hdd.control2(val)
        pass
