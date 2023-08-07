import sqlite3
import os

DB_PATH = '../courseCatalog.db'

if os.path.exists(DB_PATH): os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

def create_db():
    """ Creates the database where all course data will be stored """
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("""CREATE TABLE school
                      (
                        id INTEGER PRIMARY KEY,
                        name TEXT
                      )""")
    cursor.execute("""CREATE TABLE subject
                      (
                        id INTEGER PRIMARY KEY,
                        school_id INTEGER,
                        code TEXT,
                        name TEXT,
                        FOREIGN KEY (school_id) REFERENCES school(id)
                      )""")
    cursor.execute("""CREATE TABLE requirement
                      (
                        id INTEGER PRIMARY KEY,
                        parent_requirement_id INT,
                        type TEXT,
                        FOREIGN KEY(parent_requirement_id) REFERENCES requirement(id)
                      )""")
    cursor.execute("""CREATE TABLE requirement_item
                      (
                        id INTEGER PRIMARY KEY,
                        requirement_id INT,
                        FOREIGN KEY(requirement_id) REFERENCES requirement(id)
                      )""")
    cursor.execute("""CREATE TABLE course
                      (
                        id INTEGER PRIMARY KEY,
                        school_id INT,
                        subject_id INT,
                        code TEXT,
                        name TEXT,
                        units INT,
                        description TEXT,
                        FOREIGN KEY(school_id) REFERENCES school(id),
                        FOREIGN KEY(subject_id) REFERENCES subject(id)
                      )""")
    conn.commit()


def add_school(name):
    """ Adds a school to the database and returns its id or just returns id if already present """
    cursor.execute("INSERT INTO school (name) VALUES (?)", (name,))
    conn.commit()
    return cursor.lastrowid


def add_subject(obj):
    """ Adds a subject to the database and returns its id or just returns id if already present """
    cursor.execute("""
        INSERT INTO subject (
            school_id,
            code,
            name
        ) VALUES (?,?,?)""",
        (obj['school_id'],obj['code'],obj['name'])
    )
    conn.commit()
    return cursor.lastrowid


def add_requirement(obj):
    """ Adds a requirement to the database and returns its id or just returns id if already present """
    cursor.execute("""
        INSERT INTO requirement (
        )""", ())
    pass


def add_course(obj):
    """ Adds a course to the database and returns its id or just returns id if already present """
    cursor.execute("""
        INSERT INTO course (
            school_id,
            subject_id,
            code,
            name,
            units,
            description
        ) VALUES (?,?,?,?,?,?)""",
        (obj['school_id'], obj['subject_id'], obj['code'], obj['name'], obj['units'], obj['description'])
    )
    conn.commit()
    return cursor.lastrowid


create_db()
school_id = add_school('osu')
add_school('umich')
subject1 = {
    'school_id': school_id, 
    'code': 'MATH',
    'name': 'Mathematics'
}
add_subject(subject1)
course1 = {
    'school_id': school_id,
    'subject_id': 1,
    'code': 'MATH 3345',
    'name': 'Foundations of Higher Mathematics',
    'units': 4,
    'description': 'this is a description'
}
add_course(course1)
