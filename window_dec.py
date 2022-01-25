import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbox


class Window(tk.Tk):
    def __init__(self):
        super(Window, self).__init__()
        self.title('SQL-worker')
        self.bold_font = 'Helvetica 13 bold'
        self.geometry('1300x700')
        self.resizable(False, False)
        self.frames()

    def frames(self):
        self.db_sql_label()
        self.db_show()
        self.sql_requests()
        self.sql_inter_del_but()
        self.db_content()
        self.sql_commands()
        self.close_save_but()

    def db_sql_label(self):
        frame_db_sql_label = tk.Frame(self, width=1000, height=20)
        frame_db_sql_label.place(relx=0, rely=0, relwidth=1, relheight=0.07)
        tk.Label(frame_db_sql_label, text='Поле для SQL-запроса',
                 height=3, font=self.bold_font).place(relx=0.35, rely=0, relwidth=0.2, relheight=1)
        tk.Label(frame_db_sql_label, text='Базы данных', height=3, font=self.bold_font).place(relx=0.05,
                                                                                              rely=0, relwidth=0.1,
                                                                                              relheight=1)
        tk.Label(frame_db_sql_label, text='SQL-хелпер', height=3, font=self.bold_font).place(relx=0.8,
                                                                                             rely=0, relwidth=0.1,
                                                                                             relheight=1)

    def db_show(self):
        frame_sql_requests = tk.Frame(self, width=600, height=200, bg='white')
        frame_sql_requests.place(relx=0, rely=0.07, relwidth=1, relheight=0.5)
        db_list = ['1', '2', '3', '4', '5']
        ttk.Combobox(frame_sql_requests, values=db_list).place(relx=0, rely=0, relwidth=0.2, relheight=0.1)

    def sql_requests(self):
        frame_sql_requests = tk.Frame(self, width=400, height=250, bg='blue')
        frame_sql_requests.place(relx=0.2, rely=0.07, relwidth=0.7, relheight=0.5)
        self.txt_sql_req = tk.Text(frame_sql_requests, width=700, height=253, bg='white', fg='black')
        self.txt_sql_req.place(relx=0, rely=0, relwidth=1, relheight=1)

    def sql_inter_del_but(self):
        frame_sql_inter_del_but = tk.Frame(self, width=1000, height=10)
        frame_sql_inter_del_but.place(relx=0, rely=0.5, relwidth=1, relheight=0.07)
        tk.Button(frame_sql_inter_del_but, text='Подключение к БД', fg='black', bg='white',
                  borderwidth=10, command=self.pop_up_bd_not_conn).place(relx=0.03, rely=0.01)
        tk.Button(frame_sql_inter_del_but, text='Очищение...',
                  fg='black', bg='white', borderwidth=10,
                  command=lambda: self.txt_sql_req.delete('1.0', tk.END)).place(relx=0.35, rely=0.01)
        tk.Button(frame_sql_inter_del_but, text='Вводи, не страшись!', fg='black', bg='white',
                  borderwidth=10,
                  command=lambda: print(self.txt_sql_req.get('1.0', tk.END).strip())).place(relx=0.46, rely=0.01)

    def db_content(self):
        frame_db_content = tk.Frame(self, width=1000, height=250, bg='green')
        frame_db_content.place(relx=0, rely=0.57, relwidth=1, relheight=0.35)
        self.tabel_db_content = ttk.Treeview(frame_db_content, show='headings')
        lst = [(2, 12, 2.09, 4, 6, 8), (3, 12, 2.09), (4, 12, 2.09),
               (2, 12, 2.09, 4, 6, 8), (2, 12, 2.09, 4, 6, 8), (3, 12, 2.09), (4, 12, 2.09),
               (2, 12, 2.09, 4, 6, 8), (2, 12, 2.09, 4, 6, 12), (2, 12, 2.09, 4, 6, 8), (3, 12, 2.09), (4, 12, 2.09),
               (2, 12, 2.09, 4, 6, 8), (2, 12, 2.09, 4, 6, 12)]
        heads = ['id', 'col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6']
        self.tabel_db_content['columns'] = heads
        for header in heads:
            self.tabel_db_content.heading(header, text=header, anchor='center')
        for row in lst:
            self.tabel_db_content.insert('', tk.END, values=row)
        scroll_bd_content_y = ttk.Scrollbar(frame_db_content, command=self.tabel_db_content.yview)
        self.tabel_db_content.configure(yscrollcommand=scroll_bd_content_y.set)
        scroll_bd_content_y.pack(side=tk.RIGHT, fill=tk.Y)

    def sql_commands(self):
        frame_sql_commands = tk.Frame(self, width=280, height=250)
        frame_sql_commands.place(relx=0.72, rely=0.07, relwidth=0.28, relheight=0.5)
        row = 0
        column = 0
        commands_lst = ['SELECT', 'UPDATE', 'WHERE', 'GROUP BY', 'INSERT', 'ALTER', 'CREATE',
                       'ORDER BY', 'HAVING', 'DROP', 'INTO', 'DELETE', 'TABEL', 'FROM', 'JOIN']
        for comm_name in commands_lst:
            tk.Button(frame_sql_commands, text=comm_name,
                      borderwidth=2).grid(row=row, column=column, padx=0, pady=0)
            column += 1
            if column == 4:
                row += 1
                column = 0
        symbols_lst = ['*', ';', "''"]
        relx = 0.74
        for symb in symbols_lst:
            tk.Button(frame_sql_commands, text=symb, borderwidth=3).place(relx=relx, rely=0.24, relwidth=0.08,
                                                                          relheight=0.08)
            relx += 0.08
        tk.Button(frame_sql_commands, text='Справочник SQL-запросов',
                  borderwidth=2).place(relx=0.16, rely=0.45, relwidth=0.7, relheight=0.2)
        tk.Button(frame_sql_commands, text='Подключение к Python',
                  borderwidth=2).place(relx=0.16, rely=0.67, relwidth=0.7, relheight=0.2)

    def close_save_but(self):
        frame_close_save_but = tk.Frame(self, width=1000, height=20)
        frame_close_save_but.place(relx=-0.002, rely=0.92, relwidth=1, relheight=0.1)
        tk.Button(frame_close_save_but, text="Уходя уходи", borderwidth=10,
                  command=self.pop_up_close).place(relx=0.85, rely=0.15)
        tk.Button(frame_close_save_but, text="Сохраняя сохраняй", borderwidth=10).place(relx=0.65, rely=0.15)
        scroll_bd_content_x = ttk.Scrollbar(frame_close_save_but, orient='horizontal',
                                            command=self.tabel_db_content.xview)
        self.tabel_db_content.configure(xscrollcommand=scroll_bd_content_x.set)
        scroll_bd_content_x.pack(side=tk.TOP, fill=tk.BOTH)
        self.tabel_db_content.pack(expand=tk.YES, fill=tk.BOTH)

    def pop_up_close(self):
        answer = mbox.askyesno('default', 'Ты уверен?')
        if answer is True:
            self.destroy()

    def pop_up_bd_not_conn(self):
        anser = mbox.askretrycancel('','Что-то пошло не так...')
        if anser is False: ###cancel == False; retry == True
            pass


window = Window()
window.mainloop()