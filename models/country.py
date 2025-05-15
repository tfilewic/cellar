"""
Country model.

Represents a country entry.
Referenced by producers.
"""

from models import db

class Country(db.Model):
    __tablename__ = "countries"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
