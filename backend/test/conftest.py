"""
Pytest fixtures.

Provides a test client and database setup for Flask API tests.
"""

import pytest
from app import app, db
from models.country import Country
from models.region import Region
from models.producer import Producer
from models.wine import Wine
from models import db


@pytest.fixture
def client():
    app.config["TESTING"] = True    #enable test mode
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"    #use in-memory sqlite
    with app.test_client() as client:
        with app.app_context():
            db.create_all() #create tables
            yield client    #run tests with client
            db.session.remove() #close sessions to release db
            db.drop_all()   #clean up db


@pytest.fixture
def data(client):
    c = Country(name="France")
    db.session.add(c)
    db.session.flush()

    r = Region(name="Champagne", country_id=c.id)
    db.session.add(r)
    db.session.flush()

    p = Producer(name="Pol Roger", region_id=r.id)
    db.session.add(p)
    db.session.flush()

    w = Wine(name="Brut", vintage="2010", producer_id=p.id)
    db.session.add(w)
    db.session.commit()

    return {"country": c, "region": r, "producer": p, "wine": w}


@pytest.fixture
def data2(client):
    c = Country(name="Canada")
    db.session.add(c)
    db.session.flush()

    r = Region(name="Okanagan Valley", country_id=c.id)
    db.session.add(r)
    db.session.flush()

    p = Producer(name="Painted Rock", region_id=r.id)
    db.session.add(p)
    db.session.flush()


@pytest.fixture
def csv_file():
    with open("test/wines.csv", "rb") as file:
        yield file

@pytest.fixture
def uploaded_csv(client, csv_file):
    data = {"file": (csv_file, "test.csv")}
    client.post("/csv", data=data, content_type="multipart/form-data")