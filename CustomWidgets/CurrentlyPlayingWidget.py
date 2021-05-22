import Paths

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5 import QtMultimedia


class CurrentlyPlaying(QtWidgets.QWidget):

    current_file = ""
    current_tile = None

    playing = QtCore.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super(CurrentlyPlaying, self).__init__(*args, **kwargs)

        grid_layout = QtWidgets.QGridLayout(self)

        self.setObjectName("CurrentlyPlaying")
        self.thumb_nail = QtWidgets.QLabel()
        self.setThumbNail(QtGui.QPixmap(Paths.UNKNOWN_MUSIC))
        self.thumb_nail.setScaledContents(True)

        self.title = QtWidgets.QLabel()
        self.title.setWordWrap(True)

        self.play_pause_btn = QtWidgets.QPushButton(objectName="PlayPause")
        self.play_pause_btn.clicked.connect(self.play_pause)
        self._pause()

        self._playing = False

        self.next = QtWidgets.QPushButton(objectName="Next")
        self.previous = QtWidgets.QPushButton(objectName="Previous")

        self.progress = QtWidgets.QProgressBar()

        self.player = QtMultimedia.QMediaPlayer()

        grid_layout.addWidget(self.thumb_nail, 0, 0, 1, 3)
        grid_layout.addWidget(self.title, 1, 0, 1, 3)
        grid_layout.addWidget(self.previous, 2, 0, alignment=QtCore.Qt.AlignTop)
        grid_layout.addWidget(self.play_pause_btn, 2, 1, alignment=QtCore.Qt.AlignTop)
        grid_layout.addWidget(self.next, 2, 2, alignment=QtCore.Qt.AlignTop)
        grid_layout.addWidget(self.progress, 3, 0, 1, 3, alignment=QtCore.Qt.AlignTop)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super(CurrentlyPlaying, self).resizeEvent(event)
        self.thumb_nail.setFixedHeight(self.thumb_nail.width())

    def setThumbNail(self, image: QtGui.QPixmap):
        self.thumb_nail.setPixmap(image)

    def setCurrentPath(self, path: str):
        self.current_file = path

    def setTitle(self, text):
        self.title.setText(text)

    def load_file(self):
        url = QtCore.QUrl.fromLocalFile(self.current_file)
        self.content = QtMultimedia.QMediaContent(url)

        self.player.setMedia(self.content)
        self.play()

    def play_pause(self):
        self._playing = not self._playing

        if self._playing:
            self.play()

        else:
            self.pause()

    def _play(self):
        self.play_pause_btn.setIcon(QtGui.QIcon(Paths.PAUSE))
        self.play_pause_btn.setToolTip("pause")

    def _pause(self):
        self.play_pause_btn.setIcon(QtGui.QIcon(Paths.PLAY))
        self.play_pause_btn.setToolTip("playing")

    def play(self):
        self._play()

        self.player.play()
        self._playing = True
        self.playing.emit(self._playing)

    def pause(self):
        self._pause()

        self.player.pause()
        self._playing = False
        self.playing.emit(self._playing)