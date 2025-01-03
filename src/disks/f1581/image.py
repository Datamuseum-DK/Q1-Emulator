
import sys
sys.path.insert(0, '../..')

from disks.f1581 import f1581
import filesys


fs = filesys.FileSys()
fs.loadtracks(f1581.data)


if __name__ == '__main__':
    track = filesys.Track()
    track.info(0, fs.data[0], 32, 40)
