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
    if len(name) > 100:
        raise ValueError(f"Country name '{name}' is too long")
    return name
