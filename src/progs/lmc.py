
### From Mattis Lind who copied the ROMs from a Gen. 2 Q1 (LMC)

lmc = {
    "descr": "Combined Q1 LMC image from IC48-IC51",
    "start": 0x0000,
    "data": [
        ["file", "roms/LMC/Q1LMC_IC48.BIN", 0x0000],
        ["file", "roms/LMC/Q1LMC_IC49.BIN", 0x0400],
        ["file", "roms/LMC/Q1LMC_IC50.BIN", 0x0800],
        ["file", "roms/LMC/Q1LMC_IC50.BIN", 0x0C00]

    ],
    "funcs" : {

    },
    "pois" : {
        0x0065: 'TOSTR()',
        0x015b: 'TODEC()',
        0x01fb: '*** start() ***',
        0x01ff: 'get timer status',
        0x0203: 'if timer *is* running (bit 1 == 0) - jump to 0x4083',
        0x0206: 'else (bit 1 == 1) - initialise system',
        0x0228: 'Copy 512B from 0x800 to 0x6800',
        0x023b: 'START()',
        0x0242: 'Check if JP instruction at 0x815 (CLRDK)',
        0x0244: ' - if not jmp to 0x8000',
        0x0247: 'call CLRDK()',
        0x024f: 'print "     Q1/LMC AT YOUR SERVICE          "',
        0x0343: 'INTRET()',
        0x039b: 'KFILE()',
        0x03d2: 'NKEY()',
        0x03fe: 'reset 0x00',
        0x0415: 'DISPLAY()',
        0x0443: 'KEYIN()',
        0x04a5: 'PROCH()',
        0x05e4: 'UPDIS()',
        0x060e: 'MUL()',
        0x0620: 'DIV()',
        0x0650: 'NHL()',
        0x065c: 'BICHAR()',
        0x0687: 'GETDN()',
        0x0362: 'PRINTER()',
        0x06c1: 'CARB()',
        0x0601: 'STOP()',
        0x0715: 'INDEX()',
        0x074f: 'SHIFTY()'


    },
    "known_ranges" : [
        [0x0000, 0x003e, 'Interrupt vectors'],
        [0x003f, 0x0064, 'text: Q1-LMC at your service'],
        [0x0065, 0x01f1, 'unexplored'],
        [0x01f2, 0x01fa, 'if disk rom present call CLRDK()'],
        [0x01fb, 0x0209, 'start()'],
        [0x020a, 0x021a, 'copy jump vectors to 4080'],
        [0x021b, 0x0220, 'clear memory up to 40FF'],
        [0x0221, 0x0227, 'unexplored'],
        [0x0228, 0x0237, 'copy 2K from ROM 0x800 to RAM 0x6800'],
        [0x0238, 0x047d, 'unexplored'],
        [0x047e, 0x04a4, 'clear display???'],
        [0x04a5, 0x1000, 'unexplored']
    ]
}
