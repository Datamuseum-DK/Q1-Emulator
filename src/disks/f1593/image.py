
import sys
sys.path.insert(0, '../..')

from disks.f1593 import f1593
import filesys


fs = filesys.FileSys()
fs.loadtracks(f1593.data)


if __name__ == '__main__':
    track = filesys.Track()
    track.info(0, fs.data[0], 32, 40)
