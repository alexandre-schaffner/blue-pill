#!python3

import cv2 as cv
import curses
from Screen import Screen
from Camera import Camera
from ui import print_keys, print_params


def convert_to_ascii(px: int, camera: Camera) -> str:
    char = int(px / (256 / 70))
    gray_ramp = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"

    if px < camera.lo_th or px > (255 - camera.hi_th):
        return ' '
    elif char > 69:
        return '@'
    else:
        return gray_ramp[char]


def handle_keys(screen: Screen, camera: Camera) -> None:
    c: str = screen.display.getch()

    if c == ord(' '):
        exit()
    elif c == ord('a') and camera.lo_th > 0:
        return camera.decrease_color()
    elif c == ord('d') and camera.lo_th < 255:
        return camera.increase_color()
    elif c == ord('w') and camera.hi_th < 255:
        return camera.increase_hi_th()
    elif c == ord('s') and camera.hi_th > 0:
        return camera.decrease_hi_th()
    elif c == ord('q') and camera.color > 0:
        return camera.decrease_color()
    elif c == ord('e') and camera.color < 255:
        return camera.increase_color()


def create_ascii_frame(camera: Camera, screen: Screen) -> list[list[str]]:
    gray_frame = camera.get_gray_frame(screen.width, screen.height)
    ascii_frame: list[list[str]] = [[] for i in range(gray_frame.shape[0])]

    for i_y in range(gray_frame.shape[0] - 1):
        for i_x in range(gray_frame.shape[1] - 1):
            ascii_frame[i_y].append(convert_to_ascii(
                gray_frame[i_y, i_x], camera))

    return ascii_frame


def main():
    screen = Screen()
    camera = Camera(screen.width, screen.height)

    while True:
        # Catch keypresses
        handle_keys(screen, camera)

        # Convert gray frame to ascii frame
        ascii_frame = create_ascii_frame(camera, screen)

        # Reset cursor position
        screen.display.move(0, 0)

        # Print ascii frame
        for i_y in range(0, len(ascii_frame)):
            for i_x in range(0, len(ascii_frame[i_y])):
                screen.display.addch(i_y, i_x, ascii_frame[i_y][i_x], curses.color_pair(
                    camera.color + ord(ascii_frame[i_y][i_x])))

        # Print ui elements
        print_params(screen, camera)
        print_keys(screen)

        # Refresh screen
        screen.refresh()


main()
