from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

# Home page
@app.route('/')
def index():
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transactions')
    transactions = c.fetchall()
    conn.close()
    return render_template('index.html', transactions=transactions)

# Add new transaction
@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        type = request.form['type']
        amount = float(request.form['amount'])
        description = request.form['description']

        conn = sqlite3.connect('transactions.db')
        c = conn.cursor()
        c.execute('INSERT INTO transactions (type, amount, description) VALUES (?, ?, ?)',
                  (type, amount, description))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_transaction.html')

# Delete transaction
@app.route('/delete/<int:id>')
def delete_transaction(id):
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute('DELETE FROM transactions WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# GST calculator page
@app.route('/gst')
def gst_calculator():
    return render_template('gst_calculator.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
