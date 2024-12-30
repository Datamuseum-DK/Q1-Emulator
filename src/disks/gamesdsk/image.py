
import sys
sys.path.insert(0, '../..')

from disks.gamesdsk import gamesdsk
import filesys


fs = filesys.FileSys()
fs.loadtracks(gamesdsk.data)


if __name__ == '__main__':
    track = filesys.Track()
    track.info(0, fs.data[0], 32, 40)
