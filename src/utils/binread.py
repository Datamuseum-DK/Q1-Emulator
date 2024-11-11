''' Create a disk image python structure from .BIN files '''

import argparse

def makeparms(geometry):
    ''' make a list of track parameters from geometry string '''
    res = []
    for t in geometry.split(','):
        t2 = t.split()
        assert len(t2) == 4, 'geometry format error'
        res.append([int(x[:-1]) for x in t2])
    return res


def record(data, offset, len):
    ''' print records for each track '''
    res = []
    for i in range(len):
        res.append(f'0x{data[offset + i]:02x}')
    return ', '.join(res)


def loadfile(file: str):
    # Helper code to load a file into a specidied address
    with open(file, 'rb') as fh:
        block = list(fh.read())
        print(f'# loaded {len(block)} bytes from {file}')
        return block




def diskdump(file, geometry):
    data = loadfile(file)
    diskgeom = makeparms(geometry)
    print('#', diskgeom)
    print('data = [')
    offset = 0
    track = 0
    for cyl, hds, recs, bytes in diskgeom:
        assert hds == 1, 'only one head is supported'
        for t in range(cyl):
            print(f'# track {track}')
            print(f'[')
            for rec in range(recs):
                sep = ''
                if rec != 0:
                    sep =','
                print(f'{sep}\n  [0x9e, 0x{track:02x}, 0x{rec:02x}],')
                print(f'  [0x9b, {record(data,  offset, bytes)}]')
                offset += bytes
            track += 1
            print('],')
    print(']')



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-f", "--file", help = ".BIN file",
        type = str, default='disks/datamuseum/Q1_FLOPPY.BIN')
    parser.add_argument("-g", "--geometry", help = "disk geometry description",
        type = str, default='1c 1h 88s 40b, 29c 1h 19s 255b, 43c 1h 126s 20b, 1c 1h 19s 255b')

    args = parser.parse_args()

    diskdump(args.file, args.geometry)
