from flask import Flask, render_template, request
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

def convert_timestamp(timestamp):
    # Convert the timestamp to a compatible format for SQLite
    dt = datetime.strptime(timestamp, '%d/%b/%Y:%H:%M:%S +%f')
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def get_filtered_results(from_date_obj, to_date_obj, selected_responses=None):
    conn = sqlite3.connect('vedas.db')
    cursor = conn.cursor()

    if selected_responses:
        if '20x' in selected_responses:
            selected_responses.extend(['200', '203'])
        
        if '40x' in selected_responses:
            selected_responses.extend(['400', '403'])

        cursor.execute('SELECT * FROM threat WHERE RESPONSE IN ({})'.format(','.join('?' * len(selected_responses))), selected_responses)
    else:
        cursor.execute("SELECT * FROM threat")

    rows = cursor.fetchall()

    results = []
    for row in rows:
        timestamp_str = row[0]
        timestamp = convert_timestamp(timestamp_str)
        timestamp_obj = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S').date()
        
        if selected_responses:
            if from_date_obj <= timestamp_obj <= to_date_obj:
                results.append(row)
        else:
            results.append(row)

    cursor.close()
    conn.close()

    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('vedas.db')
    cur = conn.cursor()
    
    if request.method == 'POST':
        selected_responses = request.form.getlist('response')

        from_date = request.form['from_date']
        to_date = request.form['to_date']

        if from_date and to_date:
            from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
            to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
        else:
            from_date_obj = datetime.min.date()
            to_date_obj = datetime.max.date()

        data = get_filtered_results(from_date_obj, to_date_obj, selected_responses)

    else:
        cur.execute('SELECT * FROM threat')
        data = cur.fetchall()

    conn.close()

    return render_template('table.html', data=data)


@app.route('/piechart')
def piechart():
    # Connect to the SQLite database
    conn = sqlite3.connect('vedas.db')
    cursor = conn.cursor()

    # Execute the query to count occurrences of each message in the 403 responses
    cursor.execute("SELECT MESSAGE, COUNT(*) AS Occurrences FROM threat WHERE RESPONSE = 403 GROUP BY MESSAGE")
    results = cursor.fetchall()

    # Prepare data for the pie chart
    data = []
    for row in results: 
        message = row[0]
        occurrences = row[1]
        data.append({'name': message, 'y': occurrences})
    
    results1 = cursor.execute("""
        SELECT COUNT(*) AS occurrences, SUBSTR(TIMESTAMP, 1, 11) AS date
        FROM threat
        GROUP BY date
        HAVING date IN ('09/Nov/2022', '10/Nov/2022', '11/Nov/2022')
    """).fetchall()

    # Close the database connection


    # Prepare data for Highcharts
    data1 = []
    for row in results1:
        occurrences, date = row
        data1.append({'date': date, 'occurrences': occurrences})

    # Close the database connection
    cursor.close()
    conn.close()

    return render_template('pie.html',data1=data1)

if __name__ == '__main__':
    app.run(debug=True)
