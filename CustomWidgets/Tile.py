import ntpath
import Paths

from io import BytesIO
from PyQt5 import QtWidgets, QtGui, QtCore
from PIL import Image
from tinytag import TinyTag


class Tile(QtWidgets.QWidget):

    def __init__(self, size: tuple = (100, 100),*args, **kwargs):
        super(Tile, self).__init__(*args, **kwargs)

        self.setObjectName("Tile")

        self._original_size = QtCore.QSize(*size)
        self.setMinimumSize(self._original_size)
        self.setMaximumSize(self._original_size.width()+50, self._original_size.height()+50)

        self.animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(150)

    def animate(self, expand):
        if expand:
            self.animation.setDirection(self.animation.Forward)
        else:
            self.animation.setDirection(self.animation.Backward)
        self.animation.start()

    def enterEvent(self, a0: QtCore.QEvent) -> None:
        super(Tile, self).enterEvent(a0)
        self.animate(True)
        self.btns.show()
        self.blur_effect.setEnabled(True)

    def leaveEvent(self, a0: QtCore.QEvent) -> None:
        super(Tile, self).leaveEvent(a0)
        self.animate(False)
        self.btns.hide()
        self.blur_effect.setEnabled(False)

    def updateAnimation(self):
        if not self.animation.state():
            center = self.geometry().center()
            start = QtCore.QRect(QtCore.QPoint(), self.minimumSize())
            start.moveCenter(center)
            self.animation.setStartValue(start)
            end = QtCore.QRect(QtCore.QPoint(), self.maximumSize())
            end.moveCenter(center)
            self.animation.setEndValue(end)

    def moveEvent(self, event):
        self.updateAnimation()

    def resizeEvent(self, event):
        self.updateAnimation()
        if not self.animation.state():
            rect = QtCore.QRect(QtCore.QPoint(),
                                self.maximumSize() if self.underMouse() else self.minimumSize())
            rect.moveCenter(self.geometry().center())
            self.setGeometry(rect)


class MusicTile(Tile):

    play = QtCore.pyqtSignal(bool, str, QtGui.QPixmap, object) # path
    addFavourite = QtCore.pyqtSignal(bool)
    addToCollection = QtCore.pyqtSignal(bool)

    def __init__(self, music: TinyTag, file_path="", *args, **kwargs):
        super(MusicTile, self).__init__(*args, **kwargs)

        def pil2pixmap(im):

            if im.mode == "RGB":
                r, g, b = im.split()
                im = Image.merge("RGB", (b, g, r))
            elif im.mode == "RGBA":
                r, g, b, a = im.split()
                im = Image.merge("RGBA", (b, g, r, a))
            elif im.mode == "L":
                im = im.convert("RGBA")
            # Bild in RGBA konvertieren, falls nicht bereits passiert
            im2 = im.convert("RGBA")
            data = im2.tobytes("raw", "RGBA")
            qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
            pixmap = QtGui.QPixmap.fromImage(qim)
            return pixmap

        self.music = music

        image = music.get_image()

        title = music.title

        self.file_path = file_path

        if title and title.isspace():
            title = ""

        if not title:
            title = ntpath.basename(file_path)

        if not image:
            image = Image.open(Paths.UNKNOWN_MUSIC)

        else:
            image = Image.open(BytesIO(image))

        image = pil2pixmap(image)

        self.setLayout(QtWidgets.QVBoxLayout())

        self.setObjectName("MusicTile")

        self.label = QtWidgets.QLabel()
        self.label.setPixmap(image)
        self.label.setScaledContents(True)

        self.music_title = QtWidgets.QLabel(text=title)

        self.btns = QtWidgets.QWidget()
        self.btns.setLayout(QtWidgets.QHBoxLayout())

        btns = QtWidgets.QButtonGroup(self)

        self._playing = False
        self._favourite = False
        self._collection = None

        self.play_btn = QtWidgets.QPushButton(objectName="PlayButton")
        self.play_btn.setToolTip("Play")
        self.play_btn.setIcon(QtGui.QIcon(Paths.PLAY))

        self.favourite = QtWidgets.QPushButton(objectName="favourite")
        self.favourite.setToolTip("Mark Favourite")
        self.favourite.setIcon(QtGui.QIcon(Paths.STAR_UNFILLED))

        self.collection = QtWidgets.QPushButton(objectName="Collection")
        self.collection.setToolTip("Add to Collection")
        self.collection.setIcon(QtGui.QIcon(Paths.COLLECTION))

        btns.addButton(self.play_btn)
        btns.addButton(self.favourite)
        btns.addButton(self.collection)
        btns.buttonClicked.connect(self.clicked)

        self.btns.layout().addWidget(self.collection, alignment=QtCore.Qt.AlignBottom)
        self.btns.layout().addWidget(self.favourite, alignment=QtCore.Qt.AlignBottom)
        self.btns.layout().addWidget(self.play_btn, alignment=QtCore.Qt.AlignBottom)

        self.btns.hide()

        self.blur_effect = QtWidgets.QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(2)

        self.shadow_effect = QtWidgets.QGraphicsDropShadowEffect()
        self.shadow_effect.setBlurRadius(5)
        self.shadow_effect.setOffset(3, 3)
        self.btns.setGraphicsEffect(self.shadow_effect)

        self.label.setGraphicsEffect(self.blur_effect)
        self.blur_effect.setEnabled(False)

        self.layout().addWidget(self.label)
        self.layout().addWidget(self.btns)
        self.layout().addWidget(self.music_title)

    def getMusic(self) -> TinyTag:
        return self.music

    def getFile(self):
        return self.file_path

    def getThumbnail(self):
        return self.label.pixmap()

    def properties(self):
        return [self._playing, self._favourite, self._collection]

    def pause(self):
        self.play_btn.setIcon(QtGui.QIcon(Paths.PAUSE))

    def playMusic(self):
        self.play_btn.setIcon(QtGui.QIcon(Paths.PLAY))

    def clicked(self, btn):

        if btn == self.play_btn:
            self._playing = not self._playing

            if self._playing:
                self.play_btn.setIcon(QtGui.QIcon(Paths.PAUSE))

            else:
                self.play_btn.setIcon(QtGui.QIcon(Paths.PLAY))

            self.play.emit(self._playing, self.file_path, self.getThumbnail(), self)

        elif btn == self.favourite:
            self._favourite = not self._favourite

            if self._favourite:
                self.favourite.setIcon(QtGui.QIcon(Paths.STAR_FILLED))

            else:
                self.favourite.setIcon(QtGui.QIcon(Paths.STAR_UNFILLED))

            self.addFavourite.emit(self._favourite)
