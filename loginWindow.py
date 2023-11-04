import tkinter as tk


class LoginWindow:
    def __init__(self, call_main_window):
        # Create a window with title
        self.window = tk.Tk()
        self.window.geometry("220x120")
        self.window.resizable(False, False)
        self.window.title("Login")

        # Create username label and entry
        self.text_name = tk.Label(self.window, text='Nome: ')
        self.input_name = tk.Entry(self.window)
        self.input_name.focus()

        # Create password label and entry
        self.text_passwd = tk.Label(self.window, text='Senha: ')
        self.input_passwd = tk.Entry(self.window, show='*')
        self.input_passwd.bind("<Return>", call_main_window)

        # Create a login button
        self.btn_login = tk.Button(self.window, text='ENTRAR', command=call_main_window)

        # Create a messages label
        self.text_message = tk.Label(self.window, text='')

        # Widgets positions
        self.text_name.place(x=10, y=10)
        self.input_name.place(x=60, y=10)

        self.text_passwd.place(x=10, y=35)
        self.input_passwd.place(x=60, y=35)

        self.btn_login.place(x=85, y=60)

        self.text_message.place(x=10, y=87)

        self.center_window(220, 120)

    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")
