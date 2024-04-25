import unittest
import sqlite3
from app import app

import unittest
from app import app, db  # Assuming 'app' is your Flask application instance and 'db' is the SQLAlchemy database object
from models import WeatherData  # Assuming 'WeatherData' is the SQLAlchemy model for weather data

class TestWeatherStation(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_data(self):
        # Add sample data to the database
        data = WeatherData(
            location='New York',
            temperature=75,
            humidity=60,
            wind_speed=10
        )
        db.session.add(data)
        db.session.commit()

        # Query the database to check if data is added
        data_count = WeatherData.query.count()
        self.assertEqual(data_count, 1)

    def test_get_data(self):
        # Add sample data to the database
        data1 = WeatherData(
            location='New York',
            temperature=75,
            humidity=60,
            wind_speed=10
        )
        data2 = WeatherData(
            location='Los Angeles',
            temperature=80,
            humidity=50,
            wind_speed=5
        )
        db.session.add(data1)
        db.session.add(data2)
        db.session.commit()

        # Query the database to retrieve data
        data = WeatherData.query.all()
        self.assertEqual(len(data), 2)

if __name__ == '__main__':
    unittest.main()

