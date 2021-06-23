from PyQt5 import QtWidgets, QtGui, QtCore
from CustomWidgets.CurrentlyPlayingWidget import CurrentlyPlaying


class TabWidget(QtWidgets.QWidget):

    def __init__(self, width=250, *args, **kwargs):
        super(TabWidget, self).__init__(*args, **kwargs)

        self._previousTab = None

        self.setObjectName("VerticalTab")

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.tabWidget = QtWidgets.QWidget()
        self.tabWidget.setMaximumWidth(width)
        self.tabWidget.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.tab_playing_holder = QtWidgets.QVBoxLayout(self.tabWidget)

        self.tab_Layout = QtWidgets.QVBoxLayout()
        currently_playing_layout = QtWidgets.QVBoxLayout()

        self.currently_playing = CurrentlyPlaying()
        currently_playing_layout.addWidget(self.currently_playing)

        self.tab_playing_holder.addLayout(self.tab_Layout)
        self.tab_playing_holder.addLayout(currently_playing_layout)

        self.widgetLayout = QtWidgets.QVBoxLayout()

        self.layout().addWidget(self.tabWidget)
        self.layout().addLayout(self.widgetLayout)

        self.button_group = QtWidgets.QButtonGroup()
        self.button_group.buttonClicked.connect(self.showTab)

        self.setFocusPolicy(QtCore.Qt.ClickFocus)

    def player_object(self):
        return self.currently_playing

    def musicCount(self):  # returns the count of musics played
        return self.currently_playing.musicCount()

    def setMusicCount(self, music_count: dict):
        self.currently_playing.setMusicCount(music_count)

    def volume(self):
        return self.currently_playing.volume()

    def setVolume(self, vol):
        self.currently_playing.setVolume(vol)

    def enterEvent(self, a0: QtCore.QEvent):
        super(TabWidget, self).enterEvent(a0)

        if not isinstance( QtWidgets.QApplication.focusWidget(), QtWidgets.QLineEdit):
            self.setFocus()

    def showTab(self, btn):

        if self._previousTab:
            index = self.tab_Layout.indexOf(self._previousTab)
            self.widgetLayout.itemAt(index).widget().hide()

        index = self.tab_Layout.indexOf(btn)
        self.widgetLayout.itemAt(index).widget().show()
        self._previousTab = btn

    def addTab(self, widget: QtWidgets.QWidget, text: str, icon=QtGui.QIcon()):
        tab = QtWidgets.QPushButton(icon, '\t'*4+text)
        tab.setMinimumHeight(40)

        tab.setIconSize(QtCore.QSize(35, 35))
        tab.setCheckable(True)


        self.button_group.addButton(tab)
        self.tab_Layout.addWidget(tab)
        self.widgetLayout.addWidget(widget)
        widget.hide()

        if not self.button_group.checkedButton():
            btn = self.tab_Layout.itemAt(0).widget()
            btn.setChecked(True)
            self.button_group.buttonClicked.emit(btn)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:

        if self.tabWidget.hasFocus():
            current_index = self.tab_Layout.indexOf(self.button_group.checkedButton())
            if event.angleDelta().y() < 120:

                current_index += 1

            else:
                current_index -= 1

            if 0 <= current_index < self.tab_Layout.count():
                btn = self.tab_Layout.itemAt(current_index).widget()
                btn.setChecked(True)
                self.button_group.buttonClicked.emit(btn)
