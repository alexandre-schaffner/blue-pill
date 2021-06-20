#!python3

import cv2 as cv
import curses

#===CLASS===#
class LenseParams:
    def __init__(self, lo_th = 85, hi_th = 50, color = 210):
        self.lo_th = lo_th
        self.hi_th = hi_th
        self.color = color

class Screen:
    def __init__(self):
        self.screen = curses.initscr()
        self.height, self.width = self.screen.getmaxyx()
        self.screen.nodelay(True)
        self.screen.keypad(True)
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()
        self.screen.clear()
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)
#=================================================================================================================#

#===INIT WEBCAM CAPTURE===#
def init_capture():
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        cap.open();
        if not cap.isOpened():
            print("Cannot open camera")
            exit()
    return cap

#===CONVERT PIXEL LUMINOSITY TO ASCII===#
def convert_to_ascii(coord, px, lense, scr): #coord is tupple (y, x)
    char = int(px / (256 / 70))
    gray_ramp = " .`:,;'_^\"\></-!~=)(|j?}{ ][ti+l7v1%yrfcJ32uIC$zwo96sngaT5qpkYVOL40&mG8*xhedbZUSAQPFDXWK#RNEHBM@"

    if px < lense.lo_th or px > (255 - lense.hi_th):
        scr.screen.addch(coord[0], coord[1], ' ')
    elif char > 69:
        scr.screen.addch(coord[0], coord[1], '@', curses.color_pair(lense.color + char))
    else:
        scr.screen.addch(coord[0], coord[1], gray_ramp[char], curses.color_pair(lense.color + char))

#===PRINT KEYBINDING AND PARAMETERS===#
def print_keys(scr):
    scr.screen.addstr(scr.height - 4, 0, "Keys:                                   ")
    scr.screen.addstr(scr.height - 3, 0, "Q/D: tweak treshhold on low luminosity  ")
    scr.screen.addstr(scr.height - 2, 0, "Z/S: tweak treshhold on high luminosity ")
    scr.screen.addstr(scr.height - 1, 0, "A/E: change colors                      ")
    scr.screen.addstr(scr.height - 1, scr.width - 17, " `Space` to quit")

def print_params(scr, lense):
        scr.screen.addstr(0, 0, "treshhold ")
        scr.screen.addstr(1, 0, "".join(["lo_th: ",str(lense.lo_th), " "]))
        scr.screen.addstr(2, 0, "".join(["hi_th: ",str(lense.hi_th), " "]))
        scr.screen.addstr(0, scr.width - 7, " color ")
        scr.screen.addstr(1, scr.width - 7, "".join(["   ", str(lense.color)]))

def reset(scr):
    scr.screen.keypad(False)
    curses.echo()
    curses.nocbreak()
    curses.endwin()


def main():
    lense = LenseParams()
    scr = Screen()
    cap = init_capture()

    #===MAIN LOOP===#
    while 1:
        #===CATCH KEYS===#
        c = scr.screen.getch()
        if c == ord(' '):
            break
        elif c == ord('q') and lense.lo_th > 0:
            lense.lo_th -= 1
        elif c == ord('d') and lense.lo_th < 255:
            lense.lo_th += 1
        elif c == ord('z') and lense.hi_th < 255:
            lense.hi_th += 1
        elif c == ord('s') and lense.hi_th > 0:
            lense.hi_th -= 1
        elif c == ord('a') and lense.color > 0:
            lense.color -= 1
        elif c == ord('e') and lense.color < 255:
            lense.color += 1
        #===READ IMAGE FROM WEBCAM===#
        isRead, frame = cap.read()
        if not isRead:
            print("Can't receive frame (stream end ?). Exiting...")
            break
        frame = cv.flip(frame, 1)
        frame = cv.resize(frame, (scr.width, scr.height), interpolation = cv.INTER_AREA)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        scr.screen.move(0, 0)
        for i_x in range(scr.width - 1):
            for i_y in range(scr.height):
                convert_to_ascii((i_y, i_x), gray.item(i_y, i_x), lense, scr)
        print_params(scr, lense)
        print_keys(scr)
        scr.screen.refresh();

    #===END===#
    cap.release()
    reset(scr)

main()
