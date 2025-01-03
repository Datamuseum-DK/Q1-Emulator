
import disks.artificial.image as mjc
import disks.datamuseum.image as floppy1
import disks.f1576.image as f1576
import disks.f1578.image as f1578
import disks.f1579.image as f1579
import disks.f1580.image as f1580
import disks.f1581.image as f1581
import disks.f1582.image as f1582
import disks.f1593.image as f1593
import disks.f1610.image as f1610
import disks.f1615.image as f1615
import disks.prgdsk.image as prgdsk
import disks.gamesdsk.image as gamesdsk


disks = {
    'floppy1'  : floppy1,  #
    'f1576'    : f1576,    #
    'f1578'    : f1578,    #
    'f1579'    : f1579,    #
    'f1580'    : f1580,    #
    'f1581'    : f1581,    #
    'f1582'    : f1582,    #
    'f1593'    : f1593,    #
    'f1610'    : f1610,    # games disk
    'f1615'    : f1615,    # felsokningsdiskett
    'prgdsk'   : prgdsk,   # programmer's disk (mattis)
    'gamesdsk' : gamesdsk, # other games disk (mattis)
    'mjc'      : mjc       # artificial disk (morten)
}
