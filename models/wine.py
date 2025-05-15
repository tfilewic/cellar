"""
Wine model.

Represents a wine entry.
Each wine belongs to a producer.
"""

from models import db

class Wine(db.Model):
    __tablename__ = "wines"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    vintage = db.Column(db.Integer)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    varietal = db.Column(db.String(100))    #ex: "Chardonnay", "Bordeaux Blend"
    color = db.Column(db.String(50))    #ex: "Red", "White", "Rosé"
    type = db.Column(db.String(100))    #ex: "Still", "Sparkling", "Dessert", "Fortified"
    producer_id = db.Column(db.Integer, db.ForeignKey("producers.id"), nullable=False)