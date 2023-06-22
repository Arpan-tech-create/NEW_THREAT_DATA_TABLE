from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = sqlite3.connect('vedas.db')
    cur = conn.cursor()
    
    if request.method == 'POST':
        selected_responses = request.form.getlist('response')

        if '20x' in selected_responses:
            selected_responses.extend(['200', '203'])
        
        if '40x' in selected_responses:
            selected_responses.extend(['400', '403'])

        cur.execute('SELECT * FROM threat WHERE RESPONSE IN ({})'.format(','.join('?' * len(selected_responses))), selected_responses)
        data = cur.fetchall()

    else:
        cur.execute('SELECT * FROM threat')
        data = cur.fetchall()

    conn.close()

    return render_template('table.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
