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
    country = db.relationship("Country", backref="regions") #link to Country



    @staticmethod
    def validate_name(name: str) -> str:
        """Validate region name.

        Args:
            name: Input string to validate.

        Returns:
            str: Trimmed name.

        Raises:s
            ValueError: If name is empty or exceeds 100 characters.
        """

        if not name or not name.strip():
            raise ValueError("Region name is required")
        name = name.strip()
        if len(name) > 100:
            raise ValueError(f"Region name '{name}' too long")
        return name

    @staticmethod
    def validate_country_id(country_id) -> int:
        """Validate country ID.

        Args:
            country_id: Input value to validate.

        Returns:
            int: Validated country ID.

        Raises:
            ValueError: If country_id is not a positive integer.
        """

        try:
            converted = int(country_id)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid country_id: '{country_id}'.  Must be integer.")
        if not 0 < converted:
            raise ValueError(f"Invalid country_id: '{country_id}'. Must be greater than 0.") 
        return converted