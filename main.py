import pyglet
import os

import tkinter as tk
from tkinter import filedialog

from utils.terminal import Terminal
from utils.data import *

class OreoEditor(tk.Frame):
    def __init__(self, _root, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        
        # IDE setup
        # ---
        self._root      = _root
        self._file      = None
        # ---

        # Editor properties
        # ---
        self.line = 0
        self.column = 0
        # ---

        # Editor setup
        # + --- +
        
        self.editor  = tk.Text(self._root, font=jetbrains_mono)
        
        # scrollbar setup
        # ---
        self.editor_scrollbar = OreoScrollbar(self.editor)
        self.editor_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.editor_scrollbar.save_pack_data(side=tk.RIGHT, fill=tk.Y)
        self.editor_scrollbar.config(command=self.editor.yview, bd=0)

        self.editor.config(yscrollcommand=self.editor_scrollbar.set)
        self.editor.pack(fill=tk.BOTH, expand=True, side=tk.TOP)
        # ---

        # Bindings Setup
        # ---
        self.bind_shortcuts()
        self.bind_key_release()
        self.bind_button_release()
        # ---

        # + --- +
    
    def bind_shortcuts(self):
        # Bindings
        # ---
        self.editor.bind("<Control-n>", self.new_file)
        self.editor.bind("<Control-o>", self.open_file)
        self.editor.bind("<Control-s>", self.save_file)
        self.editor.bind("<Control-S>", self.save_file_as)

        self.editor.bind("<Shift-F5>", self.build)
        self.editor.bind("<F5>", self.build_run)
        self.editor.bind("<Control-F5>", self.debug)
        self.editor.bind("Control-I", self.interactive)
        # ---
    
    def bind_key_release(self):
        self.editor.bind('<KeyRelease>', self.key_release)

    def bind_button_release(self):
        self.editor.bind('<ButtonRelease>', self.button_release)
    
    def change_window_name(self, name):
        self._root.title(os.path.basename(name) + " - Oreo")
    
    def clear_editor(self):
        self.editor.delete(1.0, tk.END)

    def get_all_code(self):
        return self.editor.get(1.0, tk.END)
    
    def get_line_column_info(self):
        self.line, self.column = self.editor.index(tk.INSERT).split('.')
        return self.line, self.column

    def create_interactive_window(self):
        base = tk.Toplevel(self)
        base.wm_title("Kookie Interactive")

        # Auto resizable components.
        # ---
        base.grid_rowconfigure(0, weight=1)
        base.grid_columnconfigure(0, weight=1)
        # ---

        terminal = Terminal(base, fira_code, interactive=True)
        terminal.pack(fill=tk.BOTH, expand=True)

    def button_release(self, *args):
        self.update_line_column_info()
    
    def key_release(self, *args):
        self.update_line_column_info()

    def update_line_column_info(self):
        self._root.statusbar.update_line_column_info()
    
    # Custom window
    # ---
    # def oreo_messagebox(self, title="Info", message="Info", font=fira_code):
    #     msgbox = tk.Toplevel(self)
    #     msgbox.wm_title(title)
    #     text = tk.Label(msgbox, text=message, font=font)
    #     text.pack(fill=tk.BOTH, expand=True, side=tk.TOP, anchor="w")
    #     center(msgbox)
    # ---

    def generate_event(self, eventname):
        self.editor.event_generate(eventname)

    

    def open_file(self, *args):
        self._file = filedialog.askopenfilename(
            defaultextension=".cookie",
            filetypes=[
                ("All Files", "*.*"), ("Cookie File", "*.cookie")
            ]
        )
        if self._file == "":
            self._file = None
        else:
            self.change_window_name(self._file)
            
            with open(self._file, "r") as file:
                self.editor.insert(1.0, file.read())
            
    def new_file(self, *args):
        self.change_window_name("New Cookie")
        self._file = None
        self.clear_editor()

    def save_file(self, *args):
        if self._file is None:
            self._file = filedialog.asksaveasfilename(
                initialfile='new.cookie',
                defaultextension=".cookie",
                filetypes=[
                    ("All Files", "*.*"), ("Cookie File", "*.cookie")
                ]
            )
            if self._file == "":
                self._file = None
            else:
                with open(self._file, "w") as f:
                    f.write(self.editor.get(1.0, END))
                
                self.change_window_name(self._file)
        else:
            with open(self._file, "w") as f:
                f.write(self.get_all_code())

    def save_file_as(self, *args):
        write_file = filedialog.asksaveasfilename(
            initialfile=f"{self._file}_copy.cookie",
            defaultextension=".cookie",
            filetypes=[
                ("All Files", "*.*"), ("Cookie File", "*.cookie")
            ]
        )
        if write_file != "":
            with open(file, "w") as f:
                f.write(self.editor.get(1.0, END))
            
            self._file = write_file
            self.change_window_name(self._file)
    
    def quit_application(self):
        self._root.destroy()
    
    def cut(self, *args):
        self.editor.event_generate("<<Cut>>")

    def copy(self, *args):
        self.editor.event_generate("<<Copy>>")

    def paste(self, *args):
        self.editor.event_generate("<<Paste>>")
    
    def build(self, *args):
        if self._file is not None:
            build_cmd = "{0}\\res\\exec\\kookie.exe {1}".format(os.getcwd(), self._file)
            terminal.automation("{0}".format(build_cmd))

    def build_run(self, *args):
        if self._file is not None:
            build_cmd = f"{os.getcwd()}\\res\\exec\\kookie.exe {self._file}"
            run_cmd = "{0}".format(str(self._file).replace(".cookie", ""))
            terminal.automation("{0} && {1}".format(build_cmd, run_cmd))

    def debug(self, *args):
        pass

    def interactive(self, *args):
        self.create_interactive_window()

    def show_about(self, *args):
        showinfo("Oreo", "Integrated Development Environment for Kookie.")


    def show_help(self, *args):
        showinfo("Help", help_text)


def center(win, width=100, height=100):
    win.update_idletasks()

    width = width
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width

    height = height
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width

    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
    win.deiconify()


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


class StatusBar(tk.Frame):
    def __init__(self, _root, *args, **kwargs):
        tk.Frame.__init__(self, _root, *args, **kwargs)
        self._root = _root

        self.terminal_config_button = tk.Menubutton(
            self._root, text="terminal_config_button",
            padx=10, bg="#007acc", fg="#ffffff",
            activebackground="#1f8ad2", activeforeground="#ffffff"
        )
        self.drop = tk.Menu(
            self.terminal_config_button, tearoff=False,
            background='#ffffff', foreground='#616161',
            activebackground='#0060c0', activeforeground='#ffffff'
        )
        self.drop.add_command(label="hide terminal", command=lambda: self.hide_terminal())
        self.drop.add_command(label="show terminal", command=lambda: self.show_terminal())
        self.terminal_config_button['menu'] = self.drop
        self.terminal_config_button.pack(side=tk.LEFT, fill=tk.X, padx=13)

        self.thing = tk.Menubutton(
            self._root, text="test",
            padx=10, bg="#007acc", fg="#ffffff",
            activebackground="#1f8ad2", activeforeground="#ffffff"
        )
        self.thing.pack(side=tk.LEFT, fill=tk.X, padx=2)

        self.line_column_info = tk.Menubutton(
            self._root, text="Ln ?, Col ?", 
            padx=10, bg="#007acc", fg="#ffffff",
            activebackground="#1f8ad2", activeforeground="#ffffff"
        )
        self.line_column_info.pack(side=tk.RIGHT, fill=tk.X, padx=13)
    
    def update_line_column_info(self):
        line, column = self._root.editor.get_line_column_info()
        self.line_column_info.config(text=f"Ln {int(line)}, Col {int(column) + 1}")

    def hide_terminal(self):
        self._root.terminal.pack_forget()
    

    def show_terminal(self):
        self._root.terminal.pack(fill=tk.BOTH, expand=True)
        self.terminal_config_button.pack_forget()
        self.thing.pack_forget()
        self.line_column_info.pack_forget()

        self.terminal_config_button.pack(side=tk.LEFT, fill=tk.X, padx=5)
        self.thing.pack(side=tk.LEFT, fill=tk.X, padx=2)
        self.line_column_info.pack(side=tk.RIGHT, fill=tk.X)


class IDE(tk.Tk):
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

class OreoScrollbar(tk.Scrollbar):
    def save_pack_data(self, *args, **kwargs):
        self.pack_data = kwargs
    def set(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            self.tk.call("pack", "forget", self)
        else:
            self.pack(self.pack_data)
        tk.Scrollbar.set(self, low, high)


root = IDE()
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
