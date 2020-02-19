import sys
import numpy as np
import cv2
import imutils

from PySide2 import (QtWidgets as qtw, QtCore as qtc, QtGui as qtg)
try:
    from .images_viewer_view import ImagesViewerView
    from Masa.core.datahandler import FrameInfo
except ModuleNotFoundError:
    sys.path.append("../../../")
    from images_viewer_view import ImagesViewerView
    from Masa.core.datahandler import FrameInfo


class ImagesViewersDockView(qtw.QDockWidget):
    jump_to_frame = qtc.Signal(int)

    def __init__(self, parent=None, window_title="Images Viewers Dock"):
        super().__init__(parent)
        self.window_title = window_title
        self._images_viewers = {}

        self.set_window_attributes()
        self.set_widgets()
        self.optimize_widgets()
        self.set_layouts()
        self.init()

    def set_window_attributes(self):
        self.setWindowTitle(self.window_title)
        self.setFeatures(
            qtw.QDockWidget.DockWidgetMovable |
            qtw.QDockWidget.DockWidgetFloatable
        )

        # XXX: Not good
        self.setSizePolicy(
            qtw.QSizePolicy.Maximum, qtw.QSizePolicy.Maximum
            )

    # def sizeHint(self):
    #     return qtc.QSize(600, 600)

    def set_widgets(self):
        self.imgs_viewers_scroll = qtw.QScrollArea()
        self.imgs_viewers_widget = qtw.QWidget()

    def set_layouts(self):
        self.main_layout = qtw.QVBoxLayout()

    def optimize_widgets(self):
        self.imgs_viewers_scroll.setHorizontalScrollBarPolicy(qtc.Qt.ScrollBarAlwaysOff)
        self.imgs_viewers_scroll.setVerticalScrollBarPolicy(qtc.Qt.ScrollBarAsNeeded)

    def init(self):
        # put layout in each widget
        self.imgs_viewers_widget.setLayout(self.main_layout)
        self.imgs_viewers_scroll.setWidget(self.imgs_viewers_widget)

        # 'connect' each widget
        self.imgs_viewers_scroll.setWidgetResizable(True)
        # self.setLayout(self.main_layout)
        self.setWidget(self.imgs_viewers_scroll)

    def add_images_viewer(self, group: str, img_viewer: ImagesViewerView):
        """Add an ImagesViewerView object."""
        self.main_layout.addWidget(img_viewer)
        self._images_viewers[group] = img_viewer

    def add_data(self, data: FrameInfo):
        if data.object_class not in self._images_viewers.keys():
            raise ValueError()

        self._images_viewers[data.object_class].add_to_row(data)


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    main = ImagesViewersDockView()

    imgs_viewer1 = ImagesViewerView()
    f_infos = []
    for i in range(3):
        frame_info = FrameInfo(
            frame=np.zeros([69, 121, 3], np.uint8), x1=11, y1=11, x2=22, y2=22,
            object_class="Test", tag="Big", frame_id=19, track_id=i
        )
        f_infos.append(frame_info)

    main.add_images_viewer(frame_info.object_class, imgs_viewer1)
    for f_info in f_infos:
        main.add_data(f_info)

    imgs_viewer2 = ImagesViewerView()
    f_infos = []
    for i in range(3):
        frame_info = FrameInfo(
            frame=np.zeros([69, 121, 3], np.uint8), x1=11, y1=11, x2=22, y2=22,
            object_class="Test2", tag="Big", frame_id=19, track_id=i
        )
        f_infos.append(frame_info)

    main.add_images_viewer(frame_info.object_class, imgs_viewer2)
    for f_info in f_infos:
        main.add_data(f_info)

    main.show()
    sys.exit(app.exec_())
