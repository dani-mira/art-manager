import sys
import configparser

from classes.window import App, TabWrapper

import PyQt6.QtWidgets as QtWid

if __name__ == '__main__':

    # ### Initialisation

    app = App(sys.argv)

    win = app.add_window("mainWindow",
                         title="Art Manager")

    # tab handling

    tabs = TabWrapper(win)

    tabs.add_tab("Queue")
    tabs.add_tab("Clients")
    tabs.add_tab("Gallery")

    win.add_widget(tabs,
                   row=0,
                   column=0)

    app.run()
