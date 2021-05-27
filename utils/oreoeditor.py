import os

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from utils.data import *
from utils.oreoscrollbar import OreoScrollbar
from utils.terminal import Terminal


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
        self.editor.bind("<Control-F5>", self.run)
        self.editor.bind("<F5>", self.build_run)
        self.editor.bind("<F6>", self.debug)
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
            self.clear_editor()
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
            dir_cmd = "cd {0}".format(os.path.dirname(self._file))
            build_cmd = "{0}\\res\\exec\\kookie.exe {1}".format(os.getcwd(), self._file)
            self._root.terminal.automation("{0} && {1}".format(dir_cmd, build_cmd))
    
    def run(self, *args):
        if self._file is not None:
            executable = str(self._file).replace(".cookie", ".exe")

            dir_cmd = "cd {0}".format(os.path.dirname(self._file))
            run_cmd = "{0}".format(executable)

            if os.path.exists(executable):
                self._root.terminal.automation("{0} && {1}".format(dir_cmd, run_cmd))

            
    def build_run(self, *args):
        if self._file is not None:
            executable = str(self._file).replace(".cookie", "")

            dir_cmd = "cd {0}".format(os.path.dirname(self._file))
            build_cmd = f"{os.getcwd()}\\res\\exec\\kookie.exe {self._file}"
            run_cmd = "{0}".format(executable)
            self._root.terminal.automation("{0} && {1} && {2}".format(dir_cmd, build_cmd, run_cmd))

    def debug(self, *args):
        pass

    def interactive(self, *args):
        self.create_interactive_window()

    def show_about(self, *args):
        messagebox.showinfo("Oreo", about_text)


    def show_help(self, *args):
        messagebox.showinfo("Help", help_text)