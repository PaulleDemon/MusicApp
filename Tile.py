from PyQt5 import QtWidgets, QtGui, QtCore
from PIL import Image


class Tile(QtWidgets.QWidget):

    def __init__(self, image_path, title="music", size: tuple = (100, 100),*args, **kwargs):
        super(Tile, self).__init__(*args, **kwargs)

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

        self.setLayout(QtWidgets.QVBoxLayout())

        self.label = QtWidgets.QLabel()
        self.label.setScaledContents(True)
        self.label.setPixmap(pil2pixmap(image_path))

        self.music_title = QtWidgets.QLabel(text=title)

        self.btns = QtWidgets.QWidget()
        self.btns.setLayout(QtWidgets.QHBoxLayout())

        self.play_btn = QtWidgets.QPushButton(objectName="PlayButton")
        self.play_btn.setToolTip("Play")

        self.favourite = QtWidgets.QPushButton(objectName="favourite")
        self.favourite.setToolTip("Mark Favourite")

        self.collection = QtWidgets.QPushButton(objectName="Collection")
        self.collection.setToolTip("Add to Collection")

        self.btns.layout().addWidget(self.play_btn, alignment=QtCore.Qt.AlignBottom)
        self.btns.layout().addWidget(self.favourite, alignment=QtCore.Qt.AlignBottom)
        self.btns.layout().addWidget(self.collection, alignment=QtCore.Qt.AlignBottom)

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

        self._original_size = QtCore.QSize(*size)
        self.setMinimumSize(self._original_size)
        self.setMaximumSize(self._original_size.width()+25, self._original_size.height()+25)

    # def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
    #
    #     event.accept()
    #
    #     if event.size().width() > event.size().height():
    #         self.resize(event.size().height(), event.size().height())
    #
    #     else:
    #         self.resize(event.size().width(), event.size().width())

    def enterEvent(self, a0: QtCore.QEvent):

        self.btns.show()

        self.blur_effect.setEnabled(True)

        self.animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.animation.setStartValue(QtCore.QRect(self.geometry()))
        self.animation.setEndValue(QtCore.QRect(self.geometry().adjusted(-25, -25, 25, 25)))
        self.animation.setDuration(150)
        self.animation.start(QtCore.QPropertyAnimation.DeleteWhenStopped)

    def leaveEvent(self, a0: QtCore.QEvent):
        self.btns.hide()

        self.blur_effect.setEnabled(False)

        self.animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.animation.setStartValue(QtCore.QRect(self.geometry()))
        self.animation.setEndValue(QtCore.QRect(self.geometry().adjusted(25, 25, -25, -25)))
        self.animation.setDuration(150)
        self.animation.start(QtCore.QPropertyAnimation.DeleteWhenStopped)

