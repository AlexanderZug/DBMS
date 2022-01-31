import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbox
import webbrowser as wb
from db_worker import DBWorker as db


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('SQL-worker')
        self.bold_font = 'Helvetica 13 bold'
        self.center_window()
        self.resizable(False, False)
        self.frames()
        self.widgets()

    def frames(self):
        self.frame_db_sql_label = tk.Frame(self, width=1000, height=20)
        self.frame_db_sql_label.place(relx=0, rely=0, relwidth=1, relheight=0.07)
        self.frame_leble_show = tk.Frame(self, width=100, height=100, bg='white')
        self.frame_leble_show.place(relx=0, rely=0.07, relwidth=1, relheight=0.5)
        self.frame_sql_requests = tk.Frame(self, width=200, height=250, )
        self.frame_sql_requests.place(relx=0.2, rely=0.07, relwidth=0.52, relheight=0.5)
        self.frame_sql_inter_del_but = tk.Frame(self, width=1000, height=10)
        self.frame_sql_inter_del_but.place(relx=0, rely=0.5, relwidth=1, relheight=0.07)
        self.frame_sql_commands = tk.Frame(self, width=280, height=250)
        self.frame_sql_commands.place(relx=0.72, rely=0.07, relwidth=0.28, relheight=0.5)
        self.frame_close_save_but = tk.Frame(self, width=1000, height=20)
        self.frame_close_save_but.place(relx=-0.002, rely=0.92, relwidth=1, relheight=0.1)

    def widgets(self):
        self.db_sql_label()
        self.db_show()
        self.table_columns('', 0)
        self.sql_requests()
        self.sql_inter_del_but()
        self.table_for_db_cont()
        self.sql_commands()
        self.sql_symbols_dict()
        self.close_save_but()

    def center_window(self):
        width, height = 1300, 700
        s_width, s_height = self.winfo_screenwidth(), self.winfo_screenheight()
        x_screen, y_screen = (s_width - width) / 2, (s_height - height) / 2
        self.geometry(f'{width}x{height}+{int(x_screen)}+{int(y_screen)}')

    def db_sql_label(self):
        tk.Label(self.frame_db_sql_label, text='Поле для SQL-запроса',
                 height=3, font=self.bold_font).place(relx=0.35, rely=0, relwidth=0.2, relheight=1)
        tk.Label(self.frame_db_sql_label, text='Базы данных', height=3, font=self.bold_font).place(relx=0.05,
                                                                                                   rely=0, relwidth=0.1,
                                                                                                   relheight=1)
        tk.Label(self.frame_db_sql_label, text='SQL-хелпер', height=3, font=self.bold_font).place(relx=0.8,
                                                                                                  rely=0, relwidth=0.1,
                                                                                                  relheight=1)

    def db_show(self):
        db_list = db().get_all_tabels()
        self.db_tables = ttk.Combobox(self.frame_leble_show, values=db_list)
        self.db_tables.place(relx=0, rely=0, relwidth=0.2, relheight=0.1)

    def sql_requests(self):
        self.txt_sql_req = tk.Text(self.frame_sql_requests, width=700, height=253, bg='white', fg='black')
        self.txt_sql_req.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.txt_sql_req.config(insertbackground='black')
        self.txt_sql_req.focus_set()

    def sql_inter_del_but(self):
        tk.Button(self.frame_sql_inter_del_but, text='Подключение к БД', fg='black', bg='white',
                  borderwidth=10, command=lambda: self.table_for_db_cont()).place(relx=0.03, rely=0.01)
        tk.Button(self.frame_sql_inter_del_but, text='Очищение...',
                  fg='black', bg='white', borderwidth=10,
                  command=lambda: self.txt_sql_req.delete('1.0', tk.END)).place(relx=0.35, rely=0.01)
        tk.Button(self.frame_sql_inter_del_but, text='Вводи, не страшись!', fg='black', bg='white',
                  borderwidth=10,
                  command=lambda: db().get_sql_requests(self.txt_sql_req.get('1.0', tk.END).strip())).place(relx=0.46,
                                                                                                            rely=0.01)

    def table_for_db_cont(self):
        self.frame_db_content = tk.Frame(self, width=1000, height=250)
        self.frame_db_content.place(relx=0, rely=0.57, relwidth=1, relheight=0.35)
        self.tabel_db_content = ttk.Treeview(self.frame_db_content, show='headings')
        lst = db().tabel_content_to_user(self.db_tables.get())
        heads = db().tabels_header(self.db_tables.get())
        self.tabel_db_content['columns'] = heads
        for index, header in enumerate(heads):
            self.tabel_db_content.heading(header, text=header[1], anchor='center')
            self.table_columns(header[1:], index)
        for row in lst:
            self.tabel_db_content.insert('', tk.END, values=row)
        self.y_scroll()
        self.x_scroll()
        self.tabel_db_content.pack(expand=tk.YES, fill=tk.BOTH)

    def table_columns(self, columns: tuple, index: int):
        if not hasattr(self, 'txt_columns') or index == 0:
            self.txt_columns = tk.Text(self.frame_leble_show, width=150, height=90, font=self.bold_font,
                                       bg='white', fg='black')
            self.txt_columns.place(relx=0, rely=0.1, relwidth=0.2, relheight=0.76)
        self.txt_columns.insert(tk.END, ''.join(i for i in f'{columns}\n' if i != "'"))

    def sql_commands(self):
        buts = []
        row = 0
        column = 0
        commands_lst = ['SELECT', 'UPDATE', 'WHERE', 'GROUP BY', 'INSERT', 'ALTER', 'CREATE',
                        'ORDER BY', 'HAVING', 'DROP', 'INTO', 'DELETE', 'TABLE', 'FROM', 'JOIN']
        for comm_name in commands_lst:
            buts.append(tk.Button(self.frame_sql_commands, borderwidth=2, ))
            buts[-1].grid(row=row, column=column, padx=0, pady=0)
            column += 1
            buts[-1]['text'] = comm_name
            if column == 4:
                row += 1
                column = 0
            for i in range(len(buts)):
                buts[i]['command'] = lambda i=i: \
                    self.txt_sql_req.insert(tk.END, commands_lst[i].rjust(6, " ").ljust(6, " "))
                if len(commands_lst[i]) == 6:
                    buts[i]['command'] = lambda i=i: \
                        self.txt_sql_req.insert(tk.END, commands_lst[i].rjust(8, " ").ljust(8, " "))
                elif len(commands_lst[i]) > 6:
                    buts[i]['command'] = lambda i=i: \
                        self.txt_sql_req.insert(tk.END, commands_lst[i].rjust(10, " ").ljust(10, " "))

    def sql_symbols_dict(self):
        buts_symb = []
        symbols_lst = ['*', ';', "''"]
        relx = 0.74
        for symb in symbols_lst:
            buts_symb.append(tk.Button(self.frame_sql_commands, text=symb, borderwidth=3))
            buts_symb[-1].place(relx=relx, rely=0.24, relwidth=0.08, relheight=0.08)
            relx += 0.08
            buts_symb[-1]['text'] = symb
            for i in range(len(buts_symb)):
                buts_symb[i]['command'] = lambda i=i: \
                    self.txt_sql_req.insert(tk.END, symbols_lst[i].rjust(3, " ").ljust(3, " "))
        tk.Button(self.frame_sql_commands, text='Справочник SQL-запросов',
                  borderwidth=2,
                  command=lambda: wb.open('https://unetway.com/tutorials/sql')).place(relx=0.16, rely=0.67,
                                                                                      relwidth=0.7, relheight=0.2)
        tk.Button(self.frame_sql_commands, text='Шаблон таблицы',
                  borderwidth=2).place(relx=0.16, rely=0.45, relwidth=0.7, relheight=0.2)

    def close_save_but(self):
        tk.Button(self.frame_close_save_but, text="Уходя уходи", borderwidth=10,
                  command=self.pop_up_close).place(relx=0.85, rely=0.03)

    def y_scroll(self):
        scroll_bd_content_y = ttk.Scrollbar(self.frame_db_content, command=self.tabel_db_content.yview)
        self.tabel_db_content.configure(yscrollcommand=scroll_bd_content_y.set)
        scroll_bd_content_y.pack(side=tk.RIGHT, fill=tk.Y)

    def x_scroll(self):
        scroll_bd_content_x = ttk.Scrollbar(self.frame_db_content, orient='horizontal',
                                            command=self.tabel_db_content.xview)
        self.tabel_db_content.configure(xscrollcommand=scroll_bd_content_x.set)
        scroll_bd_content_x.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def pop_up_close(self):
        answer = mbox.askyesno('default', 'Ты уверен?')
        if answer is True:
            self.destroy()

    def pop_up_bd_not_conn(self):
        answer = mbox.askretrycancel('', 'Что-то пошло не так...')
        if answer is False:  ###cancel == False; retry == True
            pass


window = Window()
window.mainloop()
