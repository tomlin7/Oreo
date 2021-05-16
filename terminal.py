import tkinter as tk
import subprocess
import queue
import os
from threading import Thread


class Terminal(tk.Frame):
    def __init__(self, parent=None, font="consolas", interactive=False):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.create_widgets(font)

        if interactive:
            # get the path to the interactive.py file assuming it is in the same folder
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

        # make queues for keeping stdout and stderr whilst it is transferred between threads
        self.outQueue = queue.Queue()
        self.errQueue = queue.Queue()

        # keep track of where any line that is submitted starts
        self.line_start = 0

        # make the enter key call the self.enter function
        self.ttyText.bind("<Return>", self.enter)

        # a daemon to keep track of the threads so they can stop running
        self.alive = True
        # start the functions that get stdout and stderr in separate threads
        Thread(target=self.readFromProccessOut).start()
        Thread(target=self.readFromProccessErr).start()

        # start the write loop in the main thread
        self.writeLoop()

    def destroy(self):
        """This is the function that is automatically called when the widget is destroyed."""
        self.alive = False
        # write exit() to the console in order to stop it running
        self.p.stdin.write("exit()\n".encode())
        self.p.stdin.flush()
        # call the destroy methods to properly destroy widgets
        self.ttyText.destroy()
        tk.Frame.destroy(self)

    def enter(self, e):
        """The <Return> key press handler"""
        string = self.ttyText.get(1.0, tk.END)[self.line_start:]
        self.line_start += len(string)
        self.p.stdin.write(string.encode())
        self.p.stdin.flush()

    def readFromProccessOut(self):
        """To be executed in a separate thread to make read non-blocking"""
        while self.alive:
            data = self.p.stdout.raw.read(1024).decode()
            self.outQueue.put(data)

    def readFromProccessErr(self):
        """To be executed in a separate thread to make read non-blocking"""
        while self.alive:
            data = self.p.stderr.raw.read(1024).decode()
            self.errQueue.put(data)

    def writeLoop(self):
        """Used to write data from stdout and stderr to the Text widget"""
        # if there is anything to write from stdout or stderr, then write it
        if not self.errQueue.empty():
            self.write(self.errQueue.get())
        if not self.outQueue.empty():
            self.write(self.outQueue.get())

        # run this method again after 10ms
        if self.alive:
            self.after(10, self.writeLoop)

    def write(self, string):
        self.ttyText.insert(tk.END, string)
        self.ttyText.see(tk.END)
        self.line_start += len(string)

    def create_widgets(self, font):
        self.ttyText = tk.Text(self, wrap=tk.WORD, height=16, font=font, fg="grey", padx=10, pady=10, bd=8)
        self.ttyText.pack(fill=tk.BOTH, expand=True)
    
    def automation(self, string):
        self.ttyText.insert(tk.END, string)
        self.ttyText.see(tk.END)
        self.enter("test")
        self.ttyText.insert(tk.END, "\n")


# if __name__ == '__main__':
#     root = tk.Tk()
#     root.config(background="red")
#     terminal = Terminal(root)
#     terminal.pack(fill=tk.BOTH, expand=True)
#     root.mainloop()
