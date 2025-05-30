
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('os_selection.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS selections (
            id INTEGER PRIMARY KEY,
            student_name TEXT NOT NULL,
            os_choice TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Home route to display the form
@app.route('/')
def index():
    conn = sqlite3.connect('os_selection.db')
    c = conn.cursor()
    c.execute('SELECT os_choice FROM selections')
    selected_os = [row[0] for row in c.fetchall()]
    conn.close()

    os_options = ['Ubuntu', 'Fedora', 'Arch Linux', 'Linux Mint', 'openSUSE']
    available_os = [os for os in os_options if os not in selected_os]

    return render_template('index.html', available_os=available_os)

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    student_name = request.form['studentName']
    os_choice = request.form['osSelect']

    conn = sqlite3.connect('os_selection.db')
    c = conn.cursor()
    c.execute('INSERT INTO selections (student_name, os_choice) VALUES (?, ?)', (student_name, os_choice))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Route to display all selections
@app.route('/selections')
def selections():
    conn = sqlite3.connect('os_selection.db')
    c = conn.cursor()
    c.execute('SELECT student_name, os_choice FROM selections')
    selections = c.fetchall()
    conn.close()

    return render_template('selections.html', selections=selections)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # default to 10000 locally
    app.run(host='0.0.0.0', port=port)
