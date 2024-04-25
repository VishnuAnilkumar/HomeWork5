import unittest
from app import app, db
from models import WeatherData

class TestWeatherStation(unittest.TestCase):

    def setUp(self):
        # Set up the Flask application context
        self.app_context = app.app_context()
        self.app_context.push()

        # Create all database tables
        db.create_all()

    def tearDown(self):
        # Drop all database tables
        db.drop_all()

        # Remove the Flask application context
        self.app_context.pop()

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
        print("Data count after adding:", data_count)
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
        print("Data retrieved from database:", data)
        self.assertEqual(len(data), 2)

if __name__ == '__main__':
    unittest.main()
