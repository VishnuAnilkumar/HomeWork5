import unittest
import sqlite3
from app import app

class TestWeatherStation(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.conn = sqlite3.connect('test_weather_data.db', check_same_thread=False)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS weather (
                            id INTEGER PRIMARY KEY,
                            temperature REAL,
                            humidity REAL,
                            pressure REAL,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )''')
        self.conn.commit()

    def tearDown(self):
        self.conn.close()
    
    def test_add_data(self):
        response = self.app.post('/add_data', data=dict(
            temperature=25.0,
            humidity=50.0,
            pressure=1013.25
        ))
        self.assertEqual(response.status_code, 200)

        # Check if data was added to the database
        self.c.execute("SELECT * FROM weather")
        data = self.c.fetchall()
        self.assertEqual(len(data), 1)
        self.assertAlmostEqual(data[0][1], 25.0, delta=0.1)
        self.assertAlmostEqual(data[0][2], 50.0, delta=0.1)
        self.assertAlmostEqual(data[0][3], 1013.25, delta=0.1)

    def test_get_data(self):
        # Add some sample data
        self.c.execute("INSERT INTO weather (temperature, humidity, pressure) VALUES (20.0, 60.0, 1015.0)")
        self.c.execute("INSERT INTO weather (temperature, humidity, pressure) VALUES (22.0, 55.0, 1012.0)")
        self.conn.commit()

        response = self.app.get('/get_data')
        self.assertEqual(response.status_code, 200)
        data = response.json

        # Check if the correct number of entries is returned
        self.assertEqual(len(data), 2)

        # Check if data fields are present
        self.assertIn('temperature', data[0])
        self.assertIn('humidity', data[0])
        self.assertIn('pressure', data[0])
        self.assertIn('timestamp', data[0])

if __name__ == '__main__':
    unittest.main()
