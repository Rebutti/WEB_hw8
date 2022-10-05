CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        name VARCHARE(30) NOT NULL,
                        group_id INTEGER NOT NULL,
                        FOREIGN KEY (group_id) REFERENCES groups (id)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE);
CREATE TABLE IF NOT EXISTS groups (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        name VARCHARE(10) NOT NULL);
CREATE TABLE IF NOT EXISTS teachers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        name VARCHARE(10) NOT NULL);
CREATE TABLE IF NOT EXISTS lessons (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        name VARCHARE(10) NOT NULL,
                        teacher_id INTEGER NOT NULL,
                        group_id INTEGER NOT NULL,
                        FOREIGN KEY (teacher_id) REFERENCES teachers (id)
                            ON DELETE SET NULL
                            ON UPDATE CASCADE
                        FOREIGN KEY (group_id) REFERENCES groups (id)
                            ON DELETE SET NULL
                            ON UPDATE CASCADE);
CREATE TABLE IF NOT EXISTS grades (
                        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                        grade INT NOT NULL,
                        lesson_id INTEGER NOT NULL,
                        student_id INTEGER NOT NULL,
                        date_time DATETIME,
                        FOREIGN KEY (lesson_id) REFERENCES lessons (id)
                            ON DELETE SET NULL
                            ON UPDATE CASCADE
                        FOREIGN KEY (student_id) REFERENCES students (id)
                            ON DELETE CASCADE
                            ON UPDATE CASCADE
                            );

