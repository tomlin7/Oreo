import tkinter as tk
from utils.data import *

class OreoIDE(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.oreomenu = None
        self.editor = None
        self.terminal = None
        self.statusbar = None

        # IDE config
        # ---
        self.title("Untitled - Oreo")
        self.wm_iconbitmap(icon)
        self.configure(background="#007acc", bd=0)
        # ---
        
        # Auto resizable components.
        # ---
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # ---

        try:
            if kwargs['oreomenu'] != None:
                self.editor = kwargs['oreomenu']
            if kwargs['editor'] != None:
                self.editor = kwargs['editor']
            if kwargs['terminal'] != None:
                self.terminal = kwargs['terminal']
            if kwargs['statusbar'] != None:
                self.statusbar = kwargs['statusbar']
        except KeyError:
            pass

    def add_oreomenu(self, oreomenu):
        self.oreomenu = oreomenu

    def add_editor(self, editor):
        self.editor = editor
    
    def add_terminal(self, terminal):
        self.terminal = terminal
    
    def add_statusbar(self, statusbar):
        self.statusbar = statusbar