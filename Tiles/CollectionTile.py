import Paths
from PyQt5 import QtWidgets, QtCore, QtGui


from Tiles.Tile import Tile
from CustomWidgets.EditableLabel import EditableLabel
from CustomWidgets.ScrollArea import ScrollView


class CollectionTile(Tile):

    playing = QtCore.pyqtSignal()

    def __init__(self, collection_name, *args, **kwargs):
        super(CollectionTile, self).__init__(*args, **kwargs)

        self.setStyleSheet('background-color: red;')

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

        self.blur_effect = QtWidgets.QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(2)

        delete_collection_btn = QtWidgets.QPushButton("Collection", clicked=self.deleteLater)
        self.play_btn = QtWidgets.QPushButton(icon=QtGui.QIcon(Paths.PLAY), clicked=self.playCollection)

        self._playing = False

        collection_label = EditableLabel(collection_name, alignment=QtCore.Qt.AlignCenter)
        collection_label.textChanged.connect(self.setCollectionName)

        self.btns.layout().addWidget(delete_collection_btn)
        self.btns.layout().addWidget(self.play_btn)

        widget.layout().addWidget(self.btns)
        widget.layout().addWidget(collection_label)

        self.layout().addWidget(self.thumb_nail)
        self.layout().addWidget(widget)

        self._play_list = []

        self._collection_children = set()

        self._thumbnail_delay = 2500
        self._thumb_nail_index = 0
        # self.updateThumbNail()

    def setThumbNail(self, thumb_nail):
        self.thumb_nail.setPixmap(thumb_nail)

    def setCollectionName(self, collection_name):
        self._collection_name = collection_name

    def addToCollection(self, obj):  # provide a music object

        self._collection_children.add(obj)
        self._play_list.append(obj)
        self.reload()

    def removeFromCollection(self, obj):

        widgets = self.scroll_view.getWidgets()
        for x in widgets:
            if x.musicObj == obj:
                x.deleteLater()
                break

        self._collection_children.remove(obj)
        self._play_list.remove(obj)
        self.reload()

    def updateThumbNail(self):  # todo: complete scrolling animation

        if not self._playing:

            if self._thumb_nail_index == len(self._collection_children):
                self._thumb_nail_index = 0

            if self._collection_children:
                thumbnail = list(self._collection_children)[self._thumb_nail_index].getThumbnail()
                x, y = 0, 0
                new_thumbnail = thumbnail

                def updateThumbnailAnimation(_thumbnail):
                    nonlocal x, y, new_thumbnail
                    new_thumbnail = _thumbnail.scroll(x, y, _thumbnail.rect())
                    new_thumbnail = new_thumbnail.s
                    x += 5
                    y += 5

                    self.setThumbNail(_thumbnail)

                    if not new_thumbnail.size() == thumbnail.size():
                        QtCore.QTimer.singleShot(20, updateThumbnailAnimation)

                updateThumbnailAnimation(thumbnail)

            self._thumb_nail_index += 1

        QtCore.QTimer.singleShot(self._thumbnail_delay, self.updateThumbNail)

    def reload(self):

        self.scroll_view.children()

        self.scroll_view.removeTileParent()
        self.scroll_view.deleteAll()

        for obj in self._collection_children:
            collection_inner_tile = CollectionInnerTile(obj, self)
            self.scroll_view.addWidget(collection_inner_tile)

    def pause(self):
        # self.playing.emit()
        self.play_btn.setIcon(QtGui.QIcon(Paths.PLAY))

    def play(self):
        # self.playing.emit()
        self.play_btn.setIcon(QtGui.QIcon(Paths.PAUSE))

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.scroll_view.show()
        super(CollectionTile, self).mousePressEvent(a0)

    def getCollectionName(self):
        return self._collection_name

    def playCollection(self):
        pass

    def deleteLater(self) -> None:

        for x in self._collection_children:
            x.clicked(self.sender())

        super(CollectionTile, self).deleteLater()


class CollectionInnerTile(Tile):  # This is tile inside the Collections

    def __init__(self, music_object, collection_object: CollectionTile, *args, **kwargs):
        super(CollectionInnerTile, self).__init__(*args, **kwargs)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.parent = music_object
        self.parent.addChild(self)

        self.collection_object = collection_object

        self.thumb_nail = QtWidgets.QLabel()
        self.thumb_nail.setScaledContents(True)
        self.thumb_nail.setPixmap(self.parent.getThumbnail())

        self.title = QtWidgets.QLabel(self.parent.getTitle())

        btns = QtWidgets.QButtonGroup(self)

        self.btns = QtWidgets.QWidget()

        self.play_btn = QtWidgets.QPushButton(objectName="PlayButton")
        self.play_btn.setIcon(QtGui.QIcon(Paths.PLAY))

        self.delete_btn = QtWidgets.QPushButton(objectName="Collection")
        self.delete_btn.setToolTip("remove from Collection")
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

        self.btns.hide()

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
        self.collection_object.play()

    def update_pause(self):
        self.play_btn.setIcon(QtGui.QIcon(Paths.PLAY))
        self.collection_object.pause()

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

    def checkFavourite(self):  # necessary just use this
        pass

    def musicObj(self):
        return self.parent


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