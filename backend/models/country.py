"""
Country model.

Represents a country entry.
Referenced by producers.
"""

from models import db
import pycountry

class Country(db.Model):
    __tablename__ = "countries"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    COUNTRY_MAP = {c.name.lower(): c.name for c in pycountry.countries}


    @staticmethod
    def validate_name(name: str) -> str:
        """Validate country name.

        Args:
            name: Input string to validate.

        Returns:
            str: Trimmed name.

        Raises:
            ValueError: If name is empty or exceeds 100 characters.
        """
        
        if not name or not name.strip():
            raise ValueError("Country name is required")
        lower = name.strip().lower()
        if not lower in Country.COUNTRY_MAP:
            raise ValueError(f"Invalid country name: '{name}'")
        return Country.COUNTRY_MAP[lower]
