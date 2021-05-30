import CustomWidgets.CurrentlyPlayingWidget
from Tiles.Music_FavouritesTile import MusicTile

from PyQt5 import QtWidgets, QtCore


# todo: add to collection feature
class Notifier:

    _current_playing_tile = None

    def __init__(self):
        self._playing = False

        self._current_playing_tile = None
        self._player = None
        self._favourite_tab = None
        self._collection_tab = None

    def setFavouriteTab(self, fav):
        self._favourite_tab = fav

    def markFavourite(self, obj):
        _, favourite, _ = obj.properties()

        if favourite:
            self._favourite_tab.addTile(obj)

        else:
            self._favourite_tab.removeTile(obj)

    def enableAutoPlay(self, enable=False):
        self._player.autoPlayNext(enable)

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
        self._player.setPlaylistIndex(self._current_playing_tile)
        self._player.load_file()

    def setCurrentTile(self, obj):
        self._current_playing_tile.pause()
        self._current_playing_tile = obj
        self._playing = self._player.isPlaying()

        if self._playing:
            self.play()

        else:
            self.pause()

    def setPlayer(self, player: CustomWidgets.CurrentlyPlayingWidget.CurrentlyPlaying):
        self._player = player
        self._player.playing.connect(self._checkPlayerPlayPause)
        self._player.current_tile_changed.connect(self.setCurrentTile)

    def _checkPlayerPlayPause(self, playing):
        if playing:
            self.play()

        else:
            self.pause()

    def play(self):
        self._current_playing_tile.play()
        self._playing = True

    def pause(self):
        self._current_playing_tile.pause()
        self._playing = False

    def play_pause(self):

        self._playing = not self._playing

        if self._playing:
            self.play()
            self._player.play()

        else:
            self.pause()
            self._player.pause()

    def setCollectionTab(self, tab):
        self._collection_tab = tab

    def addToCollection(self, obj):
        print(obj)
        new_dialog = CollectionDialog()
        new_dialog.addItems(self._collection_tab.getCollections())
        new_dialog.collection_edit.setFocus()
        if new_dialog.exec_():
            collection_name = new_dialog.getCollectionName()
            print(collection_name)
            print(self._collection_tab)
            self._collection_tab.addTile(obj, collection_name)


class CollectionDialog(QtWidgets.QDialog):

    def __init__(self, *args, **kwargs):
        super(CollectionDialog, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.collection_edit = QtWidgets.QLineEdit()
        self.collection_edit.setMaximumHeight(30)
        self.collection_edit.textChanged.connect(self.textChange)
        self.collection_edit.returnPressed.connect(self.confirm)
        self.collection_edit.setPlaceholderText("Collection name")
        self.collection_edit.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.err_lbl = QtWidgets.QLabel('', alignment=QtCore.Qt.AlignCenter)
        self.err_lbl.hide()

        self.collection_list_view = QtWidgets.QListWidget()
        self.collection_list_view.itemDoubleClicked.connect(self.itemSelected)

        self.layout().addWidget(self.collection_edit)
        self.layout().addWidget(self.err_lbl)
        self.layout().addWidget(self.collection_list_view)

        self._items = []
        self._selected_item = None

    def addItems(self, items: list):
        print(items)
        self.collection_list_view.addItems(items)
        self._items = items

    def textChange(self, text):

        if text == "":
            self.collection_list_view.addItems(self._items)

        self.collection_list_view.clear()

        for collection in self._items:
            if collection.startswith(text):
                self.collection_list_view.addItem(collection)

    def itemSelected(self, item: QtWidgets.QListWidgetItem):
        self._selected_item = item.text()
        self.accept()

    def confirm(self):

        self.err_lbl.show()
        if len(self.collection_edit.text()) < 5:
            self.err_lbl.setText("Must contain at-least 5 characters")
            return

        if len(self.collection_edit.text()) > 30:
            self.err_lbl.setText("Must contain max 30 characters")
            return

        if self.collection_edit.text() in self._items:
            self.err_lbl.setText(f"This Collection already exists. "
                                 f"Please double-click on the collection to add to the collection")
            return

        self.accept()

    def getCollectionName(self):
        return self._selected_item if self._selected_item is not None else self.collection_edit.text()
