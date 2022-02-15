import tkinter as tk
import webbrowser as wb

from tkinter import messagebox as mbox
from tkinter import filedialog as fd
from tkinter import ttk
from PostgreSQL import PostgreSQL
from SQLite import SQLite
from window_user_data_postrge import UserForm
from logger_config import logger


class Window(tk.Tk):
    """
    The class has a Tkinter interface with business logic.
    It accepts user requests and switches the processing strategy.
    """

    def __init__(self):
        super().__init__()
        self.title('SQL-worker')
        self.bold_font = 'Helvetica 13 bold'
        self.center_window()
        self.resizable(False, False)
        self.db = SQLite()
        self.frames()
        self.widgets()

    def frames(self):
        self.frame_title_labels = ttk.Frame(self, width=1000, height=20)
        self.frame_title_labels.place(relx=0, rely=0, relwidth=1, relheight=0.07)
        self.frame_db_tables_content = tk.Frame(self, width=100, height=100, bg='white')
        self.frame_db_tables_content.place(relx=0, rely=0.07, relwidth=1, relheight=0.5)
        self.frame_sql_requests = ttk.Frame(self, width=200, height=250, )
        self.frame_sql_requests.place(relx=0.2, rely=0.07, relwidth=0.52, relheight=0.5)
        self.frame_tables_sql_but = ttk.Frame(self, width=1000, height=10)
        self.frame_tables_sql_but.place(relx=0, rely=0.5, relwidth=1, relheight=0.07)
        self.frame_sql_commands = ttk.Frame(self, width=280, height=250)
        self.frame_sql_commands.place(relx=0.72, rely=0.07, relwidth=0.28, relheight=0.5)
        self.frame_close_but = ttk.Frame(self, width=1000, height=20)
        self.frame_close_but.place(relx=-0.002, rely=0.92, relwidth=1, relheight=0.1)

    def widgets(self):
        self.db_sql_label()
        self.table_show()
        self.table_columns('', 0)
        self.sql_requests()
        self.btns_for_sql_requests()
        self.sql_requests_for_select()
        self.sql_commands_grid()
        self.sql_commands_place()
        self.btns_for_close_db_choose()

    def center_window(self):
        width, height = 1300, 700
        s_width, s_height = self.winfo_screenwidth(), self.winfo_screenheight()
        x_screen, y_screen = (s_width - width) / 2, (s_height - height) / 2
        self.geometry(f'{width}x{height}+{int(x_screen)}+{int(y_screen)}')

    def db_sql_label(self):
        tk.Label(self.frame_title_labels, text='Поле для SQL-запроса',
                 height=3, font=self.bold_font).place(relx=0.35, rely=0, relwidth=0.2, relheight=1)
        tk.Label(self.frame_title_labels, text='Базы данных', height=3, font=self.bold_font).place(relx=0.05,
                                                                                                   rely=0, relwidth=0.1,
                                                                                                   relheight=1)
        tk.Label(self.frame_title_labels, text='SQL-хелпер', height=3, font=self.bold_font).place(relx=0.8,
                                                                                                  rely=0, relwidth=0.1,
                                                                                                  relheight=1)

    @logger.catch
    def table_show(self):  # The method takes all tables' names from DB.
        db_list = self.db.get_all_tables()
        self.db_tables = ttk.Combobox(self.frame_db_tables_content, values=db_list)
        self.db_tables.place(relx=0, rely=0, relwidth=0.2, relheight=0.1)

    def sql_requests(self):  # The method creates the text-field for sql requests.
        self.txt_sql_req = tk.Text(self.frame_sql_requests, width=700, height=253, bg='white', fg='black')
        self.txt_sql_req.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.txt_sql_req.config(insertbackground='black')
        self.txt_sql_req.focus_set()

    def btns_for_sql_requests(self):
        tk.Button(self.frame_tables_sql_but, text='Выбрать таблицу', fg='black', bg='white',
                  command=lambda: self.table_for_db_cont([])).place(relx=0.03, rely=0.01)
        tk.Button(self.frame_tables_sql_but, text='Очищение...',
                  fg='black', bg='white',
                  command=lambda: self.txt_sql_req.delete('1.0', tk.END)).place(relx=0.35, rely=0.01)
        #  It accepts two versions of sql requests - select request (method) and other requests (get text).
        tk.Button(self.frame_tables_sql_but, text='Вводи, не страшись!', fg='black', bg='white',
                  command=lambda: [self.db.get_sql_requests(self.txt_sql_req.get('1.0', tk.END).strip()),
                                   self.sql_requests_for_select()]).place(relx=0.46, rely=0.01)

    def sql_requests_for_select(self):  # The method checks whether the request is select. If the truth, transmits it
        # as a list in the table. Otherwise returns a blank list.
        lst = []
        if self.txt_sql_req.get('1.0', tk.END)[0:6].strip() == 'SELECT':
            lst = self.db.get_sql_select_requests(self.txt_sql_req.get('1.0', tk.END))
        self.table_for_db_cont(lst)

    @logger.catch
    def table_for_db_cont(self, lst: list):  # The method takes the name of the columns and their content and
        # displays the user.
        self.frame_db_content = ttk.Frame(self, width=1000, height=250)
        self.frame_db_content.place(relx=0, rely=0.57, relwidth=1, relheight=0.35)
        self.tabel_db_content = ttk.Treeview(self.frame_db_content, show='headings')
        if not lst:
            lst = self.db.send_table_content_to_user(self.db_tables.get())
        heads = self.db.get_tables_header(self.db_tables.get())
        self.tabel_db_content['columns'] = heads
        if isinstance(self.db, SQLite):  # This check is necessary, since the name of the column in SQLite and
            # Postgres are located under different indexes.
            for index, header in enumerate(heads):
                self.tabel_db_content.heading(header, text=header[1], anchor='center')
                self.table_columns(header[0:], index)
        else:
            for index, header in enumerate(heads):
                self.tabel_db_content.heading(header, text=header[0], anchor='center')
                self.table_columns(header[0:], index)
        for row in lst:
            self.tabel_db_content.insert('', tk.END, values=row)
        self.y_scroll()
        self.x_scroll()
        self.tabel_db_content.pack(expand=tk.YES, fill=tk.BOTH)

    def table_columns(self, columns: str, index: int):  # The method shows table settings.
        if index == 0:
            self.txt_columns = tk.Text(self.frame_db_tables_content, width=150, height=90, font=self.bold_font,
                                       bg='white', fg='black')
            self.txt_columns.place(relx=0, rely=0.1, relwidth=0.2, relheight=0.76)
        self.txt_columns.insert(tk.END, ''.join(i for i in f'{columns}\n' if i != "'"))

    def sql_commands_grid(self):
        buts = []
        row = 0
        column = 0
        commands_lst = ['SELECT', 'UPDATE', 'WHERE', 'GROUP BY', 'INSERT', 'ALTER', 'CREATE',
                        'ORDER BY', 'HAVING', 'DROP', 'INTO', 'VALUES', 'TABLE', 'FROM', 'JOIN',
                        'DELETE', ]
        for comm_name in commands_lst:
            buts.append(tk.Button(self.frame_sql_commands, ))
            buts[-1].grid(row=row, column=column, padx=0, pady=0)
            column += 1
            buts[-1]['text'] = comm_name
            if column == 4:
                row += 1
                column = 0
            for i in range(len(buts)):
                buts[i]['command'] = lambda i=i: \
                    self.txt_sql_req.insert(tk.END, commands_lst[i].ljust(6, " "))  # Adding gaps depending on the
                # word length.
                if len(commands_lst[i]) == 6:
                    buts[i]['command'] = lambda i=i: \
                        self.txt_sql_req.insert(tk.END, commands_lst[i].ljust(8, " "))
                elif len(commands_lst[i]) > 6:
                    buts[i]['command'] = lambda i=i: \
                        self.txt_sql_req.insert(tk.END, commands_lst[i].ljust(10, " "))

    def sql_commands_place(self):
        buts_symb = []
        symbols_lst = ['AND', 'OR', '*', ';', "''", ]
        relx = 0.05
        for symb in symbols_lst:
            buts_symb.append(tk.Button(self.frame_sql_commands, text=symb, ))
            buts_symb[-1].place(relx=relx, rely=0.32, relwidth=0.11, relheight=0.08)
            relx += 0.12
            buts_symb[-1]['text'] = symb
            for i in range(len(buts_symb)):
                if len(symbols_lst[i]) > 2:
                    buts_symb[i]['command'] = lambda i=i: \
                        self.txt_sql_req.insert(tk.END, symbols_lst[i].ljust(4, " "))  # Adding gaps depending on the
                # word length.
                else:
                    buts_symb[i]['command'] = lambda i=i: \
                        self.txt_sql_req.insert(tk.END, symbols_lst[i].ljust(3, " "))
        tk.Button(self.frame_sql_commands, text='Справочник SQL-запросов',
                  command=lambda: wb.open('https://unetway.com/tutorials/sql')).place(relx=0.16, rely=0.54,
                                                                                      relwidth=0.7, relheight=0.2)
        tk.Button(self.frame_sql_commands, text='PRIMARY KEY',
                  command=lambda: self.txt_sql_req.insert(tk.END,
                                                          'PRIMARY KEY'.ljust(12, " "))).place(relx=0.65, rely=0.32,
                                                                                               relwidth=0.3,
                                                                                               relheight=0.08)

    def btns_for_close_db_choose(self):
        tk.Button(self.frame_close_but, text="Уходя уходи", command=self.pop_up_close).place(relx=0.85, rely=0.03)
        tk.Button(self.frame_close_but, text='Выбрать локальную БД (SQLite)', fg='black', bg='white',
                  command=self.__new_db_config).place(relx=0.04, rely=0.01)
        tk.Button(self.frame_close_but, text='Подключиться к удаленной БД (PostgreSQL)', fg='black',
                  bg='white', command=self.__new_postgre_config).place(relx=0.25, rely=0.01)

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

    @logger.catch
    def __new_db_config(self):  # The method switches to SQLite-strategy.
        self.db = SQLite()
        self.db.con = fd.askopenfilename()
        self.table_show()

    @logger.catch
    def __new_postgre_config(self):  # The method switches to Postgres-strategy.
        if isinstance(self.db, SQLite):
            self.db = PostgreSQL()
            self.db.con = UserForm(self).open_user_data_postgres_window()
            self.table_show()
            # This check is necessary that in the
            # case of incorrect data or closing the window without entering data it is possible to call the
            # window again (since otherwise the strategy remains the same and the window is not called).
        elif isinstance(self.db, PostgreSQL) and not hasattr(self.db, 'con'):
            self.db.con = UserForm(self).open_user_data_postgres_window()
            self.table_show()


if __name__ == '__main__':
    window = Window()
    window.mainloop()
