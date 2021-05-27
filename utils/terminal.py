import tkinter as tk
import subprocess
import queue
import os
from threading import Thread


class OreoScrollbar(tk.Scrollbar):
    def save_pack_data(self, *args, **kwargs):
        self.pack_data = kwargs
    def set(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            self.tk.call("pack", "forget", self)
        else:
            self.pack(self.pack_data)
        tk.Scrollbar.set(self, low, high)


class Terminal(tk.Frame):
    def __init__(self, parent=None, font="consolas", interactive=False, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.config(background="#007acc")
        self.create_widgets(font)

        if interactive:
            consolePath = os.path.join(os.path.dirname(__file__),"interactive.py")
            self.p = subprocess.Popen(["python", consolePath],
                                        stdout=subprocess.PIPE,
                                        stdin=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        else:
            self.p = subprocess.Popen(["cmd"],
                                        stdout=subprocess.PIPE,
                                        stdin=subprocess.PIPE,
                                        stderr=subprocess.PIPE)

        # make queues for keeping stdout and stderr 
        # whilst it is transferred between threads.
        self.out_queue = queue.Queue()
        self.err_queue = queue.Queue()

        # keep track of where any line that is submitted starts
        self.line_start = 0

        # bind the enter key to self.enter
        self.terminal.bind("<Return>", self.enter)

        # daemon to keep track of the threads so they can stop running
        self.alive = True

        # start the functions that get stdout and stderr in separate threads
        Thread(target=self.read_from_proccessOut).start()
        Thread(target=self.read_from_proccessErr).start()

        # start the write loop in the main thread
        self.write_loop()

    def destroy(self):
        self.alive = False
        # write exit() to the console in order to stop it running
        self.p.stdin.write("exit()\n".encode())
        self.p.stdin.flush()
        # call the destroy methods to properly destroy widgets
        self.terminal.destroy()
        tk.Frame.destroy(self)

    def enter(self, e):
        """
        The <Return> key press handler
        """
        string = self.terminal.get(1.0, tk.END)[self.line_start:]
        self.line_start += len(string)
        self.p.stdin.write(string.encode())
        self.p.stdin.flush()

    def read_from_proccessOut(self):
        """
        To be executed in a separate thread to make read non-blocking
        """
        while self.alive:
            data = self.p.stdout.raw.read(1024).decode('utf-8')
            self.out_queue.put(data)

    def read_from_proccessErr(self):
        """
        To be executed in a separate thread to make read non-blocking
        """
        while self.alive:
            data = self.p.stderr.raw.read(1024).decode('utf-8')
            self.err_queue.put(data)

    def write_loop(self):
        """
        write data from stdout and stderr to the Text widget
        """
        # if there is anything to write from stdout or stderr, then write it
        if not self.err_queue.empty():
            self.write(self.err_queue.get())
        if not self.out_queue.empty():
            self.write(self.out_queue.get())

        # run this method again after 10ms
        if self.alive:
            self.after(10, self.write_loop)

    def write(self, output):
        self.terminal.insert(tk.END, output.replace("\\u25ba", "►"))
        self.terminal.see(tk.END)
        self.line_start += len(output)

    def create_widgets(self, font):
        self.terminal = tk.Text(
            self, wrap=tk.WORD, height=16, 
            font=font, fg="#494949", 
            padx=10, pady=10
        )
        
        self.terminal_scrollbar = OreoScrollbar(self.terminal)

        self.terminal_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.terminal_scrollbar.save_pack_data(side=tk.RIGHT, fill=tk.Y)
        self.terminal_scrollbar.config(command=self.terminal.yview)

        self.terminal.config(yscrollcommand=self.terminal_scrollbar.set)
        self.terminal.pack(fill=tk.BOTH, expand=True)
    
    def automation(self, string):
        self.terminal.insert(tk.END, string)
        self.terminal.see(tk.END)
        self.enter("test")
        self.terminal.insert(tk.END, "\n")


# Standalone
# ---

# if __name__ == '__main__':
#     root = tk.Tk()
#     root.config(background="red")
#     terminal = Terminal(root)
#     terminal.pack(fill=tk.BOTH, expand=True)
#     root.mainloop()

# ---