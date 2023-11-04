import tkinter as tk
import subprocess


class UpdateSoftware:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Verificar Atualizações")


update = UpdateSoftware()
update.window.mainloop()
