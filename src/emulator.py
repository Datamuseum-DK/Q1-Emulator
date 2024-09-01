#!/usr/bin/env python3

import sys
import argparse
import cpu as c
import kbd
import match
import ros as r
import z80io
import programs as prg
import disks.debugdisk.image as ddim
import disks.datamuseum.image as dmim

'''
    Q1 Emulator
'''


def int38(cpu, io, ch):
    io.keyin = ch
    oldpc = cpu.m.pc
    cpu.m.sp -= 2
    cpu.mem.writeu16(cpu.m.sp, oldpc)
    cpu.m.pc = 0x38


def emulator(args):
    prgobj = prg.proglist[args.program]
    funcs = prgobj["funcs"]

    cpu = c.Cpu(prgobj)
    # todo select from multiple disk images
    #io = z80io.IO(cpu.m, ddim.ddfs)
    io = z80io.IO(cpu.m, dmim.dmfs)
    ros = r.ROS(cpu.mem)
    key = kbd.Key()
    kc = kbd.KeyboardCodes()
    #io.verbose = True
    cpu.reset()
    cpu.m.set_input_callback(io.handle_io_in)
    cpu.m.set_output_callback(io.handle_io_out)

    stoppc = 0x1ffff
    if "stop" in prgobj:
        stoppc = prgobj["stop"]

    icount = 0
    if args.hexdump:
        cpu.mem.hexdump(0x2000, 0xFFFF - 0x2000) # dump RAM part of memory

    while True:
        pc = cpu.m.pc
        icount += 1
        if icount >= args.stopafter or pc > 65530:
            print(f'exiting ... {icount}')
            for l in cpu.bt:
                print(l)
            sys.exit()

        if pc in funcs and args.decode:
            print(f'; {funcs[pc]}')

        if pc == args.poi and args.decode: # PC of interest
            print('\n<<<<< pc of interest >>>>>\n')

        # Decode the instruction.
        inst_str, _, bytes_str = cpu.getinst()
        inst_str2 = cpu.decodestr(inst_str, bytes_str)
        annot = match.operandaddr(inst_str, ros.addrs)
        if annot == "":
            if cpu.m.pc in prgobj["pois"]:
                annot = f'{prgobj["pois"][cpu.m.pc]}'
        if args.decode:
            print(inst_str2, annot)


        if icount % args.dumpfreq == 0 and args.hexdump:
            cpu.mem.hexdump(0x2000, 0x10000 - 0x2000) # dump RAM part of memory

        # main cpu emulation step
        cpu.step() # does the actual emulation of the next instruction


        if pc in (args.breakpoint, stoppc):
            print(f'\n<<<< BREAKPOINT at 0x{pc:04x} >>>>\n')
            #cpu.e(False, True, False)
            cpu.exit()

        if args.trigger == pc:
            print(f'\n<<<< TRIGGER at 0x{pc:04x} >>>>\n')
            args.decode = True
            io.verbose = True
            cpu.info()

        if pc ==0x4cb and args.program == 'jdc':
            print("<STOP>")

        if (icount % 1000) == 0: # int_disabled check?
            if key.kbhit():
                ch = ord(key.getch())
                if 32 <= ch < 127:
                    print(f'{chr(ch)}')
                else:
                    print(f'{ch}')

                if ch == 0x222b:       # opt-b -> hexdump
                    cpu.mem.hexdump(0x2000, 0x10000 - 0x2000)
                elif ch == 8224: # opt-t
                    args.decode = not args.decode
                elif ch == 170: # opt-a FDs
                    ros.index()
                    ros.file()
                    ros.disk()
                # Q1 Keyboard input below
                elif ch == kc.ikey("HEX"):
                    int38(cpu, io, kc.okey("HEX"))
                elif ch == kc.ikey("TAB"):
                    int38(cpu, io, kc.okey("TAB"))
                elif ch == kc.ikey("RETURN"):
                    int38(cpu, io, kc.okey("RETURN"))
                elif ch == kc.ikey("GO"):
                    io.go = 1
                elif ch == kc.ikey("STOP"):
                    io.stop = 1
                elif ch == kc.ikey("CORR"):
                    int38(cpu, io, kc.okey("CORR"))
                elif ch == kc.ikey("CLEAR ENTRY"):
                    int38(cpu, io, kc.okey("CLEAR ENTRY"))
                elif ch == kc.ikey("INSERT MODE"):
                    int38(cpu, io, kc.okey("INSERT MODE"))
                elif ch == kc.ikey("CHAR ADV"):
                    int38(cpu, io, kc.okey("CHAR ADV"))
                elif ch == kc.ikey("DEL CHAR"):
                    int38(cpu, io, kc.okey("DEL CHAR"))
                elif ch == kc.ikey("TAB SET"):
                    int38(cpu, io, kc.okey("TAB SET"))
                elif ch == kc.ikey("RESET"):
                    cpu.m.pc = 0
                else:
                    int38(cpu, io, ch)


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

    emulator(args)
