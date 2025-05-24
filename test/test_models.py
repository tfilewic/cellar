"""
Model validation tests.

Unit tests for data validation functions defined in model classes.
Covers country, region, producer, and wine models.
"""

import pytest
import re
from models.country import Country
from models.region import Region
from models.producer import Producer
from models.wine import Wine

# Country
@pytest.mark.parametrize("name", [None, "", "     "])
def test_country_validate_name_empty(name) :
    with pytest.raises(ValueError, match="Country name is required"):
        Country.validate_name(name)

@pytest.mark.parametrize("name", ["Cranada"])
def test_country_validate_name_invalid(name) :
    with pytest.raises(ValueError, match=f"Invalid country name: '{name}'"):
        Country.validate_name(name)

@pytest.mark.parametrize("name,expected", [("France", "France"),
    ("   France ", "France"), ("uNiTed sTAtes", "United States")])
def test_country_validate_name_valid(name, expected) :
    assert Country.validate_name(name) == expected
    
#Region
@pytest.mark.parametrize("name", [None, "", "     "])    
def test_region_validate_name_empty(name) :
    with pytest.raises(ValueError, match="Region name is required"):
        Region.validate_name(name)

@pytest.mark.parametrize("name", ["z" * 101])
def test_region_validate_name_too_long(name) :
    with pytest.raises(ValueError, match=f"Region name '{name}' too long"):
        Region.validate_name(name)

@pytest.mark.parametrize("name, expected", [("z" * 100, "z" * 100), 
    (" Côte du Rhône-Villages  ", "Côte du Rhône-Villages"), ("Rioja", "Rioja")])
def test_region_validate_name_valid(name, expected) :
    assert Region.validate_name(name) == expected

@pytest.mark.parametrize("id", [None, [7], object()])
def test_region_validate_country_id_not_int(id) :
    with pytest.raises(ValueError, match=re.escape(f"Invalid country_id: '{id}'.  Must be integer.")):
        Region.validate_country_id(id)

@pytest.mark.parametrize("id", ["0", 0, -2341])
def test_region_validate_country_id_not_positive(id) :
    with pytest.raises(ValueError, match=re.escape(f"Invalid country_id: '{id}'. Must be greater than 0.")):
        Region.validate_country_id(id)

@pytest.mark.parametrize("id,expected", [(1, 1), ("1", 1), (2341, 2341)])
def test_region_validate_country_id_valid(id, expected) :
    assert Region.validate_country_id(id) == expected


def test_producer_validate_name() :
    pass

def test_producer_validate_region_id() :
    pass

def test_producer_validate_name() :
    pass

def test_wine_validate_quantity() :
    pass

def test_wine_validate_color() :
    pass

def test_wine_validate_name() :
    pass

def test_wine_validate_vintage() :
    pass

def test_wine_validate_varietal() :
    pass

def test_wine_validate_type() :
    pass

def test_wine_validate_producer_id() :
    pass