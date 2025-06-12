"""
CSV I/O utilities for database population and export.

"""

from models.wine import Wine
from models.producer import Producer
from models.region import Region
from models.country import Country 
from models import db


CSV_HEADERS = ["id", "name", "vintage", "varietal", "color", "type", "rating", "quantity",
             "producer", "region", "country"]


def clear_database():
    """
    Delete all records from Wine, Producer, Region, and Country tables.

    This function should be used before inserting new data from CSV to avoid duplicates.
    Commits the session after deletion.
    """
    db.session.query(Wine).delete()
    db.session.query(Producer).delete()
    db.session.query(Region).delete()
    db.session.query(Country).delete()
    db.session.commit()

    
def insert_countries(rows) -> dict:
    """
    Insert distinct countries from CSV rows.

    Args:
        rows (list[dict]): Parsed CSV rows.

    Returns:
        dict: Mapping of country name to database ID.
    """
    country_map = {}
    countries = {r["country"].strip() for r in rows}
    for name in countries:
        c = Country(name=name)
        db.session.add(c)
        db.session.flush()
        country_map[name] = c.id
    return country_map


def insert_regions(rows, country_map) -> dict:
    """
    Insert distinct regions from CSV rows.

    Args:
        rows (list[dict]): Parsed CSV rows.
        country_map (dict): Mapping of country names to IDs.

    Returns:
        dict: Mapping of region name to database ID.
    """
    region_map = {}
    regions = {(r["region"].strip(), r["country"].strip()) for r in rows}
    for region_name, country_name in regions:
        r = Region(name=region_name, country_id=country_map[country_name])
        db.session.add(r)
        db.session.flush()
        region_map[region_name] = r.id
    return region_map


def insert_producers(rows, region_map) -> dict:
    """
    Insert distinct producers from CSV rows.

    Args:
        rows (list[dict]): Parsed CSV rows.
        region_map (dict): Mapping of region names to IDs.

    Returns:
        dict: Mapping of producer name to database ID.
    """
    producer_map = {}
    producers = {(r["producer"].strip(), r["region"].strip()) for r in rows}
    for producer_name, region_name in producers:
        p = Producer(name=producer_name, region_id=region_map[region_name])
        db.session.add(p)
        db.session.flush()
        producer_map[producer_name] = p.id
    return producer_map

def insert_wines(rows, producer_map):
    """
    Insert wines from CSV rows.

    Args:
        rows (list[dict]): Parsed CSV rows.
        producer_map (dict): Mapping of producer names to IDs.
    """
    for row in rows:
        wine = Wine(
            name = row["name"].strip(),
            vintage = row["vintage"],
            varietal = row["varietal"],
            color = row["color"],
            type = row["type"],
            rating = row["rating"],
            quantity = row["quantity"],
            producer_id = producer_map[row["producer"].strip()]
        )
        db.session.add(wine)