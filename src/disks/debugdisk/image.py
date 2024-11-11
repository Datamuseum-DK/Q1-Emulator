
import sys
sys.path.insert(0, '../..')

# tracks 5 - 9 still not ready
from disks.debugdisk import t0, t1, t2, t3, t4 #, t5, t6, t7, t8, t9
import filesys


ddfs = filesys.FileSys()
ddfs.loadtracks([t0.data, t1.data, t2.data, t3.data, t4.data #,
                 # t5.data, t6.data, t7.data, t8.data, t9.data
                 ])


if __name__ == '__main__':
    track = filesys.Track()
    track.info(0, ddfs.data[0], 130, 40)
    track.info(1, ddfs.data[1], 30, 255)
    track.info(2, ddfs.data[2], 30, 255)
    track.info(3, ddfs.data[3], 30, 255)
    track.info(4, ddfs.data[4], 30, 255)
    # track.info(5, ddfs.data[5], 30, 255)
    # track.info(6, ddfs.data[6], 30, 255)
    # track.info(7, ddfs.data[7], 30, 255)
    # track.info(8, ddfs.data[8], 30, 255)
    # track.info(9, ddfs.data[9], 30, 255)

    # print(ddfs.data[0][:48])
    # print()
    # print(ddfs.data[0][48:96])
    # print()
    # print(ddfs.data[1][:263])
    # print(ddfs.data[1][263:293])
    #print(ddfs.marks[1])
    #print(ddfs.data)
