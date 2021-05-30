import Paths
from PyQt5 import QtWidgets, QtCore, QtGui
from Tiles.Tile import Tile
from CustomWidgets.EditableLabel import EditableLabel
from CustomWidgets.ScrollArea import ScrollView


class CollectionTile(Tile):

    def __init__(self, collection_name, *args, **kwargs):
        super(CollectionTile, self).__init__(*args, **kwargs)

        self._collection_name = collection_name

        self.setLayout(QtWidgets.QVBoxLayout())

        self.thumb_nail = QtWidgets.QLabel()
        self.thumb_nail.setScaledContents(True)

        self.scroll_view = CollectionTileScrollView()
        self.scroll_view.hide()

        widget = QtWidgets.QWidget()
        widget.setLayout(QtWidgets.QVBoxLayout())

        self.btns = QtWidgets.QWidget()
        self.btns.setLayout(QtWidgets.QHBoxLayout())
        self.btns.hide()

        delete_collection_btn = QtWidgets.QPushButton("Delete Collection")
        play_btn = QtWidgets.QPushButton("play")
        collection_label = EditableLabel(collection_name)
        collection_label.textChanged.connect(self.setCollectionName)

        self.btns.layout().addWidget(delete_collection_btn)
        self.btns.layout().addWidget(play_btn)


        widget.layout().addWidget(self.btns)
        # widget.layout().addWidget(play_btn, 0, 1)
        widget.layout().addWidget(collection_label)

        self.layout().addWidget(self.thumb_nail)
        self.layout().addWidget(widget)

        self._collection_children = set()

    def setThumbNail(self, thumb_nail):
        pass

    def setCollectionName(self, collection_name):
        self._collection_name = collection_name

    def addToCollection(self, innerTile):
        self._collection_children.add(innerTile)
        self.reload()

    def removeFromCollection(self, innerTile):
        self._collection_children.remove(innerTile)
        self.reload()

    def reload(self):
        self.scroll_view.removeTileParent()
        self.scroll_view.deleteAll()

        for tile in self._collection_children:
            self.scroll_view.addWidget(tile)

    def pause(self):
        pass

    def play(self):
        pass

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.scroll_view.show()

    def getCollectionName(self):
        return self._collection_name


class CollectionInnerTile(Tile):

    def __init__(self, music_object, *args, **kwargs):
        super(CollectionInnerTile, self).__init__(*args, **kwargs)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.parent = music_object
        self.parent.addChild(self)

        self.thumb_nail = QtWidgets.QLabel()
        self.thumb_nail.setScaledContents(True)
        self.thumb_nail.setPixmap(self.parent.getThumbnail())

        self.title = QtWidgets.QLabel(self.parent.getTitle())

        btns = QtWidgets.QButtonGroup(self)

        self.btns = QtWidgets.QWidget()

        self.play_btn = QtWidgets.QPushButton(objectName="PlayButton")
        self.play_btn.setIcon(QtGui.QIcon(Paths.PLAY))

        self.delete_btn = QtWidgets.QPushButton(objectName="Delete")
        self.delete_btn.setToolTip("remove from delete")
        self.delete_btn.setIcon(QtGui.QIcon(Paths.DELETE_BIN))  # todo: add a delete icon

        if self.parent.isPlaying():
            self.update_play()

        btns.addButton(self.play_btn)
        btns.addButton(self.delete_btn)
        btns.buttonClicked.connect(self.clicked)

        self.btns = QtWidgets.QWidget()
        self.btns.setLayout(QtWidgets.QHBoxLayout())

        self.btns.layout().addWidget(self.delete_btn, alignment=QtCore.Qt.AlignBottom)
        self.btns.layout().addWidget(self.play_btn, alignment=QtCore.Qt.AlignBottom)

        self.blur_effect = QtWidgets.QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(2)

        self.shadow_effect = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(5)
        self.shadow_effect.setOffset(3, 3)
        self.btns.setGraphicsEffect(self.shadow_effect)

        self.thumb_nail.setGraphicsEffect(self.blur_effect)
        self.blur_effect.setEnabled(False)

        self.layout().addWidget(self.thumb_nail)
        self.layout().addWidget(self.title)

        self.layout().addWidget(self.btns)

    def update_play(self):
        self.play_btn.setIcon(QtGui.QIcon(Paths.PAUSE))

    def update_pause(self):
        self.play_btn.setIcon(QtGui.QIcon(Paths.PLAY))

    def pause(self):
        self.update_pause()
        self.play_btn.setToolTip("Play")
        self.parent.clicked(self.play_btn)

    def play(self):
        self.update_play()
        self.play_btn.setToolTip("Pause")
        self.parent.clicked(self.play_btn)

    def clicked(self, btn):

        if btn == self.play_btn:
            if self.parent.isPlaying():
                self.pause()

            else:
                self.play()

        elif btn == self.delete_btn:
            self.parent.clicked(btn)

    def deleteLater(self) -> None:
        self.parent.removeChild(self)
        super(CollectionInnerTile, self).deleteLater()


class CollectionTileScrollView(ScrollView):

    def addTile(self, obj: CollectionTile):
        tile = CollectionTile(obj, (250, 250))
        self.addWidget(tile)

    def addWidget(self, widget):
        self.grid_layout.addWidget(widget, self._row, self._column)
        if self._column == 3:
            self._row += 1
            self._column = 0

        else:
            self._column += 1

    def removeTileParent(self):
        for x in range(self.grid_layout.count()):
            searchTile = self.grid_layout.itemAt(x).widget()
            searchTile.deleteLater()