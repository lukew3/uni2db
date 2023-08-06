import sqlite3

conn = sqlite3.connect('../courseCatalog.db')
cursor = conn.cursor()

def create_db():
    """ Creates the database where all course data will be stored """
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("""CREATE TABLE school
                      (
                        id INT PRIMARY KEY,
                        name TEXT
                      )""")
    cursor.execute("""CREATE TABLE subject
                      (
                        id INT PRIMARY KEY,
                        school_id INT,
                        code TEXT,
                        name TEXT,
                        FOREIGN KEY(school_id) REFERENCES school(id)
                      )""")
    cursor.execute("""CREATE TABLE requirement
                      (
                        id INT PRIMARY KEY,
                        parent_requirement_id INT,
                        type TEXT,
                        FOREIGN KEY(parent_requirement_id) REFERENCES requirement(id)
                      )""")
    cursor.execute("""CREATE TABLE requirement_item
                      (
                        id INT PRIMARY KEY,
                        requirement_id INT,
                        FOREIGN KEY(requirement_id) REFERENCES requirement(id)
                      )""")
    cursor.execute("""CREATE TABLE course
                      (
                        id INT PRIMARY KEY,
                        school_id INT,
                        subject_id INT,
                        prerequisites_id INT,
                        code TEXT,
                        name TEXT,
                        units INT,
                        description TEXT,
                        FOREIGN KEY(school_id) REFERENCES school(id),
                        FOREIGN KEY(subject_id) REFERENCES subject(id),
                        FOREIGN KEY(prerequisites_id) REFERENCES requirement(id)
                      )""")
    conn.commit()


def add_school(obj):
    """ Adds a school to the database and returns its id or just returns id if already present """
    pass


def add_course(obj):
    """ Adds a course to the database and returns its id or just returns id if already present """
    pass


def add_subject(obj):
    """ Adds a subject to the database and returns its id or just returns id if already present """
    pass

create_db()
