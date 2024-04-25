# models.py

from app import db

class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100))
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    wind_speed = db.Column(db.Float)

    def __repr__(self):
        return f"<WeatherData(location={self.location}, temperature={self.temperature}, humidity={self.humidity}, wind_speed={self.wind_speed})>"
