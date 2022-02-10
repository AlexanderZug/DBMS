import sqlite3
from tkinter import messagebox as mbox
from psycopg2 import errors

import psycopg2


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


def sql_error_handler_postgres(func):
    def wrapper(*args, **kvargs):
        try:
            return func(*args, **kvargs)
        except (psycopg2.errors.SyntaxError, psycopg2.errors.UndefinedColumn) as sql_error:
            mbox.showerror('', sql_error)

    return wrapper


def select_error_postgres(func):
    def wrapper(*args, **kvargs):
        try:
            return func(*args, **kvargs)
        except (psycopg2.errors.SyntaxError, psycopg2.errors.UndefinedColumn) as select_error:
            mbox.showerror('', select_error)

    return wrapper


def postgres_init_massages(func):
    def wrapper(*args, **kvargs):
        try:
            return func(*args, **kvargs)
        except Exception as e:
            mbox.showerror('', f"Ошибка подключения: '{e}'")

    return wrapper
