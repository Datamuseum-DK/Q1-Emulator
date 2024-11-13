


# "Q1 ASM IO addresses usage Q1 Lite" p. 75 - 77
class SerialImpactPrinter:

    def __init__(self):
        self.poshi2 = 0
        self.pos = [0.0, 0.0]
        self.dir = [0, 0]
        self.buffer = ''

    def status(self) -> int:
        return 0x01 # selected


    def output(self, value):
        self.buffer += chr(value)


    def ctrl_06(self, value: int):
        dist = (self.poshi2 << 8) + value
        x, y = self.pos
        dx, dy = self.dir

        if dx != 0: # x-dir
            dir = f'<->'
            cm = 2.54 * dist / 60 # cm
            v = cm * dx
            x = x + v
            if dx < -0.00001:
                print(self.buffer)
                self.buffer = ''
            else:
                self.buffer += ' ' * (int(v/0.21) -1)

        if dy != 0: # y-dir
            dir = f' I '
            cm = 2.54 * dist / 48 # cm
            v = cm * dy
            y = y + v
        self.pos = [x, y]
        #print(f'SI printer ctrl: move {dir} {v:6.2f} cm. pos ({x:6.2f}, {y:6.2f})')


    def ctrl_07(self, value: int):
        self.poshi2 = value & 0x3
        desc = ''
        if value & 0x80:
            desc += 'reset, '
            self.pos[0] = 0.0
        if value & 0x40:
            desc += 'exp res, '
        if value & 0x20:
            desc += 'raise ribbon, '
        if value & 0x10:
            desc += 'lower ribbon, '
        if value & 0x08:
            desc += 'paper '
            self.dir = [0, 1]
        else:
            desc += 'carriage '
            self.dir = [1, 0]
        if value & 0x04:
            self.dir[0] = - self.dir[0]
            self.dir[1] = - self.dir[1]
            assert self.dir[1] >= 0
            desc += 'reverse '
        else:
            desc += 'forward '
        desc += 'motion'

        #print(f'SI printer ctrl: - 0x{value:02x} [{desc}]')
