import tkinter as tk


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
            self._root, text="Ln 0, Col 0", 
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