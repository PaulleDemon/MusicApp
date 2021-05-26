from PyQt5 import QtWidgets, QtCore, QtGui


class Slider(QtWidgets.QSlider):
    clicked = QtCore.pyqtSignal(float)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        super(Slider, self).mousePressEvent(event)

        if event.button() == QtCore.Qt.LeftButton:
            val = self.pixelPosToRangeValue(event.pos())
            self.setValue(val)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
            super(Slider, self).mouseReleaseEvent(event)

            if event.button() == QtCore.Qt.LeftButton:
                val = self.pixelPosToRangeValue(event.pos())
                self.valueChanged.emit(val)


    def pixelPosToRangeValue(self, pos):
        opt = QtWidgets.QStyleOptionSlider()
        self.initStyleOption(opt)
        gr = self.style().subControlRect(QtWidgets.QStyle.CC_Slider, opt, QtWidgets.QStyle.SC_SliderGroove, self)
        sr = self.style().subControlRect(QtWidgets.QStyle.CC_Slider, opt, QtWidgets.QStyle.SC_SliderHandle, self)

        if self.orientation() == QtCore.Qt.Horizontal:
            sliderLength = sr.width()
            sliderMin = gr.x()
            sliderMax = gr.right() - sliderLength + 1
        else:
            sliderLength = sr.height()
            sliderMin = gr.y()
            sliderMax = gr.bottom() - sliderLength + 1;
        pr = pos - sr.center() + sr.topLeft()
        p = pr.x() if self.orientation() == QtCore.Qt.Horizontal else pr.y()
        return QtWidgets.QStyle.sliderValueFromPosition(self.minimum(), self.maximum(), p - sliderMin,
                                               sliderMax - sliderMin, opt.upsideDown)