"""
Producer model.

Represents a wine producer entry.
Each producer belongs to a region.
"""

from models import db

class Producer(db.Model):
    __tablename__ = "producers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    region_id = db.Column(db.Integer, db.ForeignKey("regions.id"), nullable=False)