import tkinter as tk
from utils.data import *


class OreoMenu(tk.Menu):
    def __init__(self, _root, *args, **kwargs):
        tk.Menu.__init__(self, _root, *args, **kwargs)

        # Menu
        # ---
        self._root = _root

        self.file_menu    = tk.Menu(self, tearoff=0, font=fira_sans)
        self.edit_menu    = tk.Menu(self, tearoff=0, font=fira_sans)
        self.run_menu     = tk.Menu(self, tearoff=0, font=fira_sans)
        self.help_menu    = tk.Menu(self, tearoff=0, font=fira_sans)
        # ---

        # File Menu
        # --- 
        self.file_menu.add_command(label="New", command=self._root.editor.new_file)
        self.file_menu.add_command(label="Open", command=self._root.editor.open_file)
        self.file_menu.add_command(label="Save", command=self._root.editor.save_file)
        self.file_menu.add_command(label="Save As...", command=self._root.editor.save_file_as)

        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self._root.editor.quit_application)

        self.add_cascade(label="File", menu=self.file_menu)
        # ---

        # Edit Menu
        # ---
        self.edit_menu.add_command(label="Cut", command=self._root.editor.cut)
        self.edit_menu.add_command(label="Copy", command=self._root.editor.copy)
        self.edit_menu.add_command(label="Paste", command=self._root.editor.paste)
        
        self.add_cascade(label="Edit", menu=self.edit_menu)
        # ---

        # Run Menu
        # ---
        self.run_menu.add_command(label="Build", command=self._root.editor.build)
        self.run_menu.add_command(label="Run", command=self._root.editor.run)
        self.run_menu.add_command(label="Build & Run", command=self._root.editor.build_run)
        self.run_menu.add_command(label="Debug", command=self._root.editor.debug)

        self.run_menu.add_separator()
        self.run_menu.add_command(label="Start Interactive Session", command=self._root.editor.interactive)

        self.add_cascade(label="Run", menu=self.run_menu)
        # ---

        # Help Menu
        # ---
        self.help_menu.add_command(label="Help", command=self._root.editor.show_help)

        self.help_menu.add_separator()
        self.help_menu.add_command(label="About", command=self._root.editor.show_about)

        self.add_cascade(label="Help", menu=self.help_menu)
        # ---

        self.setup()

    def setup(self):
        # add menubar
        # ---
        self._root.config(menu=self)
        # ---