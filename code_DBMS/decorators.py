import sqlite3
from tkinter import messagebox as mbox

import psycopg2
from psycopg2 import errors


def sql_error_handler(func):
    def wrapper(*args, **kvargs):
        try:
            return func(*args, **kvargs)
        except (sqlite3.OperationalError, TypeError) as sql_error:
            mbox.showerror('', sql_error)

    return wrapper


def sql_error_handler_postgres(func):
    def wrapper(*args, **kvargs):
        try:
            return func(*args, **kvargs)
        except (
            psycopg2.errors.SyntaxError,
            psycopg2.errors.UndefinedTable,
            TypeError,
        ) as sql_error:
            mbox.showerror('', sql_error)

    return wrapper


def postgres_init_massages(func):
    def wrapper(*args, **kvargs):
        try:
            return func(*args, **kvargs)
        except Exception:
            pass

    return wrapper
