"""
Region model.

Represents a wine-producing region entry.
Each region belongs to a country and is referenced by producers.
"""

from models import db

class Region(db.Model):
    __tablename__ = "regions"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey("countries.id"), nullable=False)