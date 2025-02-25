import utils.udptx as udp

'''
    Display emulator for Q1
'''

subst = {'[':'Ä', ']':'Å', '\\':'Ö', '}':'å', '|':'ö', '{':'ä'}

class Display:

    def __init__(self, height=12, width=47):
        self.w = width
        self.h = height
        self.pos = (0,0)
        self.buffer = [[chr(0x20) for x in range(width)] for y in range(height)]

        self.udp = udp.UdpTx(port=5005)


    def _incx(self):
        x, y = self.pos
        x += 1
        if x == self.w:
            x = 0
            y += 1
        if y == self.h:
            #print('y exceeds maximum')
            y = 0
        self.pos = (x,y)


    def data(self, char):
        if 32 <= ord(char) < 127:
            x, y = self.pos
            # if char in subst:
            #     char = subst[char]
            self.buffer[y][x] = char
        self._incx()


    def control(self, val):
        reset   = val & 0x01
        #blank   = val & 0x02
        #unblank = val & 0x04
        step    = val & 0x08

        if reset:
            self.pos = (0,0)
        elif step:
            self._incx()


    def update(self):
        msg = chr(self.pos[0]) + chr(self.pos[1])
        for l in self.buffer:
            msg += ''.join(l)
        self.udp.send(msg)

if __name__ == '__main__':
    import time
    d = Display()
    while True:
        d.data('a')
        d.update()
        time.sleep(1)
