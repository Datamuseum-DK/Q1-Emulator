#!/usr/bin/env python3

import sys
import argparse
import devices.cpu as c
import devices.kbd as kbd
import match
import ros as r
import devices.z80io as z80io
import devices.i8080io as i8080io
import progs.programs as prg
import utils.misc as misc
import utils.udptx as udp
import disks.debugdisk.image as debugdisk
import disks.datamuseum.image as datamuseum
import disks.fluxsamples.image as fluxsamples
import disks.artificial.image as artificial
from timeit import default_timer as timer
#from multiprocessing import shared_memory

'''
    Q1 Emulator
'''

udptx = udp.UdpTx(port=5009, timestamp=True, nl=True)

class Emulator:

    def on_write(self, address, value):
        assert value < 256
        assert address < 65536
        if address < 0x4000: # 0x2000 - 0x3fff is unused
            #print(f"write to ROM (0x{address:04x}) error, exiting ...")
            print(f"write to ROM (0x{address:04x}), pc {self.cpu.m.pc} warning, no effect ...")
            #self.cpu.exit()

        self.cpu.m.memory[address] = value
        #self.shm.buf[address] = value


    def __del__(self):
        #self.shm.close()
        #self.shm.unlink()
        pass


    def __init__(self, args):
        self.args = args
        self.prgobj = prg.proglist[args.program]
        self.funcs = self.prgobj["funcs"]

        self.cpu = c.Cpu(self.prgobj)
        self.defaultsteps = 103 # set to 1 for disassembly debug
        self.steps = self.defaultsteps

        #floppydisks = [datamuseum.fs, , fluxsamples.fs]
        floppydisks = [datamuseum.fs, debugdisk.fs, fluxsamples.fs, artificial.fs]
        harddisks = [datamuseum.fs, debugdisk.fs]
        if args.program == 'lmc':
            self.io = i8080io.IO(self.cpu.m, floppydisks, harddisks)
        else:
            self.io = z80io.IO(self.cpu.m, floppydisks, harddisks)

        self.ros = r.ROS(self.cpu.mem)
        self.key = kbd.Key()
        self.kc = kbd.KeyboardCodes()

        self.cpu.reset()
        self.cpu.m.set_write_callback(self.on_write)
        self.cpu.m.set_input_callback(self.io.handle_io_in)
        self.cpu.m.set_output_callback(self.io.handle_io_out)

        # self.shm = shared_memory.SharedMemory(
        #     name="shm_q1",
        #     create=True,
        #     size=65535)
        # print(self.shm.name)

        self.stoppc = 0x1ffff
        if "stop" in self.prgobj:
            self.stoppc = self.prgobj["stop"]

        self.icount = 0
        if self.args.hexdump:
            self.cpu.mem.hexdump(0x2000, 0xFFFF - 0x2000) # dump RAM part of memory


    def kbd_input(self):
        kc = self.kc
        if self.key.kbhit():
            ch = ord(self.key.getch())
            if misc.isprintable(ch):
                print(f'{chr(ch)}')
            else:
                print(f'{ch}')

            if ch == 0x222b:       # opt-b -> hexdump
                self.cpu.mem.hexdump(0x2000, 0x10000 - 0x2000)
            elif ch == 402: # opt-f function keys
                k = 'F' + input("fn key:\n")
                #print('key:', k)
                self.int38(kc.okey(k))
            elif ch == 8224: # opt-t
                args.decode = not args.decode
                if args.decode:
                    self.steps = 1
                else:
                    self.steps = self.defaultsteps

            elif ch == 170: # opt-a misc debug FDs, floppy dump
                drive = input("enter drive (1-7):\n")
                track = input("enter track:\n")
                self.io.floppy.disk.drives[int(drive)-1].dump(int(track))
                # self.ros.index()
                # self.ros.file()
                # self.ros.disk()
            # Q1 Keyboard input below
            elif ch == kc.ikey("HEX"):
                self.int38(kc.okey("HEX"))
            elif ch == kc.ikey("TAB"):
                self.int38(kc.okey("TAB"))
            elif ch == kc.ikey("RETURN"):
                self.int38(kc.okey("RETURN"))
            elif ch == kc.ikey("GO"):
                self.io.go = 1
            elif ch == kc.ikey("STOP"):
                self.io.stop = 1
            elif ch == kc.ikey("CORR"):
                self.int38(kc.okey("CORR"))
            elif ch == kc.ikey("CLEAR ENTRY"):
                self.int38(kc.okey("CLEAR ENTRY"))
            elif ch == kc.ikey("INSERT MODE"):
                self.int38(kc.okey("INSERT MODE"))
            elif ch == kc.ikey("CHAR ADV"):
                self.int38(kc.okey("CHAR ADV"))
            elif ch == kc.ikey("DEL CHAR"):
                self.int38(kc.okey("DEL CHAR"))
            elif ch == kc.ikey("TAB SET"):
                self.int38(kc.okey("TAB SET"))
            elif ch == kc.ikey("RESET"):
                self.cpu.m.pc = 0
            else:
                self.int38(ch)


    # Only works for the JDC image
    def pl1_debug(self):
        pc = self.cpu.m.pc
        m = self.cpu.m
        if pc in self.prgobj["pl1"]:
            inst = self.prgobj["pl1"][pc]
            regs = f'a: {m.a:02x}, bc: {m.bc:04x}, de: {m.de:04x}, hl: {m.hl:04x}'
            udptx.send(f'{inst:40} ; {regs}')


    # Fake a keyboard interrupt, seems to work, but the Q1 interrupt model
    # is currently not well understood
    def int38(self, ch):
        self.io.keyin = ch
        oldpc = self.cpu.m.pc
        self.cpu.m.sp -= 2
        self.cpu.mem.writeu16(self.cpu.m.sp, oldpc)
        self.cpu.m.pc = 0x38


    # Main emulator loop
    def run(self):
        args = self.args
        io = self.io
        cpu = self.cpu
        kc = self.kc
        n = self.steps

        tstart = timer()
        while True:
            # First take care of timer 'interrupt'
            tend = timer()
            if (tend - tstart) > 1.0:
                tstart = timer()
                io.timeout = True

            # Prepare for next instruction(s)
            pc = cpu.m.pc
            self.icount += 1

            # Check for halt condition (number of instructions or invalid
            # address )
            if self.icount >= args.stopafter or pc > 65530:
                print(f'exiting ... {self.icount}')
                for l in cpu.bt:
                    print(l)
                sys.exit()

            # Print info about known functions
            if pc in self.funcs and args.decode:
                print(f'; {self.funcs[pc]}')


            if pc == args.poi and args.decode: # PC of interest
                print('\n<<<<< pc of interest >>>>>\n')

            # Decode the instruction.
            inst_str, _, bytes_str = cpu.getinst()
            inst_str2 = cpu.decodestr(inst_str, bytes_str)
            annot = match.operandaddr(inst_str, self.ros.addrs)
            if annot == "":
                if cpu.m.pc in self.prgobj["pois"]:
                    annot = f'{self.prgobj["pois"][cpu.m.pc]}'
            if args.decode:
                print(inst_str2, annot)


            if self.icount % args.dumpfreq == 0 and args.hexdump:
                cpu.mem.hexdump(0x2000, 0x10000 - 0x2000) # dump RAM part of memory

            # Debugging PL/1 programs (experimental)
            # if cpu.m.pc > 0x1880:
            #     self.pl1_debug()

            # main cpu emulation step
            cpu.step(self.steps) # actual emulation of the next n instruction(s)

            # Handle breakpoints
            if pc in (args.breakpoint, self.stoppc):
                print(f'\n<<<< BREAKPOINT at 0x{pc:04x} >>>>\n')
                #cpu.e(False, True, False)
                cpu.exit()

            # Handle trigger conditions
            if args.trigger == pc:
                print(f'\n<<<< TRIGGER at 0x{pc:04x} >>>>\n')
                args.decode = True
                io.verbose = True
                cpu.info()

            # Handle (JDC) program halt
            if pc ==0x4cb and args.program == 'jdc':
                print("<STOP>")

            # Handle occasional keyboard input
            if (self.icount % 1000) == 0: # int_disabled check?
                self.kbd_input()



