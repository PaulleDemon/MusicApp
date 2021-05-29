import Paths
from PyQt5 import QtWidgets, QtCore, QtGui
from Tiles.Tile import Tile
from CustomWidgets.EditableLabel import EditableLabel


class CollectionTile(Tile):

    def __init__(self, collection_name, *args, **kwargs):
        super(CollectionTile, self).__init__(*args, **kwargs)

        self._collection_name = collection_name

        self.setLayout(QtWidgets.QVBoxLayout())

        self.thumb_nail = QtWidgets.QLabel()
        self.thumb_nail.setScaledContents(True)

        widget = QtWidgets.QWidget()
        widget.setLayout(QtWidgets.QGridLayout())

        delete_collection_btn = QtWidgets.QPushButton("Delete Collection")
        play_btn = QtWidgets.QPushButton("play")
        collection_label = EditableLabel()
        collection_label.textChanged.connect(self.setCollectionName)

        widget.layout().addWidget(delete_collection_btn, 0, 0)
        widget.layout().addWidget(play_btn, 0, 1)
        widget.layout().addWidget(play_btn, 1, 0, 1, 2)

        self.layout().addWidget(self.thumb_nail)
        self.layout().addWidget(widget)

    def setThumbNail(self, thumb_nail):
        pass

    def setCollectionName(self, collection_name):
        self._collection_name = collection_name

    def pause(self):
        pass

    def play(self):
        pass


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

        self.play_btn = QtWidgets.QPushButton(objectName="PlayButton")
        self.play_btn.setIcon(QtGui.QIcon(Paths.PLAY))

        self.delete_btn = QtWidgets.QPushButton(objectName="Delete")
        self.delete_btn.setToolTip("remove from delete")
        self.delete_btn.setIcon(QtGui.QIcon(Paths.DELETE))  # todo: add a delete icon

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


# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#
#     widget = QtWidgets.QWidget()
#     widget.setLayout(QtWidgets.QVBoxLayout())
#     widget.layout().addWidget(CollectionTile("Simple"))
#     widget.show()
#
#     sys.exit(app.exec_())