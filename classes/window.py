from PyQt6.QtWidgets import QWidget, QApplication


class App(QApplication):

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


class MainWindow(QWidget):

    def __init__(self, parent: App, id, *, title="Default", size=(800, 600)):

        super().__init__()

        # by the nature of how PyQt works there can only be one QApp instance running!!
        # this is a crime against OOP

        self.__parent = parent  # NEVER SHOULD BE CHANGED

        self._id = id
        self.setObjectName(self._id)

        self._title = title
        self._size = size

        self.title = self._title
        self.size = self._size

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
