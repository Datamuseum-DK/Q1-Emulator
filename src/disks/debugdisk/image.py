
import sys
sys.path.insert(0, '../..')

# tracks 5 - 9 still not ready
from disks.debugdisk import t0, t1, t2, t3, t4, t5, t6, t7, t8, t9
from disks.debugdisk import t10, t11, t12, t13, t14, t15, t16
import filesys


fs = filesys.FileSys()
fs.loadtracks([t0.data,  t1.data,  t2.data,  t3.data,  t4.data,
               t5.data,  t6.data,  t7.data,  t8.data,  t9.data,
               t10.data, t11.data, t12.data, t13.data, t14.data,
               t15.data, t16.data
              ])


if __name__ == '__main__':
    track = filesys.Track()
    track.info(0, fs.data[0], 130, 40)
    track.info(1, fs.data[1], 30, 255)
    track.info(2, fs.data[2], 30, 255)
    track.info(3, fs.data[3], 30, 255)
    track.info(4, fs.data[4], 30, 255)
    track.info(5, fs.data[5], 30, 255)
    track.info(6, fs.data[6], 30, 255)
    track.info(7, fs.data[7], 30, 255)
    track.info(8, fs.data[8], 30, 255)
    track.info(9, fs.data[9], 30, 255)
    track.info(10, fs.data[10], 30, 255)
    track.info(11, fs.data[11], 30, 255)
    track.info(12, fs.data[12], 30, 255)
    track.info(13, fs.data[13], 30, 255)

    # print(fs.data[0][:48])
    # print()
    # print(fs.data[0][48:96])
    # print()
    # print(fs.data[1][:263])
    # print(fs.data[1][263:293])
    #print(fs.marks[1])
    #print(fs.data)
