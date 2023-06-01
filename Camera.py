import cv2 as cv


class Camera:
    def __init__(self, width, height, lo_th=85, hi_th=50, color=0):
        self.lo_th = lo_th  # low-luminosity threshold
        self.hi_th = hi_th  # high-luminosity threshold
        self.color = color  # color of the light

        self.video_capture = cv.VideoCapture(0)

        if not self.video_capture.isOpened():
            self.video_capture.open()
            if not self.video_capture.isOpened():
                print("Cannot open camera")
                exit()

    def __del__(self):
        self.video_capture.release()

    def get_gray_frame(self, width, height):
        isRead, frame = self.video_capture.read()

        if not isRead:
            print("Can't receive frame (stream end ?). Exiting...")
            exit()

        frame = cv.flip(frame, 1)
        frame = cv.resize(frame, (width, height),
                          interpolation=cv.INTER_AREA)
        return cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    def increase_lo_th(self):
        if self.lo_th < 255:
            self.lo_th += 1

    def decrease_lo_th(self):
        if self.lo_th > 0:
            self.lo_th -= 1

    def increase_hi_th(self):
        if self.hi_th < 255:
            self.hi_th += 1

    def decrease_hi_th(self):
        if self.hi_th > 0:
            self.hi_th -= 1

    def increase_color(self):
        if self.color < 255:
            self.color += 1

    def decrease_color(self):
        if self.color > 0:
            self.color -= 1
