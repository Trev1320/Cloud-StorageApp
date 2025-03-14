from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__, template_folder='template')

def init_db():
    with sqlite3.connect("storage.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS files (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            filename TEXT UNIQUE NOT NULL)''')
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect("storage.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM files")
        files = cursor.fetchall()
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    filename = request.form.get('filename')
    if filename:
        with sqlite3.connect("storage.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO files (filename) VALUES (?)", (filename,))
            conn.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:file_id>', methods=['POST'])
def update(file_id):
    new_filename = request.form.get('new_filename')
    with sqlite3.connect("storage.db") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE files SET filename = ? WHERE id = ?", (new_filename, file_id))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:file_id>')
def delete(file_id):
    with sqlite3.connect("storage.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM files WHERE id = ?", (file_id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
