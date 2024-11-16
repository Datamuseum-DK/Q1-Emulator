
import sys
sys.path.insert(0, '../..')

from disks.fluxsamples import t0, t1, t2, t3, t4, t5, t6, t7
import filesys

tracks = [t0.data, t1.data, t2.data, t3.data, t4.data, t5.data, t6.data, t7.data]

fs = filesys.FileSys()
fs.loadtracks(tracks) #


if __name__ == '__main__':
    track = filesys.Track()
    track.info(0, fs.data[0], 16, 40)
    track.info(1, fs.data[1], 77, 79)
    track.info(2, fs.data[2], 82, 79)
    track.info(3, fs.data[3], 82, 79)
    track.info(4, fs.data[4], 82, 79)
    track.info(5, fs.data[5], 82, 79)
    track.info(6, fs.data[6], 82, 79)
    track.info(7, fs.data[7], 82, 79)
