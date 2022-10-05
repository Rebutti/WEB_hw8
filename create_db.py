import sqlite3


# sql_create_users_table ="""CREATE TABLE IF NOT EXISTS students (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                         name VARCHARE(30) NOT NULL);
#                         CREATE TABLE IF NOT EXISTS teachers (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#                         name VARCHARE(30) NOT NULL);
#                         """

def create_db():
    # читаємо файл зі скриптом для створення БД
    with open('univer.sql', 'r') as f:
        sql = f.read()

    # створюємо з'єднання з БД (якщо файлу з БД немає, він буде створений)
    with sqlite3.connect('univer.db') as con:
        cur = con.cursor()
        # виконуємо скрипт із файлу, який створить таблиці у БД
        cur.executescript(sql)


if __name__ == "__main__":
    create_db()