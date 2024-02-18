import sys

from classes.window import App

if __name__ == '__main__':

    app = App(sys.argv)

    win = app.add_window("mainWindow",
                         title="Art Manager")

    app.run()
