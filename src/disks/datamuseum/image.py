
import sys
sys.path.insert(0, '../..')

from disks.datamuseum import disk
import filesys


fs = filesys.FileSys()
fs.loadtracks(disk.data)


if __name__ == '__main__':
    track = filesys.Track()
    track.info(0, fs.data[0], 88, 40)
    track.info(8, fs.data[8], 19, 255)
    track.info(9, fs.data[9], 19, 255)
    track.info(70, fs.data[70], 126, 20)
    track.info(71, fs.data[71], 126, 20)
    track.info(73, fs.data[72], 126, 20)
