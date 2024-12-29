
import sys
sys.path.insert(0, '../..')

from disks.artificial import t0, t1, t2, t3, t4
import filesys

tracks = [t0.data, t1.data, t2.data, t3.data, t4.data]

fs = filesys.FileSys()
fs.loadtracks(tracks) #


if __name__ == '__main__':
    track = filesys.Track()
    track.info( 0, fs.data[0],   16,  40)
    track.info( 1, fs.data[1],   10,  79)
    track.info( 2, fs.data[2],   10,  79)
    track.info( 3, fs.data[3],   3,  79)
