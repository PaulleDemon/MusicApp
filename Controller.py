from PlayList import PlayList
import CustomWidgets.CurrentlyPlayingWidget
from Tiles.Music_FavouritesTile import MusicTile

from PyQt5 import QtWidgets, QtCore


class Notifier:

    # This class is responsible for interaction between class it passes information from one class to another.
    # All the tabs(MyMusic, Favourite, Collection) and CurrentlyPlayingWidget must be registered here. Once it's
    # registered it controls which, how each object interacts with currentlyPlayingWidget

    _current_playing_tile = None
    _current_playing_collection = None

    with open(r'Resources/DarkTheme.qss') as style:
        _style = style.read()

    def __init__(self):
        self._playing = False

        self._play_list = PlayList()
        self._current_playing_tile = None
        self._current_playing_collection = None
        self._player = None
        self._music_tab = None
        self._favourite_tab = None
        self._collection_tab = None
        self._statics_tab = None

    def enableAutoPlay(self, enable=False):  # enable auto next
        self._player.autoPlayNext(enable)

    def setMusicTab(self, tab): # register music tab
        self._music_tab = tab
        self._music_tab.play.connect(self.loadMusicPlayList)
        self._music_tab.addFavourite.connect(self.markFavourite)
        self._music_tab.addToCollection.connect(self.addToCollection)
        self._music_tab.playlist_added.connect(self.reloadMyMusicPlaylist)

    def setFavouriteTab(self, fav):  # register favourite's tab
        self._favourite_tab = fav

    def setStatisticsTab(self, stat):
        self._statics_tab = stat

    def updateStatisticsChart(self, music_count):
        print("updating...")
        self._statics_tab.plotAxis(music_count)

    def setCollectionTab(self, tab):  # registers the collection tab
        self._collection_tab = tab
        self._collection_tab.playing.connect(self.loadCollectionPlayList)
        self._collection_tab.reloadPlayList.connect(self.reloadCollectionPlayList)

    def setPlayer(self, player: CustomWidgets.CurrentlyPlayingWidget.CurrentlyPlaying):
        # registers the CurrentlyPlayingWidget
        self._player = player
        self._player.playing.connect(self._checkPlayerPlayPause)
        self._player.current_tile_changed.connect(self.setCurrentTile)

    def setCurrentTile(self, obj):  # This will set current music object that is to be played
        self._current_playing_tile.pause()
        self._current_playing_tile = obj
        self._playing = self._player.isPlaying()

        self.updateStatisticsChart(self._player.musicCount())

        if self._playing:
            self.play()

        else:
            self.pause()

    def markFavourite(self, obj):  # marks a music object as favourite and adds to Favourites tab
        _, favourite, _ = obj.properties()

        if favourite:
            self._favourite_tab.addTile(obj)

        else:
            self._favourite_tab.removeTile(obj)

    def loadCurrentTile(self, obj):  # loads current playing object and sets the thumbnail of currentlyPlayingWidget
        self._current_playing_tile = obj
        self._player.setThumbNail(obj.getThumbnail())
        self._player.setTitle(obj.getTitle())
        self._player.setCurrentPath(obj.getFile())
        self._player.setPlaylistIndex(self._current_playing_tile)
        self._player.load_file()
        self.updateStatisticsChart(self._player.musicCount())

    def loadMusicPlayList(self, obj: MusicTile):  # loads musics from MyMusic tab to playlist

        if self._current_playing_tile == obj:
            self.play_pause()
            return

        if self._current_playing_tile:
            try:
                self._current_playing_tile.pause()

            except NameError:
                raise NotImplementedError("Pause must be implemented")

        self._play_list.clear()
        self._play_list.set_playlist(self._music_tab.playlist())
        self.loadCurrentTile(obj)

    def loadCollectionPlayList(self, collection):
        # loads music from collection.
        # Note only one playlist can be stored at an instance. When a new one is loaded old one is removed

        if self._current_playing_collection == collection:
            self.play_pause()
            return

        if self._current_playing_tile:
            try:
                self._current_playing_tile.pause()

            except NameError:
                raise NotImplementedError("Pause must be implemented")

        self._current_playing_collection = collection
        self._play_list.clear()
        self._play_list.set_playlist(self._collection_tab.playlist())
        self.loadCurrentTile(self._play_list.playList()[0])

    def reloadMyMusicPlaylist(self):
        # reloads playlist this is done when new object is added in the music tab
        if self._music_tab.playlist() and self._current_playing_tile:
            self._play_list.clear()
            self._play_list.set_playlist(self._music_tab.playlist())
            self._player.setPlaylistIndex(self._current_playing_tile)

    def reloadCollectionPlayList(self):
        # reloads playlist this is done when new object is added in the collection tab
        if self._collection_tab.playlist() and self._current_playing_tile:
            self._play_list.clear()
            self._play_list.set_playlist(self._collection_tab.playlist())
            self._player.setPlaylistIndex(self._current_playing_tile)

    def _checkPlayerPlayPause(self, playing): # checks player state
        if playing:
            self.play()

        else:
            self.pause()

    def play(self):  # plays music
        self._current_playing_tile.play()
        self._playing = True

    def pause(self): # pauses music
        self._current_playing_tile.pause()
        self._playing = False

    def play_pause(self): # if a music is being played stops it, else plays it

        self._playing = not self._playing
        if self._playing:
            self.play()
            self._player.play()

        else:
            self.pause()
            self._player.pause()

    def addToCollection(self, obj, addToCollection=True):
        # adds a music object to collection, if already in collection removes it

        if not addToCollection:
            self._collection_tab.removeTile(obj, obj.getCollectionName())
            return

        new_dialog = CollectionDialog()
        new_dialog.setStyleSheet(self._style)
        new_dialog.addItems(self._collection_tab.getCollections())
        new_dialog.collection_edit.setFocus()
        if new_dialog.exec_():
            collection_name = new_dialog.getCollectionName()
            self._collection_tab.addTile(obj, collection_name)
            obj.setCollectionName(collection_name)

        else:
            obj._collection = False


class CollectionDialog(QtWidgets.QDialog):  # This is a collection dialog that ask user to enter collection name

    def __init__(self, *args, **kwargs):
        super(CollectionDialog, self).__init__(*args, **kwargs)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Popup)
        self.setObjectName("CollectionDialog")

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
        # self.collection_list_view.itemDoubleClicked.connect(self.itemSelected)
        self.collection_list_view.itemActivated.connect(self.itemSelected)

        self.layout().addWidget(self.collection_edit)
        self.layout().addWidget(self.err_lbl)
        self.layout().addWidget(self.collection_list_view)

        self._items = []
        self._selected_item = None

    def addItems(self, items: list):
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
        if len(self.collection_edit.text()) < 3:
            self.err_lbl.setText("Must contain at-least 3 characters")
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
