class PlayList:

    _playList = []
    _current = 0

    def __init__(self, start: int = 0):
        self._current = start

    def set_playlist(self, lst: list):
        PlayList._playList = lst

    def add_to_playlist(self, music_obj):
        PlayList._playList.append(music_obj)

    def clear(self):
        PlayList._playList = []

    def remove_from_playlist(self, music_obj):
        PlayList._playList.remove(music_obj)

    def remove_item_at(self, index: int):
        PlayList._playList.pop(index)

    def next(self):

        self._current += 1

        if self._current == len(PlayList._playList):
            self._current -= 1
            return None

        print("current: ", self._current, len(PlayList._playList), PlayList._playList)

        return PlayList._playList[self._current]

    def previous(self):

        self._current -= 1

        if self._current == -1:
            self._current = 0
            return None

        print("CURRENT PREVIOUS: ", self._current)

        return PlayList._playList[self._current]

    def islast(self):
        return self._current == len(PlayList._playList) -1

    def isfirst(self):
        return  self._current == 0

    def current(self):
        return PlayList._playList[self._current]

    def current_index(self):
        return self._current

    def getIndex(self, music_obj):
        return PlayList._playList.index(music_obj)

    def setCurrentIndex(self, index):
        self._current = index

    def playList(self):
        return PlayList._playList