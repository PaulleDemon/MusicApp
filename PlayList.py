

class PlayList:

    _playList = []
    _current = 0

    def __init__(self, start: int = 0):
        self._current = start

    def add_to_playlist(self, music_obj):
        self._playList.append(music_obj)
        print("YES")

    def clear(self):
        self._playList = []

    def remove_from_playlist(self, music_obj):
        self._playList.remove(music_obj)

    def remove_item_at(self, index: int):
        self._playList.pop(index)

    def next(self):
        self._current += 1

        if not self._current < len(self._playList):
            return None

        return self._playList[self._current]

    def previous(self):
        self._current -= 1

        if self._current < 0:
            return None

        return self._playList[self._current]

    def current(self):
        return self._playList[self._current]

    def current_index(self):
        return self._current

    def getIndex(self, music_obj):
        return self._playList.index(music_obj)

    def setCurrentIndex(self, index):
        self._current = index

    def playList(self):
        return self._playList