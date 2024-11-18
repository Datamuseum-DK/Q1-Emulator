
import sys
sys.path.insert(0, '../..')

from disks.fluxsamples import t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11
from disks.fluxsamples import t12, t13, t14, t15, t16, t17, t18
import filesys

tracks = [t0.data, t1.data, t2.data, t3.data, t4.data, t5.data, t6.data, t7.data,
          t8.data, t9.data, t10.data, t11.data, t12.data, t13.data, t14.data,
          t15.data, t16.data, t17.data, t18.data]

fs = filesys.FileSys()
fs.loadtracks(tracks) #


if __name__ == '__main__':
    track = filesys.Track()
    track.info( 0, fs.data[0],   16,  40)
    track.info( 1, fs.data[1],   82,  79)
    track.info( 2, fs.data[2],   82,  79)
    track.info( 3, fs.data[3],   82,  79)
    track.info( 4, fs.data[4],   82,  79)
    track.info( 5, fs.data[5],   82,  79)
    track.info( 6, fs.data[6],   82,  79)
    track.info( 7, fs.data[7],   82,  79)
    track.info( 8, fs.data[8],  122,  47)
    track.info( 9, fs.data[9],  122,  47)
    track.info(10, fs.data[10], 122,  47)
    track.info(11, fs.data[11],  67, 100)
    track.info(12, fs.data[12],  33,  50)
    track.info(13, fs.data[13],  67, 100)
    track.info(14, fs.data[14],  30, 255)
    track.info(15, fs.data[15],   1, 255)
    track.info(16, fs.data[16],  82,  79)
    track.info(17, fs.data[17],  82,  79)
    track.info(18, fs.data[18],  82,  79)
