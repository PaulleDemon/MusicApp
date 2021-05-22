from PyQt5 import QtCore

import CustomWidgets.CurrentlyPlayingWidget
from CustomWidgets.Tile import MusicTile


class Notifier:

    # play = QtCore.pyqtSignal(bool)

    def __init__(self):
        self._playing = False

        self._current_playing_tile = None
        self._player = None

    def loadObject(self, obj: MusicTile):

        if self._current_playing_tile == obj:
            self.play_pause()
            return

        if self._current_playing_tile:
            try:
                self._current_playing_tile.pause()

            except NameError:
                raise NotImplementedError("Pause must be implemented")

        self._current_playing_tile = obj
        self._player.setThumbNail(obj.getThumbnail())
        self._player.setTitle(obj.getTitle())
        self._player.setCurrentPath(obj.getFile())
        self._player.load_file()

    def setPlayer(self, player: CustomWidgets.CurrentlyPlayingWidget.CurrentlyPlaying):
        self._player = player
        self._player.playing.connect(self._checkPlayerPlayPause)

    def _checkPlayerPlayPause(self, playing):
        if playing:
            self.play()

        else:
            self.pause()

    def play(self):
        self._current_playing_tile.play()
        self._playing = True
        # self._player.play()

    def pause(self):
        self._current_playing_tile.pause()
        self._playing = False
        # self._player.pause()

    def play_pause(self):

        self._playing = not self._playing

        if self._playing:
            self.play()
            self._player.play()


        else:
            self.pause()
            self._player.pause()