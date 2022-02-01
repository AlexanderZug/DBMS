from tkinter import messagebox as mbox


def sql_error_handler(func):
    def wrapper(*args, **kvargs):
        try:
            return func(*args, **kvargs)
        except Exception as sql_error:
            mbox.showerror('Опять не то ввел...',
                           sql_error)
    return wrapper