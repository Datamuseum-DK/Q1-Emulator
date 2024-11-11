import sys
import termios
from select import select
#from enum import Enum

# class kMBP(Enum):
#     optb = 0x222b
#     optc = 231
#     optg = 169
#     optm = 181
#     backspace = 127
#

class KeyboardCodes:

    def __init__(self, input="macos"):
        if input == "macos":
            self.input = self.macos
        else:
            assert False, 'no known keyboard input provided'


    # Macos mappings for Q1 Emulator
    macos = {
        #"TAB CLR"     : 0x02,
        "TAB SET"     :  339,  # opt-q
        "CORR"        :  127,  # backspace
        "TAB"         :    9,  # TAB
        "RETURN"      :   10,  # RETURN
        "GO"          :  169,  # opt-g
        "STOP"        :  223,  # opt-s
        #"REV TAB"     : 0x10,
        "HEX"         : 8721,  # opt-w
        "CLEAR ENTRY" :  231,  # opt-c
        "CHAR ADV"    :  172,  # opt-l
        "DEL CHAR"    : 8706,  # opt-d
        "INSERT MODE" :  181,  # opt-m
        # Reset is not a keyboard input, but the red
        # button on the right side of the cabinet
        "RESET"       :  174   # opt-r
    }

    windows = {
        #"TAB CLR"     : 0x02,
        # "TAB SET"     : 339,  # opt-q
        # "CORR"        : 127,  # backspace
        # "TAB"         :   9,  # TAB
        # "RETURN"      :  10,  # RETURN
        # "GO"          : 169,  # opt-g
        # "STOP"        : 223,  # opt-s
        #"REV TAB"     : 0x10,
        # "HEX"         : 8721, # opt-w
        # "CLEAR ENTRY" :  231, # opt-c
        # "CHAR ADV"    :  172, # opt-l
        # "DEL CHAR"    : 8706, # opt-d
        # "INSERT MODE" : 181   # opt-m
    }

    # Key codes used by Q1
    q1key = {
        "TAB CLR"     : 0x02,
        "TAB SET"     : 0x03,
        "CORR"        : 0x04,
        "TAB"         : 0x09,
        "RETURN"      : 0x0d,
        "GO"          : 0x0e,
        "STOP"        : 0x0f,
        "REV TAB"     : 0x10,
        "F1"          : 0x11, # Not all Fn keys are confirmed
        "F2"          : 0x12,
        "F3"          : 0x13,
        "F4"          : 0x14,
        "F5"          : 0x15,
        "F6"          : 0x16,
        "F7"          : 0x17,
        "F8"          : 0x18,
        "F9"          : 0x19,
        "HEX"         : 0x1a,
        "CLEAR ENTRY" : 0x1b,
        "CHAR ADV"    : 0x1c,
        "DEL CHAR"    : 0x1d,
        "INSERT MODE" : 0x1e
    }

    # get input key value for Q1 keyboard
    def ikey(self, s):
        assert s in self.input
        return self.input[s]

    # get output key value for Q1
    def okey(self, s):
        assert s in self.q1key
        return self.q1key[s]




class Key:

    def __init__(self):
        # save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)

        # new terminal setting unbuffered
        self.new_term[3] = self.new_term[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)


    def __del__(self):
        # switch to normal terminal
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)


    def putch(self, ch):
        sys.stdout.write(ch)

    def getch(self):
        return sys.stdin.read(1)

    def getche(self):
        ch = self.getch()
        self.putch(ch)
        return ch

    def kbhit(self):
        dr,_,_ = select([sys.stdin], [], [], 0)
        return dr != []

if __name__ == '__main__':

    kbd = Key()

    while 1:
        if kbd.kbhit():
            char = kbd.getch()
            break
        print("A")
        #sys.stdout.write('.')

    print(f'done {char}')
