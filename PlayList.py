class PlayList:

    # stores the music objects of MusicTile class from Music_FavoritesTile.py in a list, so that it
    # can be played in a sequence

    _playList = []
    _current = 0

    def __init__(self, start: int = 0):
        self._current = start

    def set_playlist(self, lst: list):  # replaces the playlist with the given list
        PlayList._playList = lst

    def add_to_playlist(self, music_obj): # adds to playlist
        PlayList._playList.append(music_obj)

    def clear(self):  # clears all the object from playlist
        PlayList._playList = []

    def remove_from_playlist(self, music_obj):  # removes the specified object from playlist
        PlayList._playList.remove(music_obj)

    def remove_item_at(self, index: int):  # removes item at specific index
        PlayList._playList.pop(index)

    def next(self):  # returns the next song

        self._current += 1

        if self._current == len(PlayList._playList):
            self._current -= 1
            return None

        return PlayList._playList[self._current]

    def previous(self):  # returns the previous song

        self._current -= 1

        if self._current == -1:
            self._current = 0
            return None

        return PlayList._playList[self._current]

    def islast(self):  # returns if the current playing song is last in playlist
        return self._current == len(PlayList._playList) -1

    def isfirst(self): # returns if the current playing song is first in playlist
        return  self._current == 0

    def current(self):  # returns current music object
        return PlayList._playList[self._current]

    def current_index(self):  # returns current index
        return self._current

    def getIndex(self, music_obj):  # given a music object return its index in the list
        return PlayList._playList.index(music_obj)

    def setCurrentIndex(self, index):  # sets the index to a given index
        self._current = index

    def playList(self):  # returns the whole playlist
        return PlayList._playList