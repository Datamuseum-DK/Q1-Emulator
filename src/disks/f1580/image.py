
import sys
sys.path.insert(0, '../..')

from disks.f1580 import f1580
import filesys


fs = filesys.FileSys()
fs.loadtracks(f1580.data)


if __name__ == '__main__':
    track = filesys.Track()
    track.info(0, fs.data[0], 32, 40)