if __name__ == "__main__":

    def auto_int(x):
        return int(x, 0)

    parser = argparse.ArgumentParser()

    parser.add_argument("-b", "--breakpoint", help = "stop on BP, hexdump and backtrace",
        type = auto_int, default = 0x1FFFF)
    parser.add_argument("-t", "--trigger", help = "start decode at trigger address",
        type = auto_int, default = 0x1FFFF)
    parser.add_argument("-s", "--stopafter", help = "stop after N instructions",
        type = int, default = -1)
    parser.add_argument("-p", "--poi", help = "Point of interest (PC)",
                        type = auto_int, default = 0x1ffff)
    parser.add_argument("--dumpfreq", help = "Hexdump every N instruction",
                        type = int, default = 256)
    parser.add_argument("-x", "--hexdump", help = "Toggle hexdump", action='store_true')
    parser.add_argument("-d", "--decode", help = "Decode instructions", action='store_true')
    parser.add_argument("-l", "--list", help = "show available programs",
        action='store_true')
    parser.add_argument("--program", help = "name of program to load, see programs.py",
                        type = str, default = "jdc")


    args = parser.parse_args()
    if args.stopafter == -1:
        args.stopafter = 1000000000

    if args.list:
        for p in prg.proglist:
            print(p)
        sys.exit()

    emulator = Emulator(args)
    emulator.run()
