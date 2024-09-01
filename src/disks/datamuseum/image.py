
import sys
sys.path.insert(0, '../..')

from disks.datamuseum import disk
import filesys


dmfs = filesys.FileSys()
dmfs.loadtracks2(disk.data)


if __name__ == '__main__':
    track = filesys.Track()
    track.info(0, dmfs.data[0], 88, 40)
    track.info(8, dmfs.data[8], 19, 255)
    track.info(9, dmfs.data[9], 19, 255)
    track.info(70, dmfs.data[70], 126, 20)
