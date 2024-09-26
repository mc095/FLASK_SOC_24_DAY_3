from flask import Flask
import sqlite3

app = Flask(__name__)


with sqlite3.connect('student.db') as conn:
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student (
            rollno TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            branch TEXT NOT NULL,
            wt REAL, 
            os REAL, 
            dm REAL, 
            ai REAL,
            ml REAL, 
            aws REAL,
            avg_gpa REAL 
        )
    ''')


    conn.commit()

print("Student database and table created successfully.")
