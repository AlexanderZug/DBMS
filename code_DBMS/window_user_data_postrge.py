
import tkinter as tk

from tkinter import messagebox as mbox


class UserForm(tk.Toplevel):
    """
    The class creates a new window to get user data for Postgres-connection.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.title('Введите данные')
        self.protocol('WM_DELETE_WINDOW', self.on_closing)
        self.center_window()
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.host = tk.StringVar()
        self.db_name = tk.StringVar()
        self.labels()
        self.entries()

    def center_window(self):
        width, height = 300, 150
        s_width, s_height = self.winfo_screenwidth(), self.winfo_screenheight()
        x_screen, y_screen = (s_width - width) / 2, (s_height - height) / 2
        self.geometry(f'{width}x{height}+{int(x_screen)}+{int(y_screen)}')

    def on_closing(self):
        if mbox.askyesno("", "Необходимо ввести данные для подключения, уверен, что ты нас покидаешь?"):
            self.destroy()

    def labels(self):
        lbs = []
        row = 1
        column = 0
        lbs_names_lst = ['user_name', 'password', 'host_name', 'db_name', ]
        for lbl_name in lbs_names_lst:
            lbs.append(tk.Label(self, text=lbl_name, width=10, height=1))
            lbs[-1].grid(row=row, column=column)
            row += 1

    def entries(self):
        entries = []
        row = 1
        column = 1
        entries_list = [self.username, self.password, self.host, self.db_name]
        for entry in entries_list:
            entries.append(tk.Entry(self, textvariable=entry, bg='white', fg='black'))
            entries[-1].grid(row=row, column=column)
            row += 1
            entries[-1].config(insertbackground='black')
        entries[0].focus_set()
        tk.Button(self, text="Ввести данные", command=self.destroy).grid(row=5, columnspan=2)

    def open_user_data_postgres_window(self):
        self.grab_set()
        self.wait_window()
        return self.username.get(), self.password.get(), self.host.get(), self.db_name.get()
