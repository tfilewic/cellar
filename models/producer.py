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


@staticmethod
def validate_name(name: str) -> str:
    """Validate producer name.

    Args:
        name: Input string to validate.

    Returns:
        str: Trimmed name.

    Raises:
        ValueError: If name is empty or exceeds 100 characters.
    """

    if not name or not name.strip():
        raise ValueError("Producer name is required")
    if len(name) > 100:
        raise ValueError(f"Producer name '{name}' too long")
    return name

@staticmethod
def validate_region_id(region_id) -> int:
    """Validate region ID.

    Args:
        region_id: Input value to validate.

    Returns:
        int: Validated region ID.

    Raises:
        ValueError: If region_id is not a positive integer.
    """

    try:
        region_id = int(region_id)
    except (TypeError, ValueError):
        raise ValueError(f"Invalid region_id: {region_id}.  Must be integer.")
    if not 0 < region_id:
        raise ValueError(f"Invalid region_id: {region_id}. Must be greater than 0.") 
    return region_id