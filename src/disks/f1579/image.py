
import sys
sys.path.insert(0, '../..')

from disks.f1579 import f1579
import filesys


fs = filesys.FileSys()
fs.loadtracks(f1579.data)


if __name__ == '__main__':
    track = filesys.Track()
    track.info(0, fs.data[0], 32, 40)
