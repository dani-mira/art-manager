import PyQt6.QtWidgets as QtWid
from PyQt6.QtCore import Qt


class App(QtWid.QApplication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.windows = {}

    # ## window and widget manipulation methods

    def _update_id(self, old_id, new_id):

        # updates the id of the widget in the internal window list

        self.windows[new_id] = self.windows.pop(old_id)

        return new_id

    def add_window(self, id, *, title="Default", size=(800, 600)):

        # adds a window to the internal window list and initialises it

        self.windows[id] = MainWindow(self,
                                      id,
                                      title=title,
                                      size=size)

        return self.windows[id]

    # ## execution and wrapper routines

    def run(self, *, mode=None):

        # wrapper to customize the execution routine before letting PyQt handle the rest

        for id, window in self.windows.items():

            window.show()

            print(f"Loaded widget '{id}'")

        self.exec()


# ### Window handlers


class MainWindow(QtWid.QWidget):

    def __init__(self, parent: App, id, *, title="Default", size=(800, 600), layout=None):

        super().__init__()

        # by the nature of how PyQt works there can only be one QApp instance running!!
        # this is a crime against OOP

        self.__parent = parent  # NEVER SHOULD BE CHANGED

        if layout:
            self.layout = layout
        else:
            self.layout = QtWid.QGridLayout(self)

        self.setLayout(self.layout)

        self._id = id
        self.setObjectName(self._id)

        self._title = title
        self._size = size

        self.title = self._title
        self.size = self._size

    # ## static methods

    def add_widget(self, wg, *, row, column, alignment=Qt.AlignmentFlag(0)):
        # lets each widget wrapper decide how to initialise its subwidgets
        wg._add_widgets()

        self.layout.addWidget(wg, row, column, alignment)

    # ## Dynamic UI setting by simple dot notation access
    # i.e "window.title = 'Foo'" will directly alter the window title being displayed

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):

        # used exclusively to update the id
        # the setter for other attributes will simply initialise the UI or update it
        # but this setter also updates the id in the parent App window dictionary
        # thus it can't be used for initialising the window id
        # that's handled in App.set_window() and in MainWindow.__init__()

        old_value = self._id
        new_value = str(value)

        self._id = new_value
        self.setObjectName(new_value)

        # updates the id of the window in the windows dict from the parent App instance

        self.__parent._update_id(old_value, new_value)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title
        self.setWindowTitle(title)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size
        self.resize(*size)


# ### Tab handlers
# parent corresponds to the window these reside in, both QTabWidget and QWidget must take the main window as their parent

class TabWrapper(QtWid.QTabWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.__parent = parent

        self.subwidgets = {}

    def add_tab(self, name, *, layout=None):

        tab = Tab(self.__parent, name=name, layout=layout)
        self.subwidgets[name] = tab

        return tab

    # personalised method for adding the subwidgets to the tab
    def _add_widgets(self):

        for name, widget in self.subwidgets.items():
            self.addTab(widget, name)


class Tab(QtWid.QWidget):

    def __init__(self, parent, *, name, layout):
        super().__init__(parent)

        if layout:
            self.layout = layout
        else:
            self.layout = QtWid.QGridLayout(self)

        self.setLayout(self.layout)

        self.name = name

