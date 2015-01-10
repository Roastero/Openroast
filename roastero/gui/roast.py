import tkinter as tk
class roastTab(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="roast", bg=root.bgColor)
        label.pack(pady=10,padx=10)
