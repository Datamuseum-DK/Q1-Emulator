

class Track:
    def __init__(self):
        # overhead consists of
        #   0x9e, trk, rec, csum, 0x10, 0x00, 0x00
        self.overhead_0x9e = 7
        #   0x9b,           csum, 0x10, 0x00, 0x00
        self.overhead_0x9b = 5

        self.overhead = self.overhead_0x9e + self.overhead_0x9b


    # Handle INDEX track which has fixed size
    def index(self, data, records, record_size):
        assert record_size == 40
        d = data
        for record in range(records):
            i = 0
            offset = record * (record_size + self.overhead)
            assert d[offset + i] == 0x9e, f'{i=}, {d[offset + i]=}'
            assert d[offset + i + 1] == 0x00
            assert d[offset + i + 2] == record
            i += self.overhead_0x9e
            assert d[offset + i] == 0x9b
            i += 1

            recno = d[offset + i] + (d[offset + i + 1] << 8)
            filename = ''.join([chr(x) for x in d[offset + i + 2: offset + i + 10]])
            nrecs =  d[offset + i + 10] + (d[offset + i + 11] << 8)
            recsz =  d[offset + i + 12] + (d[offset + i + 13] << 8)
            rpt = d[offset + i + 14]
            disk = d[offset + i + 15]
            ftrack = d[offset + i + 16] + (d[offset + i + 17] << 8)
            ltrack = d[offset + i + 18] + (d[offset + i + 19] << 8)
            #assert recno == 0
            if nrecs:
                print(f'{filename}: recno {recno}, nrecs {nrecs:2}, record size {recsz:3}, recs/trk: {rpt:3}, disk {disk}, first track {ftrack:2}, last track {ltrack:2}')

    # Handle case where segments are loaded according to ROS manual
    # separator, address, number of bytes, ....
    def loadable(self, track, data, records, record_size):
        assert record_size == 255
        d = data
        for record in range(records):
            print(f'record {record}')
            firstline = False
            i = 0
            offset = record * (record_size + self.overhead)
            assert d[offset + i] == 0x9e, f'{i=}, {d[offset + i]=}'
            assert d[offset + i + 1] == track
            assert d[offset + i + 2] == record
            i += self.overhead_0x9e
            assert d[offset + i] == 0x9b
            i += 1
            while 255 - i  >= 5:
                block_separator = d[offset + i]
                if block_separator == 0:
                    break
                if not firstline:
                    firstline = True
                    print(f'\nTrack {track}, Record {record}')

                i += 1
                addr = d[offset + i] + (d[offset + i + 1] << 8)
                i += 2
                bytecount = d[offset + i]
                i += 1
                print(f'separator 0x{block_separator:02x}: load {bytecount:3} bytes into address 0x{addr:04x}')
                brk = 0
                s0 = f'{addr:04x}'
                s1 = ''
                s2 = ''
                for _ in range(bytecount):
                    val = d[offset + i]
                    i += 1
                    s1 += f'{val:02x} '
                    if 32 <= val <= 127:
                        s2 += chr(val)
                    else:
                        s2 += '.'
                    brk += 1
                    if brk == 16:
                        brk = 0
                        s0 = f'{addr:04x}'
                        print(s0, s1, s2)
                        addr += 16
                        s1 = ''
                        s2 = ''
                s0 = f'{addr:04x}'
                print(f'{s0} {s1:48} {s2}')
                print()


    def program(self, track, data, records, record_size):
        d = data
        for record in range(records):
            i = 0
            offset = record * (record_size + self.overhead)
            assert d[offset + i] == 0x9e, f'{i=}, {d[offset + i]=}'
            assert d[offset + i + 1] == track, f'expected track {track}'
            assert d[offset + i + 2] == record, f'expected rec {record}'
            i += self.overhead_0x9e
            assert d[offset + i] == 0x9b
            i += 1

            ch = d[offset + i: offset + i + record_size]
            print(''.join(list(map(chr, ch))))


    def rawdata(self, track, data, records, record_size):
        d = data
        for record in range(records):
            i = 0
            offset = record * (record_size + self.overhead)
            assert d[offset + i] == 0x9e, f'{i=}, {d[offset + i]=}'
            i += self.overhead_0x9e
            assert d[offset + i] == 0x9b
            i += 1

            ch = d[offset + i: offset + i + record_size]
            #print(''.join(list(map(chr, ch))))
            cha = [ chr(x) if 32 <= x < 127 else '.' for x in ch]
            print(f'{record:03}', ''.join(cha))

            # this output can be filtered for more condensed output:
            # python3 image.py | grep -v '\.\.\.\.\.\.\.' | grep -v '       '

    # INDEX track handled separately
    # Currently only works for loadable tracks (record size 255)
    def info(self, track, data, records, record_size):
        print(f'\nTrack information for track {track}\n')
        if track == 0:
            self.index(data, records, record_size)
            return

        if record_size == 255:
            self.loadable(track, data, records, record_size)
            return

        if record_size == 79:
            self.program(track, data, records, record_size)
            return

        # all other record types are presumed custom
        self.rawdata(track, data, records, record_size)



class FileSys:

    # Possibilities according to "Q1 Lite system overview"
    # Tracks  Bytes per track
    #   35    4608
    #   77    8316
    def __init__(self, tracks=77, bytes_per_track=8316):
        self.tracks = tracks
        self.bpt = bytes_per_track
        self.data = [[0x00 for B in range(self.bpt)] for A in range(self.tracks)]
        self.marks = [set() for A in range(self.tracks)]


    def rawrecord(self, track, offset, data):
        # if track == 0 and data[0] == 0x9b and data[3] >= 0x30:
        #     fn = ""
        #     for i in range(8):
        #         fn += chr(data[3+i])
            #print(f'INDEX Record:  {fn}')

        d = self.data[track]
        cksum = sum(data[1:]) & 0xff
        if data[0] == 0x9b:
            cksum = (cksum + 0x9b) & 0xff
        for i, e in enumerate(data):
            d[offset + i] = e
        i = len(data)
        d[offset + i + 0] = cksum
        d[offset + i + 1] = 0x10
        d[offset + i + 2] = 0x00 # needed by write
        d[offset + i + 3] = 0x00 # needed by write
        return offset + i + 4


    #
    def loadtracks(self, track_list): # assume contiguous, starting with t0
        for track, trackdata in enumerate(track_list):
            offset = 0
            for lst in trackdata:
                self.marks[track].add(offset)
                offset = self.rawrecord(track, offset, lst)
