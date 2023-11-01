import tkinter as tk


class RegisterWindow:
    def __init__(self, userRegister):
        # Create a window with title
        self.window = tk.Tk()
        self.window.geometry("420x150")
        self.window.resizable(False, False)
        self.window.title("Cadastrar usuário")

        # Create a username input
        self.text_name = tk.Label(self.window, text="Nome: ")
        self.input_name = tk.Entry(self.window)

        # Create a email input
        self.text_email = tk.Label(self.window, text="Email: ")
        self.input_email = tk.Entry(self.window, width=30)

        # Create a password input
        self.text_passwd = tk.Label(self.window, text="Senha: ")
        self.input_passwd = tk.Entry(self.window, show='*')

        # Create a password confirmation input
        self.text_cpass = tk.Label(self.window, text="Confirmar senha: ")
        self.input_cpass = tk.Entry(self.window, show='*')

        # Create a register button
        self.btn_register = tk.Button(self.window, text='CADASTRAR', command=userRegister)

        # Create a cancel button
        self.btn_cancel = tk.Button(self.window, text='CANCELAR')

        # Create a messages Label
        self.text_message = tk.Label(self.window, text='')

        # Widgets positions
        self.text_name.place(x=10, y=10)
        self.input_name.place(x=52, y=10)

        self.text_email.place(x=180, y=10)
        self.input_email.place(x=220, y=10)

        self.text_passwd.place(x=10, y=35)
        self.input_passwd.place(x=52, y=35)

        self.text_cpass.place(x=180, y=35)
        self.input_cpass.place(x=280, y=35)

        self.btn_register.place(x=90, y=80)
        self.btn_cancel.place(x=250, y=80)

        self.text_message.place(x=10, y=120)

        self.center_window(420, 150)

    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")