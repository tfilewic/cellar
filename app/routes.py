"""
REST API routes.

Defines endpoints for wines, producers, regions, and countries.
"""

from flask import request, jsonify, Response
from app import app
from models.wine import Wine
from models.producer import Producer
from models.region import Region
from models.country import Country 
from models import db
from scraper.scraper import scrape_rating
import pandas as pd
import csv
import csv_io.csv_io as csvio



#GET /wines
@app.route("/wines", methods=["GET"])
def get_wines():
    """Retrieve all wine entries.

    Returns:
        JSON response with a list of all wines and HTTP 200.
    """

    wines = Wine.query.all()
    result = [
        {"id": wine.id,
        "quantity": wine.quantity,
        "name": wine.name,
        "vintage": wine.vintage,
        "varietal": wine.varietal,
        "color": wine.color,
        "type": wine.type,
        "producer_id": wine.producer_id,
        "rating": wine.rating} 
        for wine in wines]
    return jsonify(result), 200


@app.route("/wines/<int:id>", methods=["GET"])
def get_wine(id):
    """Retrieve a single wine by ID.

    Args:
        id (int): Wine ID.

    Returns:
        JSON response with wine data and HTTP 200
        HTTP 404 if not found
    """

    wine = Wine.query.get_or_404(id)
    result = {
        "id": wine.id,
        "quantity": wine.quantity,
        "name": wine.name,
        "vintage": wine.vintage,
        "varietal": wine.varietal,
        "color": wine.color,
        "type": wine.type,
        "producer_id": wine.producer_id,
        "rating": wine.rating
    }
    return jsonify(result), 200


@app.route("/wines", methods=["POST"])
def add_wine():
    """Create a new wine entry.

    Parses JSON request, validates fields, checks for duplicates,
    scrapes rating, and inserts the wine.

    Returns:
        JSON response with new wine ID and HTTP 201 on success.
        HTTP 400 or 409 on error.
    """

    #get request
    data = request.get_json()

    #validate required fields
    try:
        name = Wine.validate_name(data.get("name"))
        vintage = Wine.validate_vintage(data.get("vintage"))
        producer_id = Wine.validate_producer_id(data.get("producer_id"))

        #get producer name
        producer = Producer.query.get(producer_id)
        if not producer:
            raise ValueError("Producer not found")
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    #check if duplicate
    existing = Wine.query.filter_by(
        name = name,
        vintage = vintage,
        producer_id = producer_id
    ).first()
    if existing:
        return jsonify({"error": "Duplicate Entry"}), 409
    
    #build entry
    try:
        quantity = data.get("quantity")
        if quantity is not None:
            quantity = Wine.validate_quantity(quantity)
        varietal = data.get("varietal")
        if varietal is not None:
            varietal = Wine.validate_varietal(varietal)
        color = data.get("color")
        if color is not None:
            color = Wine.validate_color(color)
        wine_type = data.get("type")
        if wine_type is not None:
            wine_type = Wine.validate_type(wine_type)
        rating = scrape_rating(name, vintage, producer.name)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
    wine = Wine(
        quantity = quantity,
        name = name,
        vintage = vintage,
        varietal = varietal,
        color = color,
        type = wine_type,
        producer_id = producer_id,
        rating = rating
    )
    db.session.add(wine)
    db.session.commit()
    
    return jsonify({"id": wine.id, "message": "Wine added successfully"}), 201


@app.route("/wines", methods=["PUT"])
def update_quantity():
    """Update quantity of an existing wine.

    Parses JSON request and updates the quantity for the given wine ID.

    Returns:
        JSON response with confirmation message and HTTP 200.
        HTTP 400 or 404 on error.
    """

    #check for id
    data = request.get_json()
    id = data.get("id")
    if not id:
        return jsonify({"error": "Missing wine id"}), 400
    
    wine = Wine.query.get_or_404(id)    #fetch wine

    #update quantiy
    try:
        quantity = Wine.validate_quantity(data.get("quantity"))
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
     
    wine.quantity = quantity
    db.session.commit()

    return jsonify({ "message": f"Wine id {id} updated to {quantity}"}), 200
    

@app.route("/wines/<int:id>", methods=["DELETE"])
def remove_wine(id):
    """Delete a wine entry by ID.

    Args:
        id (int): Wine ID.

    Returns:
        JSON response confirming deletion and HTTP 200.
        HTTP 404 if not found.
    """

    wine = Wine.query.get_or_404(id)
    db.session.delete(wine)
    db.session.commit()
    return jsonify({"message": f"Wine id {id} deleted"}), 200


