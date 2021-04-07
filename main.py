import tkinter as tk
from tkinter.filedialog import *
from tkinter.messagebox import *

from terminal import Terminal

import pyglet

pyglet.font.add_file('res/ext/fira.ttf')
pyglet.font.add_file('res/ext/jbmono.ttf')

icon = "./res/cookieide.ico"
fira_sans = ('Fira Sans', 8)
jetbrains_mono = ('Fira Sans', 10)


def show_about() -> None:
    """
    show the about popup
    """
    showinfo("About Cookie IDE", "Integrated Development Environment for Cookie.")


def show_command() -> None:
    """
    show the documentation popup
    """
    # spacing is difficult
    showinfo("Help",
             "File\n"
             "-----\n"
             "New        - Creates a new file.\n"
             "Open      - Opens an existing file.\n"
             "Save        - Saves the current file.\n"
             "Save As   - Saves file as a new file.\n"
             "Exit          - Quit the application\n"
             "-----------------------------------\n"
             "Edit\n"
             "-----\n"
             "Copy       - Copy selected text.\n"
             "Cut          - Cut selected text.\n"
             "Paste       - Paste text from clipboard.")


class CookieIDE:
    def __init__(self, _root, **kwargs):
        self._root = _root
        self._Width: int = 500
        self._Height: int = 700
        self._TextArea: Text = Text(self._root, font=jetbrains_mono)
        self._ScrollBar: Scrollbar = Scrollbar(self._TextArea)
        self._file = None

        self._MenuBar: Menu = Menu(_root)
        self._FileMenu: Menu = Menu(self._MenuBar, tearoff=0, font=fira_sans)
        self._EditMenu: Menu = Menu(self._MenuBar, tearoff=0, font=fira_sans)
        self._HelpMenu: Menu = Menu(self._MenuBar, tearoff=0, font=fira_sans)
        self._CommandMenu: Menu = Menu(self._MenuBar, tearoff=0, font=fira_sans)

        try:
            self._Width = kwargs['width']
            self._Height = kwargs['height']
        except KeyError:
            print("gave invalid window size values")
            pass

        self._root.title("Untitled-CookieIDE")
        self._root.wm_iconbitmap(icon)

        # Center the window
        screen_width = self._root.winfo_screenwidth()
        screen_height = self._root.winfo_screenheight()
        left = (screen_width / 2) - (self._Width / 2)
        top = (screen_height / 2) - (self._Height / 2)

        # top and bottom
        self._root.geometry('%dx%d+%d+%d' % (self._Width, self._Height, left, top))

        # auto resizable text area.
        self._root.grid_rowconfigure(0, weight=1)
        self._root.grid_columnconfigure(0, weight=1)

        # Add controls (widget)
        # self._TextArea.grid(sticky=N + E + S + W)

        # File Menu

        # open new file
        self._FileMenu.add_command(label="New", command=self.new_file)
        # open a already existing file
        self._FileMenu.add_command(label="Open", command=self.open_file)
        # save file
        self._FileMenu.add_command(label="Save", command=self.save_file)
        # save file
        self._FileMenu.add_command(label="Save As...", command=self.save_file_as)
        # separator
        self._FileMenu.add_separator()
        # quit the application
        self._FileMenu.add_command(label="Exit", command=self.quit_application)
        # add menu
        self._MenuBar.add_cascade(label="File", menu=self._FileMenu)

        # Edit Menu

        # cut selected
        self._EditMenu.add_command(label="Cut", command=self.cut)
        # copy selected
        self._EditMenu.add_command(label="Copy", command=self.copy)
        # paste from clipboard
        self._EditMenu.add_command(label="Paste", command=self.paste)
        # add menu
        self._MenuBar.add_cascade(label="Edit", menu=self._EditMenu)

        # Help Menu

        # Documentation
        self._HelpMenu.add_command(label="Help", command=show_command)
        # separator
        self._HelpMenu.add_separator()
        # about
        self._HelpMenu.add_command(label="About", command=show_about)
        # add menu
        self._MenuBar.add_cascade(label="Help", menu=self._HelpMenu)

        # add menubar
        self._root.config(menu=self._MenuBar)
        self._ScrollBar.pack(side=RIGHT, fill=Y)

        # adjust scrollbar according to the content
        self._ScrollBar.config(command=self._TextArea.yview)
        self._TextArea.config(yscrollcommand=self._ScrollBar.set)
        self._TextArea.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

    def quit_application(self) -> None:
        """
        exits the application.
        """
        self._root.destroy()
        # exit()

    def open_file(self) -> None:
        """
        opens an existing file.
        """
        self._file = askopenfilename(defaultextension=".txt",
                                     filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self._file == "":
            # no file to open
            self._file = None
        else:
            # Try to open the file
            # set the window title
            self._root.title(os.path.basename(self._file) + " - CookieIDE")
            self._TextArea.delete(1.0, END)
            file = open(self._file, "r")
            self._TextArea.insert(1.0, file.read())
            file.close()

    def new_file(self) -> None:
        """
        Creates a new file.
        """
        self._root.title("Untitled CookieIDE")
        self._file = None
        self._TextArea.delete(1.0, END)

    def save_file(self) -> None:
        """
        saves current file.
        """
        # save as new file
        if self._file is None:
            # Save as new file
            self._file = asksaveasfilename(initialfile='main.cookie',
                                           defaultextension=".cookie",
                                           filetypes=[("All Files", "*.*"),
                                                      ("Cookie File", "*.cookie"),
                                                      ("C source files", "*.c"),
                                                      ("C header files", "*.h")])
            if self._file == "":
                self._file = None
            else:
                # Try to save the file
                file = open(self._file, "w")
                file.write(self._TextArea.get(1.0, END))
                file.close()
                # Change the window title
                self._root.title(os.path.basename(self._file) + " - CookieIDE")
        # overwrite existing
        else:
            file = open(self._file, "w")
            file.write(self._TextArea.get(1.0, END))
            file.close()

    def save_file_as(self) -> None:
        """
        saves file with given name
        """
        file = asksaveasfilename(initialfile="main.cookie",
                                 defaultextension=".cookie",
                                 filetypes=[("All Files", "*.*"),
                                            ("Cookie File", "*.cookie"),
                                            ("C source files", "*.c"),
                                            ("C header files", "*.h")])
        if file != "":
            _file = open(file, "w")
            _file.write(self._TextArea.get(1.0, END))
            _file.close()
            self._file = file
            # Change the window title
            self._root.title(os.path.basename(self._file) + " - CookieIDE")

    def cut(self) -> None:
        """
        cut the selected text
        """
        self._TextArea.event_generate("<<Cut>>")

    def copy(self) -> None:
        """
        copy the selected text
        """
        self._TextArea.event_generate("<<Copy>>")

    def paste(self) -> None:
        """
        paste text from clipboard
        """
        self._TextArea.event_generate("<<Paste>>")


root = tk.Tk()
cookie_ide = CookieIDE(_root=root, width=1000, height=700)

terminal = Terminal(root, jetbrains_mono)
terminal.pack(fill=tk.BOTH, expand=False, side=tk.BOTTOM)

statusbar_visible = tk.Button(text="test")
statusbar_visible.pack(side=tk.LEFT, fill=tk.X, padx=5)

statusbar = tk.Label(root, text="status bar on development", bd=1, relief=tk.FLAT, anchor=tk.W, padx=10)
statusbar.pack(side=tk.RIGHT, fill=tk.X)

root.mainloop()
