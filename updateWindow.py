import tkinter as tk
# import subprocess


class UpdateSoftware:
    def __init__(self):
        # Create a update window
        self.window = tk.Tk()
        self.window.geometry('300x100')
        self.window.title("Verificar Atualizações")

        # Create update window widgets
        self.status_label = tk.Label(text="Status: ")
        self.status_info = tk.Label(text="")
        self.btn_update = tk.Button(self.window, text="ATUALIZAR", state=tk.DISABLED)

        # Widgtes positions
        self.status_label.place(x=10, y=10)
        self.status_info.place(x=10, y=30)
        self.btn_update.place(x=110, y=60)

        self.center_window(300, 100)

    # Centralize the window
    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")