@app.route("/producers", methods=["GET"])
def get_producers():
    """Retrieve all producers.

    Returns:
        JSON response with a list of all producers and HTTP 200.
    """

    producers = Producer.query.all()
    result = [
        {"id": producer.id,
        "name": producer.name,
        "region_id": producer.region_id} 
        for producer in producers]
    return jsonify(result), 200
    

@app.route("/producers/<int:id>", methods=["GET"])
def get_producer(id):
    """Retrieve a single producer by ID.

    Args:
        id (int): Producer ID.

    Returns:
        JSON response with producer data and HTTP 200.
        HTTP 404 if not found.
    """

    producer = Producer.query.get_or_404(id)
    result = {
        "id": producer.id,
        "name": producer.name,
        "region_id": producer.region_id
    }
    return jsonify(result), 200


@app.route("/regions", methods=["GET"])
def get_regions():
    """Retrieve all regions.

    Returns:
        JSON response with a list of all regions and HTTP 200.
    """

    regions = Region.query.all()
    result = [
        {"id": region.id,
        "name": region.name,
        "country_id": region.country_id} 
        for region in regions]
    return jsonify(result), 200


@app.route("/regions/<int:id>", methods=["GET"])
def get_region(id):
    """Retrieve a single region by ID.

    Args:
        id (int): Region ID.

    Returns:
        JSON response with region data and HTTP 200.
        HTTP 404 if not found.
    """

    region = Region.query.get_or_404(id)
    result = {
        "id": region.id,
        "name": region.name,
        "country_id": region.country_id
    }
    return jsonify(result), 200


@app.route("/countries", methods=["GET"])
def get_countries():
    """Retrieve all countries.

    Returns:
        JSON response with a list of all countries and HTTP 200.
    """

    countries = Country.query.all()
    result = [
        {"id": country.id,
        "name": country.name}
        for country in countries]
    return jsonify(result), 200


@app.route("/countries/<int:id>", methods=["GET"])
def get_country(id):
    """Retrieve a single country by ID.

    Args:
        id (int): Country ID.

    Returns:
        JSON response with country data and HTTP 200.
        HTTP 404 if not found.
    """

    country = Country.query.get_or_404(id)
    result = {
        "id": country.id,
        "name": country.name
    }
    return jsonify(result), 200


@app.route("/csv", methods=["GET"])
def download_csv():
    """Download all wine data as CSV.

    Returns:
        CSV file response with HTTP 200.
        Each row includes wine, producer, region, and country details.
    """

    wines = (db.session.query(
        Wine.name,
        Wine.vintage,
        Wine.varietal,
        Wine.color,
        Wine.type,
        Wine.rating,
        Wine.quantity,
        Producer.name,
        Region.name,
        Country.name
    ).select_from(Wine)
    .join(Producer, Wine.producer_id == Producer.id)
    .join(Region, Producer.region_id == Region.id)
    .join(Country, Region.country_id == Country.id)
    .order_by(Wine.id)
    .all())


    dataframe = pd.DataFrame(wines, columns=csvio.CSV_HEADERS)
    csv_data = dataframe.to_csv(index=False)

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=wines.csv"},
        status=200
    )

@app.route("/csv", methods=["POST"])
def upload_csv():
    """Upload and replace wine database from CSV file.

    Expects a multipart/form-data request with a '.csv' file named 'file'.
    Validates headers, clears existing data, and inserts new countries, regions,
    producers, and wines in dependency order.

    Returns:
        JSON response with confirmation message and HTTP 200.
        HTTP 400 on invalid or missing file.
    """

    #check if file is in request
    if "file" not in request.files:
        return jsonify({"error": "No file in request"}), 400
    
    #get file from request
    file = request.files["file"]

    #validate extension
    if not file.filename.lower().endswith(".csv"):
        return jsonify({"error": "Invalid file type"}), 400
    
    #read to dataframe
    try:
        df = pd.read_csv(file)
    except Exception as e:
        return jsonify({"error": "Failed to parse file"}), 400

    #validate headers
    if list(df.columns) != csvio.CSV_HEADERS:
        return jsonify({"error": "Invalid CSV headers"}), 400
    
    #convert to dict
    rows = df.to_dict(orient="records")

    #wipe db
    csvio.clear_database()

    #insert each distinct country and map ids to names
    country_map = csvio.insert_countries(rows)

    #insert each distinct region and map ids to names
    region_map = csvio.insert_regions(rows, country_map)

    #insert each distinct producer and map ids to names
    producer_map = csvio.insert_producers(rows, region_map)

    #insert all wines
    csvio.insert_wines(rows, producer_map)
    
    db.session.commit()
    
    return jsonify(message="File uploaded successfully"), 200