
import sys
sys.path.insert(0, '../..')

from disks.fluxsamples import t0, t1, t2
import filesys


fs = filesys.FileSys()
fs.loadtracks([t0.data, t1.data, t2.data]) #


if __name__ == '__main__':
    track = filesys.Track()
    track.info(1, fs.data[1], 82, 79)
    track.info(2, fs.data[2], 82, 79)
