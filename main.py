import sys
from PyQt5 import QtWidgets
from MainWindow import MainWindow

# Date started: 15 may 2021
# Author: Paul
# Description: Music Player that can play songs from your local repository, You can add your songs to favourite, or
# create collections. The user can also check statistics to know the number of times a song was played


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    # win.showMaximized()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()