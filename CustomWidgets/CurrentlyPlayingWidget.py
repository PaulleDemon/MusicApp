import Paths
import PlayList

from .Slider import Slider
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5 import QtMultimedia


# todo: disable slider and pause the song if the position is not seekable
# todo: slider doesn't work good when
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
        self.play_pause_btn.setEnabled(False)
        self._pause()

        self._playing = False
        self.play_list = PlayList.PlayList()

        self.next = QtWidgets.QPushButton(objectName="Next", clicked=self.nextSong)
        self.previous = QtWidgets.QPushButton(objectName="Previous", clicked=self.previousSong)

        self.next.setEnabled(False)
        self.previous.setEnabled(False)

        # self.progress = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.progress = Slider(QtCore.Qt.Horizontal)
        self.progress.valueChanged.connect(self.setMusicPosition)
        self.progress.setEnabled(False)
        # self.progress.clicked.connect(self.moveSliderToClicked)

        self.progress_lbl = QtWidgets.QLabel("No Music")
        self.progress_lbl.setWordWrap(True)

        self._duration = f"00:00:00"
        self._formatted_duration = f"00:00:00"

        self.player = QtMultimedia.QMediaPlayer()
        # self.player.mediaStatusChanged.connect(self.mediaStatusChanged)
        self.player.durationChanged.connect(self.setDuration)

        self.volume_indicator = ButtonLabel()
        self.volume_indicator.setMaximumSize(50, 50)
        self.volume_indicator.setScaledContents(True)
        self.volume_indicator.clicked.connect(self.setMuted)

        self.volume_slider = Slider(QtCore.Qt.Horizontal)
        self.volume_slider.valueChanged.connect(self.setVolume)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setSliderPosition(70)

        grid_layout.addWidget(self.thumb_nail, 0, 0, 1, 3)
        grid_layout.addWidget(self.title, 1, 0, 1, 3)
        grid_layout.addWidget(self.previous, 2, 0, alignment=QtCore.Qt.AlignTop)
        grid_layout.addWidget(self.play_pause_btn, 2, 1, alignment=QtCore.Qt.AlignTop)
        grid_layout.addWidget(self.next, 2, 2, alignment=QtCore.Qt.AlignTop)
        grid_layout.addWidget(self.progress, 3, 0, 1, 3, alignment=QtCore.Qt.AlignTop)
        grid_layout.addWidget(self.progress_lbl, 4, 0, 1, 3, alignment=QtCore.Qt.AlignHCenter)
        grid_layout.setRowStretch(5, 2)
        grid_layout.addWidget(self.volume_slider, 6, 0, 1, 2, alignment=QtCore.Qt.AlignHCenter)
        grid_layout.addWidget(self.volume_indicator, 6, 3, 1, 1, alignment=QtCore.Qt.AlignHCenter)

        grid_layout.setRowStretch(7, 1)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super(CurrentlyPlaying, self).resizeEvent(event)
        self.thumb_nail.setFixedHeight(self.thumb_nail.width())

    def setThumbNail(self, image: QtGui.QPixmap):
        self.thumb_nail.setPixmap(image)

    def setCurrentPath(self, path: str):
        self.current_file = path

    def setTitle(self, text):
        self.title.setText(text)

    def setVolume(self, value):
        self.player.setMuted(False)
        self.player.setVolume(value)

        if value == 0:
            image_path = Paths.VOLUME_LVL_0

        elif 0 < value < 40:
            image_path = Paths.VOLUME_LVL_1

        elif 40 <= value < 60:
            image_path = Paths.VOLUME_LVL_2

        else:
            image_path = Paths.VOLUME_LVL_3

        self.volume_indicator.setPixmap(QtGui.QPixmap(image_path))

    def setMuted(self):
        self.player.setMuted(not self.player.isMuted())

        if self.player.isMuted():
            image_path = Paths.MUTED

        else:
            image_path = Paths.VOLUME_LVL_1

        self.volume_indicator.setPixmap(QtGui.QPixmap(image_path))

    def load_file(self):
        self.play_pause_btn.setEnabled(True)
        self.next.setEnabled(True)
        self.previous.setEnabled(True)
        self.progress.setEnabled(True)

        url = QtCore.QUrl.fromLocalFile(self.current_file)
        self.content = QtMultimedia.QMediaContent(url)
        self.player.setMedia(self.content)
        self.player.positionChanged.connect(self.changeSliderPos)
        # self.play()

    def setProgressLabel(self, value):
        print("Progress: ", self.sender(), value)
        duration = QtCore.QDateTime.fromTime_t(value / 1000).toUTC().toString("hh:mm:ss")
        self.progress_lbl.setText(f"{duration}/{self._formatted_duration}")

    def changeSliderPos(self, value):
        # print("Value2: ", value)

        self.progress.blockSignals(True)
        self.progress.setSliderPosition(value)
        self.progress.blockSignals(False)

        self.setProgressLabel(value)

    def moveSliderToClicked(self, value):  # todo: remove this as there is no use
        self.progress.setSliderPosition(value)
        self.player.setPosition(value)
        self.setProgressLabel(value)

    def setMusicPosition(self, value):
        # print(value)

        self.player.setPosition(value)
        self.player.play()

        self.setProgressLabel(value)

    def setDuration(self, duration):
        self._duration = duration

        self._formatted_duration = QtCore.QDateTime.fromTime_t(duration / 1000).toUTC().toString("hh:mm:ss")
        # self.progress_lbl.setText(f"00:00:00/{self._formatted_duration}")
        print("real duration: ", duration)

        h, m, s = list(map(int, self._formatted_duration.split(':')))
        max_range = h * 3600 + m * 60 + s

        self.progress.setEnabled(True)

        if not self.player.isSeekable() or self._duration == 0:
            QtCore.QTimer.singleShot(5, lambda: self.progress_lbl.setText("Not Playable"))
            self.progress.setEnabled(False)
            self.player.positionChanged.disconnect(self.changeSliderPos)
            self.pause()
            print("Not Playable")
            return

        self.play()
        self.progress.setRange(0, duration)
        print("duration: ", self._duration)
        self.setProgressLabel(duration)

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


class ButtonLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()
    
    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        super(ButtonLabel, self).mousePressEvent(event)
        if event.button() == QtCore.Qt.LeftButton:
            self.clicked.emit()