import tkinter as tk


class OreoScrollbar(tk.Scrollbar):
    def save_pack_data(self, *args, **kwargs):
        self.pack_data = kwargs
    def set(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            self.tk.call("pack", "forget", self)
        else:
            self.pack(self.pack_data)
        tk.Scrollbar.set(self, low, high)