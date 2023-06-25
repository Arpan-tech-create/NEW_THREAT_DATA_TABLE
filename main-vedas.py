from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

def convert_to_sqlite_date(date_str):
    date_obj = datetime.strptime(date_str, '%d/%b/%Y:%H:%M:%S:%z')
    return date_obj.strftime('%Y-%m-%d')

@app.route('/', methods=['GET'])
def home():
    from_date = request.args.get('from_date').strftime('%d/%b/%Y')
    to_date = request.args.get('to_date').strftime('%d/%b/%Y')

    conn = sqlite3.connect('vedas.db')
    cursor = conn.cursor()

    logs = []
    if from_date and to_date:
        from_date = convert_to_sqlite_date(from_date)
        to_date = convert_to_sqlite_date(to_date)
        cursor.execute("SELECT * FROM threat WHERE TIMESTAMP BETWEEN ? AND ?", (from_date, to_date))
    else:
        cursor.execute("SELECT * FROM threat")

    logs = cursor.fetchall()
    conn.close()

    return render_template('index.html', logs=logs)

if __name__ == '__main__':
    app.run()
