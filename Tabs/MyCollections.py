from PyQt5 import QtWidgets
from CustomWidgets import ScrollArea
from Tiles.CollectionTile import CollectionTile


class MyCollection(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(MyCollection, self).__init__(*args, **kwargs)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.view = CollectionScrollView()

        self.layout().addWidget(self.view)

    def addTile(self, obj, collection_name):
        # self.view.addTile(obj, collection_name)
        print("NAme1: ", collection_name, obj)
        self.view.addTile(collection_name)

    def removeTile(self, obj):
        self.view.removeWidget(obj)

    def getCollections(self):
        wid = self.view.getWidgets()
        print("Widgets: ", wid)
        return [x.getCollectionName() for x in wid]


class CollectionScrollView(ScrollArea.ScrollView):

    def __init__(self, *args):
        super(CollectionScrollView, self).__init__(*args)

    def addTile(self, name: str):
        print("Collection Name: ", name)
        tile = CollectionTile(name, (250, 250))
        self.addWidget(tile)

    def addWidget(self, widget):
        self.grid_layout.addWidget(widget, self._row, self._column)
        if self._column == 3:
            self._row += 1
            self._column = 0

        else:
            self._column += 1

    def removeWidget(self, obj):

        child = obj.getChildren().copy()
        print("Children: ", child)
        for x in child:
            print(x.parent.getTitle())
            if isinstance(x, CollectionTile):
                self.grid_layout.removeWidget(x)
                x.deleteLater()

        widgets = self.getWidgets()
        self.deleteAll()
        print(widgets)
        for widget in widgets:
            self.addTile(widget.parent)
            widget.parent.removeChild(widget)

        self.grid_layout.update()