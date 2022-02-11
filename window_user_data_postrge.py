
import tkinter as tk


class UserForm(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Введите данные')
        self.center_window()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.host = tk.StringVar()
        self.db_name = tk.StringVar()
        self.entries()

    def center_window(self):
        width, height = 300, 150
        s_width, s_height = self.winfo_screenwidth(), self.winfo_screenheight()
        x_screen, y_screen = (s_width - width) / 2, (s_height - height) / 2
        self.geometry(f'{width}x{height}+{int(x_screen)}+{int(y_screen)}')

    def entries(self):
        tk.Label(self, text='user_name', width=10, height=1).grid(row=1, column=0)
        password_entry = tk.Entry(self, textvariable=self.username, bg='white', fg='black')
        password_entry.grid(row=1, column=1)
        password_entry.config(insertbackground='black')

        tk.Label(self, text='password', width=10, height=1).grid(row=2, column=0)
        password_entry = tk.Entry(self, textvariable=self.password, bg='white', fg='black')
        password_entry.grid(row=2, column=1)
        password_entry.config(insertbackground='black')

        tk.Label(self, text='host_name', width=10, height=1).grid(row=3, column=0)
        user_entry = tk.Entry(self, textvariable=self.host, bg='white', fg='black')
        user_entry.grid(row=3, column=1)
        user_entry.config(insertbackground='black')

        tk.Label(self, text='db_name', width=10, height=1).grid(row=4, column=0)
        user_entry = tk.Entry(self, textvariable=self.db_name, bg='white', fg='black')
        user_entry.grid(row=4, column=1)
        user_entry.config(insertbackground='black')

        btn = tk.Button(self, text="Submit", command=self.destroy)
        btn.grid(row=5, columnspan=2)

    def open(self):
        self.grab_set()
        self.wait_window()
        username = self.username.get()
        password = self.password.get()
        host = self.host.get()
        db_name = self.db_name.get()
        return username, password, host, db_name

