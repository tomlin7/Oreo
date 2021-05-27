import os
import tkinter as tk

from utils.data import *
from utils.utilities import *
from utils.statusbar import StatusBar
from utils.oreoide import OreoIDE
from utils.oreoeditor import OreoEditor
from utils.oreomenu import OreoMenu
from utils.terminal import Terminal


if __name__ == "__main__":
    root = OreoIDE()
    center(root, width=1000, height=700)

    oreoeditor = OreoEditor(_root=root, background="#ffffff")
    root.add_editor(oreoeditor)

    oreomenu = OreoMenu(root, relief=tk.FLAT)
    root.add_oreomenu(oreomenu)

    terminal = Terminal(root, fira_code)
    terminal.pack(fill=tk.BOTH, expand=True)
    root.add_terminal(terminal)

    statusbar = StatusBar(root, bg="#007acc")
    statusbar.pack(fill=tk.BOTH, side=tk.BOTTOM)
    root.add_statusbar(statusbar)

    root.mainloop()
