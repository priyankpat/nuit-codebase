import sys
import cv2
import qdarkstyle
from qtpy import QtWidgets, QtCore, QtGui
from VideoWidget import VideoWidget
import json
import random
from Scene import Scene
from Category import Category
from file import File
from threading import Thread


def exit_application(self):
    sys.exit(1)


def load_registry():
    regData = []
    registry_file = open('./data/registry.json')
    registry_data = json.load(registry_file)
    registry_file.close()

    for cat in registry_data['data']:
        cat_id = cat['id']
        scenes = cat['videos']
        cat = Category(cat_id)

        for sce in scenes:
            scene = Scene(sce['id'], sce['path'])
            cat.addscene(scene)

        regData.append(cat)

    return regData


def randomize_startup(registry):
    startup_sequece = []  # contains 3 random category
    random_cat = random.choice(registry)

    while len(startup_sequece) < 3:
        if random_cat.name not in startup_sequece:
            startup_sequece.append(random_cat.name)
        random_cat = random.choice(registry)

    return startup_sequece

if __name__ == '__main__':
    video_registry = load_registry()
    start_registry = randomize_startup(video_registry)

    app = QtWidgets.QApplication([])
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt())
    app.setStyle(QtWidgets.QStyleFactory.create("Nunito"))

    mainWindow = QtWidgets.QMainWindow()
    mainWindow.setWindowTitle("Nuit")
    mainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    centralWidget = QtWidgets.QWidget()
    gridLayout = QtWidgets.QGridLayout()
    centralWidget.setLayout(gridLayout)
    mainWindow.setCentralWidget(centralWidget)
    mainWindow.showMaximized()

    screen_width = QtWidgets.QApplication.desktop().screenGeometry().width()
    screen_height = QtWidgets.QApplication.desktop().screenGeometry().height()

    ref_file_db = File()
    init_list = ref_file_db.read()
    ref_file_db.empty()

    print('--------')
    print(start_registry)
    if len(init_list) == 0:
        list_to_write = []
        for sr in start_registry:
            print('--')
            print(sr)
            list_to_write.append(sr)
        print(list_to_write)
        ref_file_db.write(list_to_write)

    # write_thread = Thread(target=write_to_reg_file, args=())
    # write_thread.daemon = True
    # write_thread.start()

    screen_1 = VideoWidget(start_registry[0], video_registry, None, screen_width // 3, screen_height)
    screen_2 = VideoWidget(start_registry[1], video_registry, None, screen_width // 3, screen_height)
    screen_3 = VideoWidget(start_registry[2], video_registry, None, screen_width // 3, screen_height)

    gridLayout.addWidget(screen_1.get_video_frame(), 0, 0)
    gridLayout.addWidget(screen_2.get_video_frame(), 0, 1)
    gridLayout.addWidget(screen_3.get_video_frame(), 0, 2)

    mainWindow.show()

    QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+Q'), mainWindow, exit_application)

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtWidgets.QApplication.instance().exec_()
