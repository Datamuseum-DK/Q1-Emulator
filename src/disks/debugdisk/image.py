
import sys
sys.path.insert(0, '../..')

from disks.debugdisk import t0, t1, t2, t3, t4
import filesys


ddfs = filesys.FileSys()
ddfs.loadtracks2([t0.data, t1.data, t2.data, t3.data, t4.data])


if __name__ == '__main__':
    track = filesys.Track()
    track.info(0, ddfs.data[0], 130, 40)
    track.info(1, ddfs.data[1], 30, 255)
    track.info(2, ddfs.data[2], 30, 255)
    track.info(3, ddfs.data[3], 30, 255)
    track.info(4, ddfs.data[4], 30, 255)

    # print(ddfs.data[0][:48])
    # print()
    # print(ddfs.data[0][48:96])
    # print()
    # print(ddfs.data[1][:263])
    # print(ddfs.data[1][263:293])
    #print(ddfs.marks[1])
    #print(ddfs.data)
