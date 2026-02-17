from flask import Flask, render_template, request, send_file
import qrcode
import os
import sqlite3
from datetime import datetime

app = Flask(_name_)
app.config['UPLOAD_FOLDER'] = 'static/qr/'

# Ensure folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database init
conn = sqlite3.connect('qr_guardian.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS lost_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    item TEXT,
    email TEXT,
    phone TEXT,
    qr_filename TEXT,
    created_at TEXT
)''')
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    item = request.form['item']
    email = request.form['email']
    phone = request.form['phone']

    data = f"{name} - {item} - {email} - {phone}"
    filename = f"{name}{item}{int(datetime.now().timestamp())}.png"
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    qr = qrcode.make(data)
    qr.save(path)

    c.execute("INSERT INTO lost_items (name, item, email, phone, qr_filename, created_at) VALUES (?, ?, ?, ?, ?, ?)",
              (name, item, email, phone, filename, datetime.now().isoformat()))
    conn.commit()

    return render_template('success.html', name=name, item=item, filename=filename)

@app.route('/found/<filename>')
def found(filename):
    c.execute("SELECT * FROM lost_items WHERE qr_filename = ?", (filename,))
    row = c.fetchone()
    if row:
        name, item, email, phone = row[1], row[2], row[3], row[4]
        return render_template('found.html', name=name, item=item, email=email, phone=phone)
    return "Item not found."

if __