"""Module to specify a list of loadable programs"""

# New abstraction to make it possible to load different roms and/or
# custom code snippets into memory with a user defined start address

import progs.jdc
import progs.misc
import progs.peeldk
import progs.lmc

proglist = {
        "peeldk"    : progs.peeldk.peeldk,
        "iws"       : progs.peeldk.iws,
        "jdc"       : progs.jdc.jdc,
        "lmc"       : progs.lmc.lmc
        # "psmcadd"   : progs.jdc.psmcadd,
        # "psmcmul"   : progs.jdc.psmcmul,
        # "psmcdiv"   : progs.jdc.psmcdiv,
        # "psmcb2ch"  : progs.jdc.psmcb2ch,
        # "psmcb2dec" : progs.jdc.psmcb2dec,
        # "SCR"       : progs.jdc.SCR,
        # "RTCTEST"   : progs.jdc.RTCTEST,
        # "dummy"     : progs.misc.dummy,
        # "loop"      : progs.misc.loop,
        # "todec"     : progs.misc.todec,
        # "emucrash"  : progs.misc.emucrash,
        # "test1"     : progs.misc.test1,
        # "loadhl"    : progs.misc.loadhl,
        # "scr"       : progs.misc.scr,
        # "ed_instrs" : progs.misc.ed_instrs
    }
