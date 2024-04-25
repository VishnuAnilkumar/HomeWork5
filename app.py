from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# SQLite Database Initialization
conn = sqlite3.connect('weather_data.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY,
                temperature REAL,
                humidity REAL,
                pressure REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_data', methods=['POST'])
def add_data():
    temperature = request.form['temperature']
    humidity = request.form['humidity']
    pressure = request.form['pressure']

    conn = sqlite3.connect('weather_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("INSERT INTO weather (temperature, humidity, pressure) VALUES (?, ?, ?)",
              (temperature, humidity, pressure))
    conn.commit()
    conn.close()

    return 'Data added successfully!'

@app.route('/get_data')
def get_data():
    conn = sqlite3.connect('weather_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute("SELECT * FROM weather ORDER BY timestamp DESC LIMIT 10")
    data = c.fetchall()
    conn.close()

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
