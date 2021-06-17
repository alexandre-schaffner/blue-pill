#!python3

from os import system
import numpy as np
import cv2 as cv
import curses


#===CONVERT GRAYSCALE TO ASCII===#
def convert_to_ascii(px, th):
    if px < th:
        return (' ')
    gray_ramp = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    char = int(px / (256 / 70))
    if char >= 70:
        char = 69
    return gray_ramp[char]
#=======================================================================================#

#===INIT WEBCAM CAPTURE===#
cap = cv.VideoCapture(0);
th = 100
if not cap.isOpened():
    cap.open();
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

#===INIT TERM===#
scr = curses.initscr()
scr.nodelay(True)
scr.keypad(True)
curses.curs_set(0)
curses.noecho()
curses.cbreak()
height, width = scr.getmaxyx()
scr.clear()

#===MAIN LOOP===#
while True:
    c = scr.getch()
    if c == ord('q'):
        break
    elif c == curses.KEY_DOWN:
        th += 1
    elif c == curses.KEY_UP:
        th -= 1
    isRead, frame = cap.read()
    if not isRead:
        print("Can't receive frame (stream end ?). Exiting...")
        break
    frame = cv.resize(frame, (width, height), interpolation = cv.INTER_AREA)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    scr.move(0, 0)
    for i_x in range(0, (width - 1), 1):
        for i_y in range(0, (height - 1), 1):
            scr.addch(i_y, i_x, convert_to_ascii(gray.item(i_y, i_x), th))
    scr.refresh();

#===END===#
cap.release()
scr.keypad(False)
curses.endwin()
curses.nocbreak()
curses.echo()
