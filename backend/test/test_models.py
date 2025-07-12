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


@pytest.mark.parametrize("id", [None, ["7"], object()])
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


#Producer

@pytest.mark.parametrize("name", [None, "", "     "])
def test_producer_validate_name_empty(name) :
    with pytest.raises(ValueError, match="Producer name is required"):
        Producer.validate_name(name)

@pytest.mark.parametrize("name", ["z" * 101])
def test_producer_validate_name_too_long(name) :
    with pytest.raises(ValueError, match=f"Producer name '{name}' too long"):
         Producer.validate_name(name)

@pytest.mark.parametrize("name, expected", [("z" * 100, "z" * 100), 
    ("  Domaine de la Romanée-Conti ", "Domaine de la Romanée-Conti"), ("Ridge", "Ridge")])
def test_producer_validate_name_valid(name, expected) :
    assert Producer.validate_name(name) == expected


@pytest.mark.parametrize("id", [None, [7], object()])
def test_producer_validate_region_id_not_int(id) :
    with pytest.raises(ValueError, match=re.escape(f"Invalid region_id: {id}.  Must be integer.")):
        Producer.validate_region_id(id)

@pytest.mark.parametrize("id", ["0", 0, -2341])
def test_producer_validate_region_id_not_positive(id) :
    with pytest.raises(ValueError, match=re.escape(f"Invalid region_id: {id}. Must be greater than 0.")):
        Producer.validate_region_id(id)

@pytest.mark.parametrize("id,expected", [(1, 1), ("1", 1), (2341, 2341)])
def test_producer_validate_region_id_valid(id, expected) :
    assert Producer.validate_region_id(id) == expected


#Wine

@pytest.mark.parametrize("quantity", [None, "", "bananas"])
def test_wine_validate_quantity_not_int(quantity) :
    with pytest.raises(ValueError, match=re.escape(f"Invalid quantity: {quantity}.  Must be integer.")):
        Wine.validate_quantity(quantity)

@pytest.mark.parametrize("quantity", [-1, 1001])
def test_wine_validate_quantity_out_of_range(quantity) :
    with pytest.raises(ValueError, match=re.escape(f"Invalid quantity: {quantity}. Out of range 0 - 1000.")):
        Wine.validate_quantity(quantity)

@pytest.mark.parametrize("quantity", [0, 288, 1000])
def test_wine_validate_quantity_valid(quantity) :
    assert Wine.validate_quantity(quantity) == quantity


@pytest.mark.parametrize("color", [None, "", "     "])
def test_wine_validate_color_empty(color) :
    assert Wine.validate_color(color) == None

@pytest.mark.parametrize("color", ["Purple"])
def test_wine_validate_color_invalid(color) :
    with pytest.raises(ValueError, match=re.escape(f"Invalid color: {color}")):
        Wine.validate_color(color)

@pytest.mark.parametrize("color, expected", [("  red ", "Red"), ("White", "White"), 
    ("rOSÉ", "Rosé"), ("orange", "Orange")])
def test_wine_validate_color_valid(color, expected) :
    assert Wine.validate_color(color) == expected


@pytest.mark.parametrize("name", [None, "", "     "])
def test_wine_validate_name_empty(name) :
    with pytest.raises(ValueError, match="Wine Name is required"):
        Wine.validate_name(name)

@pytest.mark.parametrize("name", ["z" * 256])
def test_wine_validate_name_too_long(name) :
    with pytest.raises(ValueError, match=f"Wine name '{name}' too long"):
        Wine.validate_name(name)

@pytest.mark.parametrize("name, expected", [("z" * 255, "z" * 255), ("Insignia", "Insignia"),
    ("  Cuvée Sir Winston Churchill   ", "Cuvée Sir Winston Churchill")])
def test_wine_validate_name_valid(name, expected) :
    assert Wine.validate_name(name) == expected


@pytest.mark.parametrize("vintage", [None, "", "NV"])
def test_wine_validate_vintage_nonvintage(vintage) :
    assert Wine.validate_vintage(vintage) == "nv"

@pytest.mark.parametrize("vintage", ["two-thousand", "1799", "2030"])
def test_wine_validate_vintage_invalid(vintage) :
    with pytest.raises(ValueError, match=f"Invalid vintage: {vintage}"):
        Wine.validate_vintage(vintage)

@pytest.mark.parametrize("vintage, expected", [("1800", "1800"), ("2025", "2025")])
def test_wine_validate_vintage_valid(vintage, expected) :
    assert Wine.validate_vintage(vintage) == expected

 
@pytest.mark.parametrize("varietal", [None, "", "     "])
def test_wine_validate_varietal_none(varietal) :
    assert Wine.validate_varietal(varietal) == None

@pytest.mark.parametrize("varietal", ["z" * 101])
def test_wine_validate_varietal_too_long(varietal) :
    with pytest.raises(ValueError, match=f"Varietal '{varietal}' too long"):
        Wine.validate_varietal(varietal)

@pytest.mark.parametrize("varietal, expected", [("  Pinot Noir ", "Pinot Noir"), ("Tempranillo", "Tempranillo")])
def test_wine_validate_varietal_valid(varietal, expected) :
    assert Wine.validate_varietal(varietal) == expected


@pytest.mark.parametrize("type", [None, "", "     "])
def test_wine_validate_type_none(type) :
    assert Wine.validate_type(type) == None

@pytest.mark.parametrize("type", ["Porto"])
def test_wine_validate_type_invalid(type) :
    with pytest.raises(ValueError, match=f"Invalid type: {type}"):
        Wine.validate_type(type)

@pytest.mark.parametrize("type, expected", [("still ", "Still"), (" Sparkling",  "Sparkling"), 
    ("Dessert", "Dessert"), ("FORTIFIED", "Fortified")])
def test_wine_validate_type_valid(type, expected) :
    assert Wine.validate_type(type) == expected


@pytest.mark.parametrize("id", [None, ["7"], object()])
def test_wine_validate_producer_id_not_int(id) :
    with pytest.raises(ValueError, match=re.escape(f"Invalid producer_id: {id}.  Must be integer.")):
        Wine.validate_producer_id(id)

@pytest.mark.parametrize("id", ["0", 0, -2341])
def test_wine_validate_producer_id_not_positive(id) :
    with pytest.raises(ValueError, match=re.escape(f"Invalid producer_id: {id}. Must be greater than 0.")):
        Wine.validate_producer_id(id)

@pytest.mark.parametrize("id,expected", [(1, 1), ("1", 1), (2341, 2341)])
def test_wine_validate_producer_id_valid(id, expected) :
    assert Wine.validate_producer_id(id) == expected
