
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
        0x01fb: '*** start() ***',
        0x01ff: 'unknown input',
        0x0228: 'Copy 2k ROM from 0x800 to 0x6800'
    },
    "known_ranges" : [
        [0x0000, 0x003d, 'Interrupt vectors'],
        [0x003e, 0x0064, 'text: Q1-LMC at your service'],
        [0x0065, 0x1000, 'ROM']
    ]
}
