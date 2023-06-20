from flask import Flask, render_template, request
import pandas as pd
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def show_table():
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv('data.csv')

    # Get the from_date and to_date from the request parameters
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

        # Get the checkbox values from the request parameters
    response_40x = request.args.get('40x')
    response_20x = request.args.get('20x')
    response_50x = request.args.get('50x')

    if response_40x:
        df = df[df['RESPONSE'].astype(str).str.startswith('4')]
    if response_20x:
        df = df[df['RESPONSE'].astype(str).str.startswith('2')]
    if response_50x:
        df = df[df['RESPONSE'].astype(str).str.startswith('5')]

    url = request.base_url
    if response_40x:
        url += '&40x=' + response_40x
    if response_20x:
        url += '&20x=' + response_20x
    if response_50x:
        url += '&50x=' + response_50x

    

    # Filter the DataFrame based on the date range
    if from_date and to_date:
        df['TIMESTAMP'] = pd.to_datetime(df['TIMESTAMP'], format='%d/%b/%Y:%H:%M:%S:%z')
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        mask = (df['TIMESTAMP'].dt.date >= from_date) & (df['TIMESTAMP'].dt.date <= to_date)
        df = df.loc[mask]
    

    # Convert the DataFrame to an HTML table
    table = df.to_html(classes='data', index=False)

    # Render the template with the table data
    return render_template('table.html', table=table,form_action=url)

if __name__ == '__main__':
    app.run(debug=True)
