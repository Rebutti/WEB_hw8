from datetime import datetime
import random
import faker
from random import randint, choice
import sqlite3

NUMBER_GRADES = 20
NUMBER_STUDENTS = 30
NUMBER_TEACHERS = 3
NUMBER_GROUPS = 3
NUMBER_LESSONS = 5
LESSONS = ('Алгебра', 'Фізика', 'Біологія', "Англійська", "Географія")
GROUPS = [('ПА-19',),('ВС-19',),('ІФ-21',)]


def generate_fake_data(number_students, number_teachers,
                       number_grades) -> tuple():

    fake_students = []
    fake_teachers = []
    fake_grades = []
    # GROUPS = ['ПА-19', 'ІФ-20', 'СВ-21']
    '''Візьмемо три компанії з faker і помістимо їх у потрібну змінну'''
    fake_data = faker.Faker('uk-UA')

    for _ in range(number_students):
        fake_students.append(fake_data.name())

    for _ in range(number_teachers):
        fake_teachers.append(fake_data.name())

    for _ in range(number_grades*number_students):
        fake_grades.append(randint(1, 5))

    return fake_students, fake_teachers, fake_grades


def prepare_data(students, teachers, grades, lessons) -> tuple():
    for_students = []

    for student in students:
        for_students.append((student, randint(1, NUMBER_GROUPS) ))

    for_teachers = []  

    for teacher in teachers:
        '''
        Для записів у таблицю співробітників нам потрібно додати посаду та id компанії. Компаній у нас було за замовчуванням
         NUMBER_COMPANIES, під час створення таблиці companies для поля id ми вказували INTEGER AUTOINCREMENT - тому кожний
         запис отримуватиме послідовне число збільшене на 1, починаючи з 1. Тому компанію вибираємо випадково
         у цьому діапазоні
        '''
        for_teachers.append((teacher,))
    '''
    Подібні операції виконаємо і для таблиці payments виплати зарплат. Приймемо, що виплата зарплати у всіх компаніях
     виконувалася з 10 по 20 числа кожного місяця. Діапазон зарплат генеруватимемо в діапазоні від 1000 до 10000 у.о.
     для кожного місяця та кожного співробітника.
    '''
    for_grades = []

    print(f'len students = {len(students)}')
    print(f'len grades = {len(grades)}')
    for lesson_id in range(1, NUMBER_LESSONS+1):
        for student_id in range(1, len(students)+1):
            for grades in range(NUMBER_GRADES):
                date_grade = datetime(2021, randint(1,12), randint(1, 28)).date()

                for_grades.append((randint(1,5), lesson_id, student_id, date_grade))
    for_lessons = []

    for lesson in lessons:
        for_lessons.append((lesson, randint(1, len(teachers)), randint(1, NUMBER_GROUPS)))

    return for_students, for_teachers, for_grades, for_lessons


def insert_data_to_db(students, teachers, grades, lessons) -> None:
    # Створимо з'єднання з нашою БД та отримаємо об'єкт курсору для маніпуляцій з даними

    with sqlite3.connect('univer.db') as con:

        cur = con.cursor()
        '''Заповнюємо таблицю компаній. І створюємо скрипт для вставлення, де змінні, які вставлятимемо, позначимо
         знаком заповнювача (?) '''

        sql_to_students = """INSERT INTO students(name, group_id)
                               VALUES (?, ?)"""
        '''Для вставлення відразу всіх даних скористаємося методом executemany курсора. Першим параметром буде текст
         скрипта, а другим дані (список кортежів).'''

        cur.executemany(sql_to_students, students)

        # Далі вставляємо дані про співробітників. Напишемо для нього скрипт і вкажемо змінні

        sql_to_teachers = """INSERT INTO teachers(name)
                               VALUES (?)"""

        # Дані були підготовлені заздалегідь, тому просто передаємо їх у функцію

        cur.executemany(sql_to_teachers, teachers)

        # Останньою заповнюємо таблицю із зарплатами

        sql_to_grades = """INSERT INTO grades(grade, lesson_id, student_id, date_time)
                              VALUES (?, ?, ?, ?)"""

        # Вставляємо дані про зарплати

        cur.executemany(sql_to_grades, grades)

        sql_to_lessons = """INSERT INTO lessons(name, teacher_id, group_id)
                              VALUES (?, ?, ?)"""

        # Вставляємо дані про зарплати

        cur.executemany(sql_to_lessons, lessons)

        sql_to_groups = """INSERT INTO groups(name)
                              VALUES (?)"""

        # Вставляємо дані про зарплати

        cur.executemany(sql_to_groups, GROUPS)

        

        # Фіксуємо наші зміни в БД

        con.commit()


if __name__ == "__main__":
    students, teachers, grades = generate_fake_data(NUMBER_STUDENTS,
                                                     NUMBER_TEACHERS,
                                                     NUMBER_GRADES)
    students, teachers, grades, lessons = prepare_data(students, teachers, grades, LESSONS)

    insert_data_to_db(students, teachers, grades, lessons)

    # print(students)
    # print('---------------------------')
    # print(teachers)
    # print('---------------------------')
    # print(grades[1])
    # print(len(grades))
    # print('---------------------------')
    # print(lessons)
    # print(len(lessons))
    # print('---------------------------')
    # print(GROUPS)