
import sys
sys.path.insert(0, '../..')

from disks.prgdsk import prgdsk
import filesys


fs = filesys.FileSys()
fs.loadtracks(prgdsk.data)


if __name__ == '__main__':
    track = filesys.Track()
    track.info(0, fs.data[0], 32, 40)
    track.info(1, fs.data[1], 3, 255)
    track.info(2, fs.data[2], 22, 255)