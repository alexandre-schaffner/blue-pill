#!python3

from os import system
import numpy as np
import cv2 as cv
import curses


#===CONVERT GRAYSCALE TO ASCII===#
def convert_to_ascii(coord, px, th, color): #coord is tupple (y, x)
    char = int(px / (256 / 70))
    gray_ramp = " .`:,;'_^\"\></-!~=)(|j?}{ ][ti+l7v1%yrfcJ32uIC$zwo96sngaT5qpkYVOL40&mG8*xhedbZUSAQPFDXWK#RNEHBM@"
    if px < th or px > (255 - th):
        scr.addch(coord[0], coord[1], ' ')
    elif char > 69:
        scr.addch(coord[0], coord[1], '@', curses.color_pair(color + char))
    else:
        scr.addch(coord[0], coord[1], gray_ramp[char], curses.color_pair(color + char))
#==========================================================================================#

#===INIT WEBCAM CAPTURE===#
cap = cv.VideoCapture(0);
th = 95
if not cap.isOpened():
    cap.open();
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

#===INIT TERM===#
scr = curses.initscr()
curses.start_color()
curses.use_default_colors()
for i in range(0, curses.COLORS):
    curses.init_pair(i + 1, i, -1)
#curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
color = 0
height, width = scr.getmaxyx()
scr.nodelay(True)
scr.keypad(True)
curses.curs_set(0)
curses.noecho()
curses.cbreak()
scr.clear()

#===MAIN LOOP===#
while True:
    c = scr.getch()
    if c == ord('q'):
        break
    elif c == curses.KEY_DOWN and th > 0:
        th -= 1
    elif c == curses.KEY_UP and th < 255:
        th += 1
    elif c == ord('a') and color > 0:
        color -= 1
    elif c == ord('p') and color < 255:
        color += 1
    isRead, frame = cap.read()
    if not isRead:
        print("Can't receive frame (stream end ?). Exiting...")
        break
    frame = cv.resize(frame, (width, height), interpolation = cv.INTER_AREA)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    scr.move(0, 0)
    for i_x in range(width - 1):
        for i_y in range(height - 1):
            convert_to_ascii((i_y, i_x), gray.item(i_y, i_x), th, color)
    scr.addstr(0, 0, str(th))
    scr.refresh();

#===END===#
cap.release()
scr.keypad(False)
curses.echo()
curses.nocbreak()
curses.endwin()
