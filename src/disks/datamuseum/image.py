
import sys
sys.path.insert(0, '../..')

from disks.datamuseum import disk
import filesys


fs = filesys.FileSys()
fs.loadtracks(disk.data)


if __name__ == '__main__':
    track = filesys.Track()
    track.info(0, fs.data[0], 88, 40)
    track.info(6, fs.data[6], 19, 255)
    track.info(7, fs.data[7], 19, 255)
    track.info(8, fs.data[8], 19, 255)
    track.info(9, fs.data[9], 19, 255)
    track.info(30, fs.data[30], 126, 20)
    track.info(31, fs.data[31], 126, 20)
    track.info(32, fs.data[32], 126, 20)
    track.info(33, fs.data[33], 126, 20)
    track.info(72, fs.data[72], 126, 20)
    track.info(73, fs.data[73], 19, 255)
