import Paths
import PlayList

from .Slider import Slider
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5 import QtMultimedia


class CurrentlyPlaying(QtWidgets.QWidget):

    current_file = ""
    current_tile = None

    playing = QtCore.pyqtSignal(bool)
    current_tile_changed = QtCore.pyqtSignal(object)

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
        self.play_list = PlayList.PlayList()

        self.next = QtWidgets.QPushButton(objectName="Next", clicked=self.nextSong)
        self.previous = QtWidgets.QPushButton(objectName="Previous", clicked=self.previousSong)

        # self.progress = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.progress = Slider(QtCore.Qt.Horizontal)
        self.progress.valueChanged.connect(self.setMusicPosition)
        self.progress.clicked.connect(self.setMusicPosition)

        self.progress_lbl = QtWidgets.QLabel()
        self.progress_lbl.setWordWrap(True)

        self.player = QtMultimedia.QMediaPlayer()
        # self.player.mediaStatusChanged.connect(self.mediaStatusChanged)
        self.player.durationChanged.connect(self.setDuration)
        self.player.positionChanged.connect(self.changeSliderPos)
        self._duration = f"00:00:00"
        self._formatted_duration = f"00:00:00"

        grid_layout.addWidget(self.thumb_nail, 0, 0, 1, 3)
        grid_layout.addWidget(self.title, 1, 0, 1, 3)
        grid_layout.addWidget(self.previous, 2, 0, alignment=QtCore.Qt.AlignTop)
        grid_layout.addWidget(self.play_pause_btn, 2, 1, alignment=QtCore.Qt.AlignTop)
        grid_layout.addWidget(self.next, 2, 2, alignment=QtCore.Qt.AlignTop)
        grid_layout.addWidget(self.progress, 3, 0, 1, 3, alignment=QtCore.Qt.AlignTop)
        grid_layout.addWidget(self.progress_lbl, 4, 0, 1, 3, alignment=QtCore.Qt.AlignHCenter)

        grid_layout.setRowStretch(6, 1)

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
        print(self.player.duration())
        self.play()

    def changeSliderPos(self, value):
        self.progress.blockSignals(True)
        self.progress.setSliderPosition(value)
        duration = QtCore.QDateTime.fromTime_t(value / 1000).toUTC().toString("hh:mm:ss")
        self.progress_lbl.setText(f"{duration}/{self._formatted_duration}")
        self.progress.blockSignals(False)

    def setDuration(self, duration):
        self._duration = duration

        self._formatted_duration = QtCore.QDateTime.fromTime_t(duration/1000).toUTC().toString("hh:mm:ss")
        # self.progress_lbl.setText(f"00:00:00/{self._formatted_duration}")
        print("real duration: ", duration)
        h, m, s = list(map(int, self._formatted_duration.split(':')))
        max_range = h*3600 + m * 60 + s

        self.progress.setRange(0, duration)
        print(self._duration)
        self.progress_lbl.setText(f"{max_range}")

    def setMusicPosition(self, value):
        print(value)
        self.player.setPosition(value)
        duration = QtCore.QDateTime.fromTime_t(value/1000).toUTC().toString("hh:mm:ss")
        self.progress_lbl.setText(f"{duration}/{self._formatted_duration}")

    def play_pause(self):
        self._playing = not self._playing

        if self._playing:
            self.play()

        else:
            self.pause()

    def _setCurrentMusicObj(self, music_obj):

        self.setCurrentPath(music_obj.getFile())
        self.setThumbNail(music_obj.getThumbnail())
        self.setTitle(music_obj.getTitle())

        self.load_file()

        self.current_tile_changed.emit(music_obj)

    def setPlaylistIndex(self, tile):
        current_index = self.play_list.getIndex(tile)
        self.play_list.setCurrentIndex(current_index)

    def nextSong(self):

        music_obj = self.play_list.next()
        if music_obj:
            self._setCurrentMusicObj(music_obj)

        else:
            self.next.setEnabled(False)

    def previousSong(self):
        music_obj = self.play_list.previous()

        if music_obj:
            self._setCurrentMusicObj(music_obj)

        else:
            self.previous.setEnabled(False)

    def _play(self):
        self.play_pause_btn.setIcon(QtGui.QIcon(Paths.PAUSE))
        self.play_pause_btn.setToolTip("pause")

    def _pause(self):
        self.play_pause_btn.setIcon(QtGui.QIcon(Paths.PLAY))
        self.play_pause_btn.setToolTip("playing")

    def isPlaying(self):
        return self._playing

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