import curses


class Screen:
    # CONSTRUCTOR
    def __init__(self):
        # CURSES INITIALIZATION
        self.display = curses.initscr()
        self.display.nodelay(True)
        self.display.keypad(True)
        self.display.clear()
        curses.curs_set(0)
        curses.noecho()
        curses.cbreak()

        # COLOR INITIALIZATION
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

        # GET SCREEN SIZE
        self.height, self.width = self.display.getmaxyx()

    # DESTRUCTOR
    def __del__(self):
        self.display.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    # METHODS

    def refresh(self):
        self.display.refresh()
