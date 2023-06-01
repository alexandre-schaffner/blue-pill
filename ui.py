from Screen import Screen
from Camera import Camera


def print_keys(screen: Screen) -> None:
    screen.display.addstr(screen.height - 4, 0,
                          "Keys:                                   ")
    screen.display.addstr(screen.height - 3, 0,
                          "Q/D: tweak treshhold on low luminosity  ")
    screen.display.addstr(screen.height - 2, 0,
                          "Z/S: tweak treshhold on high luminosity ")
    screen.display.addstr(screen.height - 1, 0,
                          "A/E: change colors                      ")
    screen.display.addstr(screen.height - 1, screen.width -
                          17, " `Space` to quit")


def print_params(screen: Screen, camera: Camera) -> None:
    screen.display.addstr(0, 0, "treshhold ")
    screen.display.addstr(1, 0, "".join(["lo_th: ", str(camera.lo_th), " "]))
    screen.display.addstr(2, 0, "".join(["hi_th: ", str(camera.hi_th), " "]))
    screen.display.addstr(0, screen.width - 7, " color ")
    screen.display.addstr(1, screen.width - 7,
                          "".join(["   ", str(camera.color)]))
