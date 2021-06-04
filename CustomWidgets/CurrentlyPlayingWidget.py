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
        self.play_pause_btn.setEnabled(False)
        self.play_pause_btn.setFixedSize(50, 50)
        self._pause()

        self._media_ended = False
        self._playing = False
        self._autoPlay = False
        self._loop = False

        self.play_list = PlayList.PlayList()

        self.loop_btn = QtWidgets.QPushButton("Loop")
        self.loop_btn.setCheckable(True)
        self.loop_btn.clicked.connect(self.loop)

        self.next = CircularButton(Paths.NEXT_BTN0, Paths.NEXT_BTN1, objectName="Next", clicked=self.nextSong)
        self.next.setFixedSize(50, 50)
        self.previous = CircularButton(Paths.PREVIOUS_BTN0, Paths.PREVIOUS_BTN1,
                                       objectName="Previous", clicked=self.previousSong)
        self.previous.setFixedSize(50, 50)

        self.next.setEnabled(False)
        self.previous.setEnabled(False)

        self.progress = Slider(QtCore.Qt.Horizontal)
        self.progress.valueChanged.connect(self.setMusicPosition)
        self.progress.setEnabled(False)

        self.progress_lbl = QtWidgets.QLabel("No Music")
        self.progress_lbl.setWordWrap(True)

        self._duration = f"00:00:00"
        self._formatted_duration = f"00:00:00"

        self.player = QtMultimedia.QMediaPlayer()
        self.player.positionChanged.connect(self.changeSliderPos)
        self.player.mediaStatusChanged.connect(self.mediaStatusChanged)
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
        grid_layout.addWidget(self.loop_btn, 2, 0, 1, 3)

        grid_layout.addWidget(self.previous, 3, 0, alignment=QtCore.Qt.AlignTop)
        grid_layout.addWidget(self.play_pause_btn, 3, 1, alignment=QtCore.Qt.AlignTop)
        grid_layout.addWidget(self.next, 3, 2, alignment=QtCore.Qt.AlignTop)
        grid_layout.addWidget(self.progress, 4, 0, 1, 3, alignment=QtCore.Qt.AlignTop)
        grid_layout.addWidget(self.progress_lbl, 5, 0, 1, 3, alignment=QtCore.Qt.AlignHCenter)
        grid_layout.setRowStretch(6, 2)
        grid_layout.addWidget(self.volume_slider, 7, 0, 1, 2, alignment=QtCore.Qt.AlignHCenter)
        grid_layout.addWidget(self.volume_indicator, 7, 3, 1, 1, alignment=QtCore.Qt.AlignHCenter)

        grid_layout.setRowStretch(8, 1)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        super(CurrentlyPlaying, self).resizeEvent(event)
        self.thumb_nail.setFixedHeight(self.thumb_nail.width())

    def loop(self, enableloop):
        self._loop = enableloop

    def autoPlayNext(self, autoPlay: bool):
        self._autoPlay = autoPlay

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
            self.volume_indicator.setPixmap(QtGui.QPixmap(Paths.MUTED))

        else:
            self.setVolume(self.volume_slider.value())

    def load_file(self):
        self.play_pause_btn.setEnabled(True)

        if not self.play_list.islast():
            self.next.setEnabled(True)

        if not self.play_list.isfirst():
            self.previous.setEnabled(True)

        self.progress.setEnabled(True)

        url = QtCore.QUrl.fromLocalFile(self.current_file)
        self.content = QtMultimedia.QMediaContent(url)
        self.player.setMedia(self.content)

        self._media_ended = False

    def mediaStatusChanged(self, status):
        print("Status: ", status)

        if status in [QtMultimedia.QMediaPlayer.InvalidMedia, QtMultimedia.QMediaPlayer.LoadingMedia,
                      QtMultimedia.QMediaPlayer.NoMedia]:
            self.progress_lbl.setText("Not Playable")
            self.play_pause_btn.setEnabled(False)
            self.progress.setEnabled(False)
            self.pause()

            if status in [QtMultimedia.QMediaPlayer.InvalidMedia, QtMultimedia.QMediaPlayer.NoMedia] \
                    and self._autoPlay:
                self.nextSong()

        elif status == QtMultimedia.QMediaPlayer.BufferedMedia and not self._media_ended:
            self.play_pause_btn.setEnabled(True)
            self.progress.setEnabled(True)
            self.play()

        if status == QtMultimedia.QMediaPlayer.EndOfMedia:
            self.pause()
            print("END OF MEDIA: ")
            if self._loop:
                self.setMusicPosition(0)
                self._play()
                return

            if self._autoPlay and not self.play_list.islast():
                self.nextSong()
                return

            # self.player.setMedia(QtMultimedia.QMediaContent())
            self._media_ended = True

    def setProgressLabel(self, value):

        duration = QtCore.QDateTime.fromTime_t(value / 1000).toUTC().toString("hh:mm:ss")
        self.progress_lbl.setText(f"{duration}/{self._formatted_duration}")

    def changeSliderPos(self, value):

        self.progress.blockSignals(True)
        self.progress.setSliderPosition(value)
        self.progress.blockSignals(False)

        self.setProgressLabel(value)

    def setMusicPosition(self, value):
        self.player.setPosition(value)

        if self._playing:
            self.player.play()

        self.setProgressLabel(value)

    def setDuration(self, duration):
        self._duration = duration

        self._formatted_duration = QtCore.QDateTime.fromTime_t(duration / 1000).toUTC().toString("hh:mm:ss")
        self.progress.setRange(0, duration)
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
        if self.play_list.isfirst():
            self.previous.setEnabled(False)

        else:
            self.previous.setEnabled(True)

        if self.play_list.islast():
            self.next.setEnabled(False)

        else:
            self.next.setEnabled(True)

    def nextSong(self):

        music_obj = self.play_list.next()

        if music_obj is not None:
            self._setCurrentMusicObj(music_obj)
            self.play()

        if self.play_list.islast():
            self.next.setEnabled(False)

    def previousSong(self):
        music_obj = self.play_list.previous()

        if music_obj is not None:
            self._setCurrentMusicObj(music_obj)
            self.play()

        if self.play_list.isfirst():
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


class CircularButton(QtWidgets.QPushButton):

    def __init__(self, default_image: QtGui.QPixmap, hover_image: QtGui.QPixmap, *args, **kwargs):
        super(CircularButton, self).__init__(*args, **kwargs)
        self._default_image = QtGui.QIcon(default_image)
        self._hover_image = QtGui.QIcon(hover_image)
        self.setIcon(self._default_image)
        self.setIconSize(QtCore.QSize(30, 30))

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        if self.isEnabled():
            self.setIcon(self._hover_image)

        super(CircularButton, self).enterEvent(a0)

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        self.setIcon(self._default_image)
        super(CircularButton, self).leaveEvent(a0)
