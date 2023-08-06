import sqlite3

conn = sqlite3.connect('../courseCatalog.db')
cursor = conn.cursor()

def create_db():
    """ Creates the database where all course data will be stored """
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("""CREATE TABLE school
                      (
                        name TEXT
                      )""")
    cursor.execute("""CREATE TABLE subject
                      (
                        school_id INT,
                        code TEXT,
                        name TEXT,
                        FOREIGN KEY(school_id) REFERENCES school(rowid)
                      )""")
    cursor.execute("""CREATE TABLE requirement
                      (
                        parent_requirement_id INT,
                        type TEXT,
                        FOREIGN KEY(parent_requirement_id) REFERENCES requirement(rowid)
                      )""")
    cursor.execute("""CREATE TABLE requirement_item
                      (
                        requirement_id INT,
                        FOREIGN KEY(requirement_id) REFERENCES requirement(rowid)
                      )""")
    cursor.execute("""CREATE TABLE course
                      (
                        school_id INT,
                        subject_id INT,
                        prerequisites_id INT,
                        code TEXT,
                        name TEXT,
                        units INT,
                        description TEXT,
                        FOREIGN KEY(school_id) REFERENCES school(rowid),
                        FOREIGN KEY(subject_id) REFERENCES subject(rowid),
                        FOREIGN KEY(prerequisites_id) REFERENCES requirement(rowid)
                      )""")
    conn.commit()


def add_school(name):
    """ Adds a school to the database and returns its id or just returns id if already present """
    cursor.execute("INSERT INTO school VALUES (?)", (name,))
    conn.commit()
    print(cursor.lastrowid)


def add_course(obj):
    """ Adds a course to the database and returns its id or just returns id if already present """
    pass


def add_subject(obj):
    """ Adds a subject to the database and returns its id or just returns id if already present """
    pass

create_db()
add_school('osu')
