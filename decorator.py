import sqlite3
from tkinter import messagebox as mbox


def sql_error_handler(func):
    def wrapper(*args, **kvargs):
        try:
            return func(*args, **kvargs)
        except sqlite3.OperationalError as sql_error:
            mbox.showerror('', sql_error)
    return wrapper


def select_error(func):
    def wrapper(*args, **kvargs):
        try:
            return func(*args, **kvargs)
        except sqlite3.OperationalError:
            pass
    return wrapper
