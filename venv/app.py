from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/details', methods=['GET', 'POST'])
def details():
    if request.method == 'POST':
        student_data = {
            'Name': request.form.get('name'),
            'Registration Number': request.form.get('regno'),
            'Branch': request.form.get('branch'),
            'Web Technologies': float(request.form.get('wt')),
            'Operating Systems': float(request.form.get('os')),
            'Data Mining': float(request.form.get('dm')),
            'Artificial Intelligence': float(request.form.get('ai')),
            'Machine Learning': float(request.form.get('ml')),
            'AWS': float(request.form.get('aws'))
        }

        gpas = [
            student_data['Web Technologies'],
            student_data['Operating Systems'],
            student_data['Data Mining'],
            student_data['Artificial Intelligence'],
            student_data['Machine Learning'],
            student_data['AWS']
        ]

        average_gpa = round(sum(gpas) / len(gpas), 2)
        student_data['Average GPA'] = average_gpa

        with sqlite3.connect("student.db") as users:
            cursor = users.cursor()

            # Check if rollno already exists
            cursor.execute("SELECT COUNT(*) FROM student WHERE rollno = ?", (student_data['Registration Number'],))
            exists = cursor.fetchone()[0]

            if exists:
                return "Student with this Registration Number already exists", 400

            # Insert new student
            cursor.execute(""" 
                INSERT INTO student 
                (rollno, name, branch, wt, os, dm, ai, ml, aws, avg_gpa) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_data['Registration Number'],
                student_data['Name'],
                student_data['Branch'],
                student_data['Web Technologies'],
                student_data['Operating Systems'],
                student_data['Data Mining'],
                student_data['Artificial Intelligence'],
                student_data['Machine Learning'],
                student_data['AWS'],
                student_data['Average GPA']
            ))

            users.commit()

        # After inserting data, redirect to the report page
        return redirect(url_for('report'))

    return render_template('details.html')

@app.route('/report')
def report():
    connect = sqlite3.connect('student.db')
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM student')

    # Fetch all rows and convert them into a list of dictionaries
    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return render_template('report.html', students=data)

if __name__ == '__main__':
    app.run(debug=False)
