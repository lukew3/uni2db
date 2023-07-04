import sqlite3

conn = sqlite3.connect('courses.db')
cursor = conn.cursor()

def make_db():
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("""CREATE TABLE course 
                      (
                         code TEXT PRIMARY KEY,
                         full_name TEXT,
                         units TEXT,
                         grading TEXT,
                         campus TEXT,
                         career TEXT,
                         attributes TEXT,
                         description TEXT,
                         university TEXT
                      )""")
    conn.commit()

if __name__ == '__main__':
    make_db()
