"""Module to provide IO hooks for the Q1 Lite"""

import sys
import devices.disk as disk
import devices.display as display

#

def isprintable(c):
    """True if character is printable ASCII"""
    return 0x20 <= c <= 0x7D


class IO:
    def __init__(self, m, floppys, hds):
        self.floppy = disk.Control('floppy', floppys)
        self.hdd = disk.Control('hdd', hds)
        self.display = display.Display()

        self.prt2bits = 0
        self.prtdir = 0 # 0 = x, 1 = y
        self.prtbuf = "" # temporary hack for 'printer'

        self.m = m
        self.incb = {}
        self.outcb = {}
        self.keyincount = 0
        self.keyin = 0
        self.go = 0
        self.stop = 0
        self.timeout = False
        self.verbose = False
        self.register_in_cb( 0x00, self.handle_rtc_in)
        self.register_out_cb(0x00, self.handle_rtc_out)

        self.register_in_cb( 0x01, self.handle_key_in)
        self.register_out_cb(0x01, self.handle_key_out)

        self.register_out_cb(0x03, self.handle_display_out)
        self.register_out_cb(0x04, self.handle_display_out_ctrl)
        self.register_in_cb( 0x04, self.handle_display_in)

        # Serial impact printer
        self.register_in_cb( 0x05, self.handle_printer_in_5)
        self.register_out_cb( 0x05, self.handle_printer_out_5)
        self.register_out_cb(0x06, self.handle_printer_out_6)
        self.register_out_cb(0x07, self.handle_printer_out_7)

        #
        self.register_in_cb( 0x08, self.handle_printer_in_8)

        # Floppy disk ?
        self.register_in_cb( 0x09, self.handle_disk_in_09)
        self.register_in_cb( 0x0a, self.handle_disk_in_0a)
        self.register_out_cb(0x09, self.handle_disk_out_09)
        self.register_out_cb(0x0a, self.handle_disk_out_0a)
        self.register_out_cb(0x0b, self.handle_disk_out_0b)

        # elusive IO
        # 2024 10 10 - could this be printer (see DINDEX F5)?
        # speculation: serial?
        self.register_in_cb( 0x0c, self.handle_unkn_in_0c)
        self.register_out_cb(0x0c, self.handle_unkn_out_0c)

        # Hard disk ?
        self.register_in_cb( 0x19, self.handle_disk_in_19)
        self.register_in_cb( 0x1a, self.handle_disk_in_1a)
        self.register_out_cb(0x1a, self.handle_disk_out_1a)
        self.register_out_cb(0x1b, self.handle_disk_out_1b)


    def print(self, s):
        if self.verbose:
            print(s)

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

        print(f'IO - unregistered input address 0x{inaddr:02x} at pc {self.m.pc:04x}, exiting')
        print()
        sys.exit()
        return 0


    def handle_io_out(self, outaddr, outval):
        outaddr = outaddr & 0xff
        if outaddr in self.outcb:
            self.outcb[outaddr](outval)
        else:
            print(f'IO - unregistered output address 0x{outaddr:02x} (0x{outval:02x})')
            sys.exit()


    ### Specific functions

    ### Real Time Clock (RTC)
    def handle_rtc_in(self) -> int:
        if self.timeout:
            self.timeout = False
            return 1 # Bit 0 is timeout
        return 0

    def handle_rtc_out(self, val):
        print(f"setting timeout value {val} not supported")


    ### Display

    def handle_display_in(self) -> int:
        self.print('IO - display status: 32 + 16 (Lite, 40 char)')
        return 32 + 16


    def handle_display_out(self, val):
        self.display.data(chr(val))
        self.display.update()


    def handle_display_out_ctrl(self, val) -> str:
        self.display.control(val)
        if val == 0x05:
            desc = 'unblank, reset to (1,1)'
        elif val == 0x08:
            desc = 'advance right (or new line)'
        else:
            desc = f'0x{val:02}'
        self.print(f"IO out - display control - {desc}")


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
        self.print(f'IO in  - key : 0x{retval:02x}')
        return retval


    def handle_key_out(self, val):
        desc = ''
        if val & 0x01: # click
            print('\a')
            desc += 'click '
        if val & 0x02: # beep
            print('\a')
            desc += 'beep '
        mode = (val >> 2) & 0x3 + 1
        desc += f'mode {mode}'
        if val & 0x10:
            desc += 'K1 '
        if val & 0x20:
            desc += 'K2 '
        if val & 0x40:
            desc += 'K3 '
        if val & 0x80:
            desc += 'INS '
        print(f'IO out - key [{desc}]')


    ### Printer 5,6,7 - Serial Impact Printer

    # Get printer status
    # Bit 0 seems to need to be 1 for selected printer, even if manual does not
    # mention this. See
    # "Q1 ASM IO addresses usage Q1 Lite" p. 77
    def handle_printer_in_5(self) -> int:
        status = 0x01
        self.print(f'IO in  - printer 0x5 status -  {status} (1 == selected)')
        return status

    # Print character at current position
    def handle_printer_out_5(self, val : int):
        print(chr(val))

    # "Q1 ASM IO addresses usage Q1 Lite" p. 75
    def handle_printer_out_6(self, val):
        dist = (self.prt2bits << 8) + val
        dir = 'horizontally'
        if self.prtdir == 0: # x-dir
            inch = dist / 60 # inches
        else:
            dir = 'vertically'
            inch = dist / 48
        self.print(f'IO out - printer ctrl 0x6 move {dir} {inch:.2f} inches.')


    def handle_printer_out_7(self, val):
        self.prt2bits = val & 0x3
        desc = ''
        if val & 0x80:
            desc += 'reset, '
        if val & 0x40:
            desc += 'exp res, '
        if val & 0x20:
            desc += 'raise ribbon, '
        if val & 0x10:
            desc += 'lower ribbon, '
        if val & 0x08:
            desc += 'paper '
            self.prtdir = 1 # y-dir
        else:
            desc += 'carriage '
            self.prtdir = 0 # x-dir
        if val & 0x04:
            desc += 'reverse '
        else:
            desc += 'forward '
        desc += 'motion'

        self.print(f'IO out - printer ctrl 0x7 - 0x{val:02x} [{desc}]')


    ### Printer 8 - Dot Matrix Printer
    # Printer needs to be selected, see
    # From "Q1 ASM IO addresses usage Q1 Lite" p. 77
    def handle_printer_in_8(self) -> int:
        status = 0x01
        self.print(f'IO in  - printer 0x8 status -  {status} (1 == selected)')
        return status


    ### Disk 1? Data and Control
    ### From "Q1 ASM IO addresses usage Q1 Lite" p. 77 - 80
    def handle_disk_out_0a(self, val):
        if val:
            self.print(f'IO out - floppy (control 1 ) - (0x{val:02x})')
        self.floppy.control1(val)


    def handle_disk_out_0b(self, val):
        if val:
            self.print(f'IO out - floppy (control 2 ) - (0x{val:02x})')
        self.floppy.control2(val)


    def handle_disk_out_09(self, val):
        self.print(f'IO out - floppy (data) - (0x{val:02x})')


    def handle_disk_in_0a(self):
        retval = self.floppy.status()
        return retval

    def handle_disk_in_09(self):
        retval = self.floppy.data_in()
        return retval


    # not disk, possibly printer
    def handle_unkn_in_0c(self):
        self.print('IO in  - unknown in for 0xc - (return 0x00)')
        return 0x00


    def handle_unkn_out_0c(self, val):
        if val == 0xa:
            print(self.prtbuf)
            self.prtbuf=""
        else:
            self.prtbuf += chr(val)

        #print(f'{chr(val)}')


    def handle_disk_out_0c(self, val):
        print(f'IO out - unknown device - (0x{val:02x})')


    ### Disk 2 Data and Control
    ### From "Q1 Assembler" p. 52 - 54
    def handle_disk_in_19(self):
        retval = self.hdd.data_in()
        self.print(f'IO in  - hdd (data): {retval}')
        return retval

    def handle_disk_in_1a(self):
        retval = self.hdd.status()
        self.print(f'IO in  - hdd (status): {retval}')
        return retval


    def handle_disk_out_1a(self, val):
        if val:
            self.print(f'IO out - hdd (control 1 ) - (0x{val:02x})')
        self.hdd.control1(val)


    def handle_disk_out_1b(self, val):
        if val != 0:
            self.print(f'IO out - hdd (control 2 ) - (0x{val:02x})')
        self.hdd.control2(val)
