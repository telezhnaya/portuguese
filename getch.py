import sys
import termios
import tty


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == '\x03':
            raise KeyboardInterrupt
        elif ch == '\x04':
            raise EOFError
        elif ch == '\033':  # arrows
            sys.stdin.read(1)
            ch = sys.stdin.read(1)
            if ch == 'A':
                ch = 'w'
            elif ch == 'B':
                ch = 's'
            elif ch == 'C':
                ch = 'd'
            elif ch == 'D':
                ch = 'a'
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
