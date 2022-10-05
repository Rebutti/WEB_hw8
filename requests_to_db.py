import sqlite3
from random import randint


def execute_query(sql: str) -> list:
    with sqlite3.connect('univer.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        return cur.fetchall()


def print_table(tuple_):
    if len(tuple_) == 0:
        return "Список пустий"
    amount_ = 30 * len(tuple_[0]) + len(tuple_[0]) + 1
    result = ('-' * amount_) + '\n'
    txt = "|{:^30}"
    for i in tuple_:
        for j in i:
            result += txt.format(j)
        result += '|\n'
    result += '-' * amount_
    return result


sql_requests = [
    ("""SELECT AVG(g.grade) as avg, s.name
    FROM grades as g
    LEFT JOIN students as s ON g.student_id = s.id
    GROUP BY s.name
    ORDER BY avg DESC
    LIMIT 5""", '5 студентів із найбільшим середнім балом з усіх предметів:'),

    ("""SELECT students.name, AVG(grade) as avg_grade, lessons.name
    FROM grades, students,lessons
    where grades.lesson_id = lessons.id and students.id = grades.student_id and lessons.id = 1
    GROUP BY students.name
    ORDER BY avg_grade DESC
    LIMIT 1;
    """,
    '1 студент із найвищим середнім балом з одного предмета:'),

    ("""SELECT l.name, avg(g.grade), gr.name
    from lessons l
    LEFT JOIN grades as g ON g.lesson_id = l.id
    LEFT JOIN groups as gr ON l.group_id = gr.id
    GROUP BY gr.name
    ORDER BY avg(g.grade) DESC
    """,
    'Середній бал в групі по одному предмету:'),

    ("""SELECT avg(g.grade)
    from grades g
    """,
    'Середній бал у потоці:'),

    ("""SELECT t.name, l.name
    from teachers t
    JOIN lessons as l ON l.teacher_id = t.id
    """,
    'Які курси читає викладач:'),

    ("""SELECT s.name, g.name
    from students s
    JOIN groups as g ON s.group_id = g.id
    where g.id = 3
    """,
    'Які курси читає викладач:'),

    ("""SELECT g.grade, l.name, gr.name, g.date_time, s.name
    FROM grades g
    JOIN lessons l on l.id = g.lesson_id 
    JOIN groups gr on gr.id = l.group_id 
    JOIN students s on s.id = l.group_id 
    WHERE l.id = 2
    ORDER BY date_time 
    LIMIT 10
    """,
    'Оцінки студентів у групі з предмета:'),

    ("""SELECT g.grade, l.name, gr.name, g.date_time, s.name
    FROM grades g
    JOIN lessons l on l.id = g.lesson_id 
    JOIN groups gr on gr.id = l.group_id 
    JOIN students s on s.id = l.group_id 
    WHERE l.id = 4 AND gr.id = 3
    ORDER BY date_time DESC 
    LIMIT 10
    """,
    'Оцінки студентів у групі з предмета на останньому занятті:'),

    (f"""SELECT l.name, s.name
    FROM groups gr
    JOIN lessons l on gr.id = l.group_id 
    JOIN students s on l.id = s.group_id 
    WHERE s.id = {randint(1,30)}
    """,
    'Список курсів, які відвідує студент:'),

    (f"""SELECT s.name, l.name, t.name
    FROM groups gr
    JOIN lessons l on gr.id = l.group_id 
    JOIN students s on l.id = s.group_id 
    JOIN teachers t on t.id = l.group_id 
    WHERE s.id = {randint(1,30)}
    """,
    'Список курсів, які студенту читає викладач:'),

    (f"""SELECT t.name, l.name, avg(g.grade) as avg_grade, s.name
    FROM teachers t
    JOIN lessons l ON t.id = l.teacher_id
    JOIN grades g ON l.id = g.lesson_id
    JOIN students s ON s.id = g.student_id
    WHERE s.id = {randint(1,30)}
    """,
    'Середній бал, який викладач ставить студенту:'),

    (f"""SELECT t.name, avg(g.grade)
    FROM lessons l
    JOIN teachers t ON t.id = l.teacher_id
    JOIN grades g ON l.id = g.lesson_id
    GROUP BY t.name
    
    """,
    'Середній бал, який ставить викладач:'),
]
if __name__ == "__main__":
    print()
    for request in sql_requests:
        print()
        result_ = execute_query(request[0])
        print(request[1] + '\n')
        print(print_table(result_))