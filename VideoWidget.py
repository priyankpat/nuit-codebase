import cv2
from qtpy import QtWidgets, QtCore, QtGui
from threading import Thread
from collections import deque
import time
import imutils
import random
from file import File
from imutils.video import FPS

class VideoWidget(QtWidgets.QWidget):
    def __init__(self, category, registry, hist=None, width=200, height=300, aspect_ratio=False, parent=None,
                 deque_size=1):
        super(VideoWidget, self).__init__(parent)

        self.deque = deque(maxlen=deque_size)
        self.fps = 0

        self.offset = 0
        self.screen_width = width - self.offset
        self.screen_height = height - self.offset
        self.maintain_aspect_ratio = aspect_ratio

        self.registry = registry
        self.category = self.search(category)
        self.scene_list = self.category.get_scenes()

        self.played_list = []

        self.active = False
        self.capture = None
        self.hist = hist
        self.video_frame = QtWidgets.QLabel()

        self.static_back = None
        self.motion_list = None
        self.time_list = None

        self.start_time = None
        self.end_time = None

        self.source = self.scene_list[0]
        self.load_stream()

        # start background frame capture
        self.frame_capture_thread = Thread(target=self.frame_capture, args=())
        self.frame_capture_thread.daemon = True
        self.frame_capture_thread.start()

        # set video frame to render frame
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.render_frame)
        self.timer.start(.5)

    def search(self, category):
        res = None
        for x in self.registry:
            if x.name == category:
                res = x
        return res

    def search_validate(self, category):
        res = None

        reg_file_ref = File()
        current_ref = reg_file_ref.read()

        for x in self.registry:
            # if x.name == category and x.name not in current_ref:
            if x.name == category:
                res = x
        return res

    def search_old(self, scene):
        contains = False
        for x in self.played_list:
            if x.id == scene.id:
                contains = True
        return contains

    def verify_stream(self, link):
        capture = cv2.VideoCapture(link)
        if not capture.isOpened():
            return False
        capture.release()
        return True

    def load_stream_thread(self):
        if self.verify_stream(self.source.path):
            self.played_list.append(self.source)

            f = File()
            f.add(self.category.name)

            self.capture = cv2.VideoCapture(self.source.path)
            self.fps = FPS().start()
            self.active = True

    def load_stream(self):
        self.load_stream_thread_ref = Thread(target=self.load_stream_thread, args=())
        self.load_stream_thread_ref.daemon = True
        self.load_stream_thread_ref.start()

    def frame_capture(self):
        while True:
            try:
                if self.capture.isOpened() and self.active:
                    status, frame = self.capture.read()

                    if status:
                        self.deque.append(frame)

                        self.fps.stop()
                        print("[INFO] elasped time: {:.2f}".format(self.fps.elapsed()))
                        print("[INFO] approx. FPS: {:.2f}".format(self.fps.fps()))
                    else:
                        print('Not active status')

                        self.capture.release()
                        self.active = False

                else:
                    print('Capture is not opened')

                    if len(self.played_list) == len(self.scene_list):
                        reg_file_ref = File()
                        reg_file_ref.remove(self.category.name)

                    if len(self.played_list) < len(self.scene_list):
                        for scene in self.scene_list:
                            if not self.search_old(scene):
                                self.source = scene
                                self.load_stream()
                                break
                    else:
                        print('Randomizing category')

                        cat = random.choice(self.registry)
                        self.category = self.search_validate(cat.name)
                        self.scene_list = self.category.get_scenes()
                        self.source = self.scene_list[0]
                        self.played_list = []
                        self.load_stream()

                self.spin(.05)
            except AttributeError:
                pass

    def spin(self, seconds):
        time_end = time.time() + seconds
        while time.time() < time_end:
            QtGui.QGuiApplication.processEvents()

    def render_frame(self):
        if not self.active:
            self.spin(1)
            return

        if self.deque and self.active:
            frame = self.deque[-1]

            if self.maintain_aspect_ratio:
                self.frame = imutils.resize(frame, width=self.screen_width)
            else:
                self.frame = cv2.resize(frame, (self.screen_width, self.screen_height))

            # convert to pixmap and add to video frame
            # aligned = cv2.resize(self.frame, (self.frame.shape[1] // 4 * 4, self.frame.shape[0] // 4 * 4), fx=0, fy=0,
            #                      interpolation=cv2.INTER_NEAREST)
            # rgb = cv2.cvtColor(aligned, cv2.COLOR_BGR2RGB)
            # self.img = QtGui.QImage(rgb.data, rgb.shape[1], rgb.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.img = QtGui.QImage(self.frame, self.frame.shape[1], self.frame.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.pix = QtGui.QPixmap.fromImage(self.img)
            self.video_frame.setPixmap(self.pix)
            self.fps.update()

    def get_video_frame(self):
        return self.video_frame
