import sys
import utils.misc as misc
import utils.udptx as udp

# System can have multple Disks (Floppy, Harddisks)
# Disks can have multiple Drives (0, 1, ...)

udptx = udp.UdpTx(port=5006, timestamp=True, nl=True)

class Disk:
    def __init__(self, type, drives):
        udptx.send(f'disk {type} has {len(drives)} drives')
        self.type = type
        self.selected_drive = -1
        self.numdrives = len(drives)
        self.drives = []
        for i, fs in enumerate(drives):
            udptx.send(f'append {self.type} Drive({i})')
            self.drives.append(Drive(i, fs))
        for i in range(self.numdrives, 8):
            udptx.send(f'append (unavailable) {self.type} Drive({i})')
            self.drives.append(Drive(i, drives[0], avail=False))


    def getdrive(self):
        return self.selected_drive


    def select_drive(self, i):
        drive = i & 0x7f
        if drive == 0:
            self.deselect_drive()
            return

        self.selected_drive = drive # allow selection of unavailable drives
        self.drive = self.drives[drive - 1]
        udptx.send(f'Disk.select_drive() - {self.type}/{drive}, active: {self.drive.avail}')

        assert self.selected_drive in [1, 2, 3, 4, 5, 6, 7]


    # bad name, also used in Drive
    def readbyte(self):
        return self.drive.readbyte()

    # bad name, also used in Drive
    def writebyte(self, byte):
        self.drive.writebyte(byte)


    def step(self, stepdir):
        self.drive.step(stepdir)


    def gettrackno(self):
        return self.drive.gettrackno()


    def istrack0(self):
        return self.drive.istrack0()


    def isindex(self):
        return self.drive.isindex()


    def isbusy(self):
        return self.drive.isbusy()


    def status(self) -> int:
        if self.type != 'floppy':
            udptx.send(f'Disk.status: {self.type} drive not available')
            return 0
        if not self.drive.avail:
            udptx.send(f'Disk.status: drive {self.selected_drive} not valid')
            return 0
        return self.drive.status()


class Drive:
    def __init__(self, driveno, fs, avail=True): #
        self.udp = udp.UdpTx(port=5006)
        self.driveno = driveno
        self.tracks = fs.tracks
        self.bytes_per_track = fs.bpt
        self.data = fs.data
        self.marks = fs.marks
        self.current_track = 0
        self.current_byte = 0
        self.avail = avail


    def dump(self, track):
        misc.hexdump(self.data[track], 32, 511)


    def istrack0(self):
        return self.current_track == 0


    def isindex(self):
        return self.current_byte == 0


    def step(self, direction):
        self.current_byte = 0 # assumption
        if direction: # UP
            msg = f'disk {self.driveno}, step up 0x{direction:02x}'
            msg += f', track {self.current_track} -> {self.current_track + 1}'
            udptx.send(msg)
            self.current_track = (self.current_track + 1) % self.tracks
        else: # DOWN
            msg = f'disk {self.driveno}, step down {direction:02x}'
            msg += f', track {self.current_track} -> {self.current_track - 1}'
            udptx.send(msg)
            if self.current_track == 0:
                return
            self.current_track -= 1


    def readbyte(self):
        track = self.current_track
        byte = self.current_byte
        #udptx.send(f'Drive.readbyte() - driveno {self.driveno}, trk {track}, byte {byte}')
        assert 0 <= track < self.tracks
        assert 0 <= byte < self.bytes_per_track, byte
        self.current_byte = (self.current_byte + 1) % self.bytes_per_track
        return self.data[track][byte]


    def writebyte(self, value):
        track = self.current_track
        byte = self.current_byte - 3 # TODO don't understand this offset
        d = self.data[track][byte]

        assert 0 <= track < self.tracks
        assert 0 <= byte < self.bytes_per_track, byte
        self.data[track][byte] = value
        self.current_byte = (self.current_byte + 1) % self.bytes_per_track


    def gettrackno(self):
        return self.current_track

    # Very unsure about the correct implementation, but this seems to work
    def isbusy(self):
        while self.current_byte not in self.marks[self.current_track]:
            self.current_byte = (self.current_byte + 1) % self.bytes_per_track
        return True


    def status(self):
        if not self.avail:
            udptx.send(f'this disk {self.driveno} is unavailable (status 0)')
            return 0
        status = statusbits["sdready"]
        if self.isindex():
            status += statusbits["index"]
        if self.isbusy():
            status += statusbits["busy"]
        if self.istrack0():
            status += statusbits["track0"]
        return status


statusbits = {
    "dbleside"   : 0x02,
    "track0"     : 0x10,
    "index"      : 0x20,
    "sdready"    : 0x40,
    "busy"       : 0x80
}

class Control:
    def __init__(self, type, fs_list):
        self.disk = Disk(type, fs_list)


    def data_in(self) -> int:
        val = self.disk.readbyte()
        return val


    def data_out(self, value):
        self.disk.writebyte(value)


    def control1(self, val):
        drive = val & 0x7f
        side = val >> 7
        if drive == 0:
            return

        assert drive in [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40], f'val: 0x{drive:02x}'
        i = 1
        while True:
            if drive == 1:
                break
            drive /= 2
            i += 1
        assert i in [1, 2, 3, 4, 5, 6, 7]
        udptx.send(f'Control.control1(): drive selected: {i}')
        self.disk.select_drive(i)


    def control2(self, val):
        stepdir = val & 0x40
        if val & 0x20: # Step
            self.disk.step(stepdir)
        if val & 0x80:
            self.disk.write_ena = True
        else:
            self.disk.write_ena = False


    def status(self):
        return self.disk.status()
