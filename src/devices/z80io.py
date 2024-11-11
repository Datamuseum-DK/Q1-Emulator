"""Module to provide IO hooks for the Q1 Lite"""

import sys
import devices.disk as disk
import devices.display as display

#

def isprintable(c):
    """True if character is printable ASCII"""
    return 0x20 <= c <= 0x7D


class IO:
    def __init__(self, m, fs):
        self.disk1 = disk.Control(1, fs)
        self.disk2 = disk.Control(2, fs)
        self.display = display.Display()
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

        self.register_in_cb( 0x05, self.handle_printer_in_5)
        self.register_out_cb(0x07, self.handle_printer_out_7)
        self.register_in_cb( 0x08, self.handle_printer_in_8)

        # Maybe these are really disk IO ?
        self.register_in_cb( 0x09, self.handle_disk_in_09)
        self.register_in_cb( 0x0a, self.handle_disk_in_0a)
        self.register_out_cb(0x09, self.handle_disk_out_09)
        self.register_out_cb(0x0a, self.handle_disk_out_0a)
        self.register_out_cb(0x0b, self.handle_disk_out_0b)

        # elusive IO
        # 2024 10 10 - could this be printer (see DINDEX F5)
        self.register_in_cb( 0x0c, self.handle_unkn_in_0c)
        self.register_out_cb(0x0c, self.handle_unkn_out_0c)

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
        #print(f'handle_io_out({outaddr:02x},{outval:02x}({chr(outval)}))')
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


    ### Printer 5,6,7 - Serial Impact Printer ?
    def handle_printer_in_5(self) -> int:
        self.print('IO in  - printer status -  0 (no errors)')
        return 0


    def handle_printer_out_7(self, val):
        if val == 0xA0:
            desc = 'reset printer, raise ribbon'
        else:
            desc = 'unknown command'
        self.print(f'IO out - printer control - {desc}')


    ### Printer 8 - Dot Matrix Printer ?
    def handle_printer_in_8(self) -> int:
        self.print('IO in  - printer 0x8 status -  0 (no errors)')
        return 0xF0 # error


    ### Disk 1? Data and Control
    ### From "Q1 ASM IO addresses usage Q1 Lite" p. 77 - 80
    def handle_disk_out_0a(self, val):
        if val != 0:
            self.print(f'IO out - disk1 (control 1 ) - (0x{val:02x})')
        self.disk1.control1(val)

    def handle_disk_out_0b(self, val):
        if val != 0:
            self.print(f'IO out - disk1 (control 2 ) - (0x{val:02x})')
        self.disk1.control2(val)


    def handle_disk_out_09(self, val):
        self.print(f'IO out - disk1 (data) - (0x{val:02x})')


    def handle_disk_in_0a(self):
        retval = self.disk1.status()
        t = self.disk1.disk.current_track
        b = self.disk1.disk.current_byte
        #self.print(f'IO in  - disk1 (0xa) (status): 0x{retval:02x}, t{t}, b{b}')
        return retval

    def handle_disk_in_09(self):
        t = self.disk1.disk.current_track
        b = self.disk1.disk.current_byte
        retval = self.disk1.data_in()
        #print(f'IO in  - disk1 (0x9) (data): 0x{retval:02x}, t{t}, b{b}')
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


    ### Disk 2 Data and Control
    ### From "Q1 Assembler" p. 52 - 54
    def handle_disk_in_19(self):
        retval =self.disk2.data_in()
        self.print(f'IO in  - disk2 (data): {retval}')
        return retval

    def handle_disk_in_1a(self):
        retval = self.disk2.status()
        self.print(f'IO in  - disk2 (status): {retval}')
        return retval


    def handle_disk_out_1a(self, val):
        if val != 0:
            self.print(f'IO out - disk2 (control 1 ) - (0x{val:02x})')
        self.disk2.control1(val)


    def handle_disk_out_1b(self, val):
        if val != 0:
            self.print(f'IO out - disk2 (control 2 ) - (0x{val:02x})')
        self.disk2.control2(val)
