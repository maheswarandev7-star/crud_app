from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create Database and Table
def emp_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            S_NO INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME TEXT NOT NULL,
            EMP_ID INTEGER NOT NULL,
            SALARY INTEGER NOT NULL,
            PHONE_NUMBER INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()

emp_db()

# Home Page - Read Data
@app.route('/')
def index():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    employees = cursor.fetchall()

    conn.close()

    return render_template("index.html", employees=employees)

# Create Data
@app.route('/add', methods=['POST'])
def create():
    name = request.form['name']
    emp_id = request.form['emp_id']
    salary = request.form['salary']
    phone_number = request.form['phone_number']

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (NAME, EMP_ID, SALARY, PHONE_NUMBER)
        VALUES (?, ?, ?, ?)
    """, (name, emp_id, salary, phone_number))

    conn.commit()
    conn.close()

    return redirect('/')

# Delete Data
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE S_NO = ?", (id,))

    conn.commit()
    conn.close()

    return redirect('/')

# Edit Page
@app.route('/edit/<int:id>')
def edit(id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE S_NO = ?", (id,))
    employee = cursor.fetchone()

    conn.close()

    return render_template("edit.html", employee=employee)

# Update Data
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form['name']
    emp_id = request.form['emp_id']
    salary = request.form['salary']
    phone_number = request.form['phone_number']

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET NAME = ?, EMP_ID = ?, SALARY = ?, PHONE_NUMBER = ?
        WHERE S_NO = ?
    """, (name, emp_id, salary, phone_number, id))

    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)