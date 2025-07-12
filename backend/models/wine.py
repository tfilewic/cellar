"""
Wine model.

Represents a wine entry.
Each wine belongs to a producer.
"""

from models import db
from datetime import datetime

NV = 'nv'   #non-vintage

class Wine(db.Model):
    __tablename__ = "wines"
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    vintage = db.Column(db.String(10), default=NV, nullable=False)
    varietal = db.Column(db.String(100))    #ex: "Chardonnay", "Bordeaux Blend"
    color = db.Column(db.String(50))    #ex: "Red", "White", "Rosé"
    type = db.Column(db.String(100))    #ex: "Still", "Sparkling", "Dessert", "Fortified"
    producer_id = db.Column(db.Integer, db.ForeignKey("producers.id"), nullable=False)
    rating = db.Column(db.Integer)  #scraped upon insert/update
    producer = db.relationship("Producer", backref="wines") #link to Producer

    @staticmethod
    def validate_quantity(quantity) -> int:
        """Validate wine quantity.

        Args:
            quantity: Input value to validate.

        Returns:
            int: Validated quantity.

        Raises:
            ValueError: If quantity is not an integer between 0 and 1000.
        """

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid quantity: {quantity}.  Must be integer.")
        MAX = 1000
        if not 0 <= quantity <= MAX:
            raise ValueError(f"Invalid quantity: {quantity}. Out of range 0 - {MAX}.")
        return quantity

    def validate_color(color: str) -> str:
        """Validate wine color.

        Args:
            color: Input string to validate.

        Returns:
            str or None: Capitalized valid color or None if blank.

        Raises:
            ValueError: If color is not one of the allowed values.
        """

        if not color or not color.strip():
            return None
        ALLOWED = {"Red", "White", "Rosé", "Orange"}
        color = color.strip().capitalize()
        if not color in ALLOWED:
            raise ValueError(f"Invalid color: {color}")
        return color

    @staticmethod
    def validate_name(name: str) -> str:
        """Validate wine name.

        Args:
            name: Input string to validate.

        Returns:
            str: Trimmed name.

        Raises:
            ValueError: If name is empty or exceeds 255 characters.
        """

        if not name or not name.strip():
            raise ValueError("Wine Name is required")
        if len(name) > 255:
            raise ValueError(f"Wine name '{name}' too long")
        return name.strip()

    @staticmethod
    def validate_vintage(vintage: str) -> str:
        """Validate wine vintage.

        Args:
            vintage: Input value to validate.

        Returns:
            str: String year or 'nv'.

        Raises:
            ValueError: If vintage is invalid or out of range.
        """   
        value = vintage
        if not vintage or str(vintage).strip().lower() == NV:
            return NV
        try:
            vintage = int(vintage)
        except (ValueError):
            raise ValueError(f"Invalid vintage: {value}")     
        min_year = 1800
        max_year = datetime.now().year
        if not min_year <= vintage <= max_year:
            raise ValueError(f"Invalid vintage: {value}")  
        return str(vintage)

    @staticmethod
    def validate_varietal(varietal: str) -> str:
        """Validate wine varietal.

        Args:
            varietal: Input string to validate.

        Returns:
            str or None: Trimmed varietal or None if blank.

        Raises:
            ValueError: If varietal exceeds 100 characters.
        """

        if not varietal or not varietal.strip():
            return None
        if len(varietal) > 100:
            raise ValueError(f"Varietal '{varietal}' too long")
        return varietal.strip()

    @staticmethod
    def validate_type(type: str) -> str:
        """Validate wine type.

        Args:
            type: Input string to validate.

        Returns:
            str or None: Capitalized type or None if blank.

        Raises:
            ValueError: If type is not one of the allowed values.
        """
        value = type
        if not type or not type.strip():
            return None
        ALLOWED = {"Still", "Sparkling", "Dessert", "Fortified"}
        type = type.strip().capitalize()
        if not type in ALLOWED:
            raise ValueError(f"Invalid type: {value}")
        return type

    @staticmethod
    def validate_producer_id(producer_id) -> int:
        """Validate producer ID.

        Args:
            producer_id: Input value to validate.

        Returns:
            int: Validated producer ID.

        Raises:
            ValueError: If producer_id is not a positive integer.
        """

        try:
            producer_id = int(producer_id)
        except (TypeError, ValueError):
            raise ValueError(f"Invalid producer_id: {producer_id}.  Must be integer.")
        if not 0 < producer_id:
            raise ValueError(f"Invalid producer_id: {producer_id}. Must be greater than 0.") 
        return producer_id
