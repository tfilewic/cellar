"""
API route tests.

Unit tests API endpoints.
"""

import pytest
from app import app
from io import BytesIO
import pandas as pd



def test_get_wines_200(client, data):
    response = client.get("/wines")
    assert response.status_code == 200


def test_get_wine_200(client, data):
    response = client.get("/wines/1")
    assert response.status_code == 200

def test_get_wine_404(client, data):
    response = client.get("/wines/2")
    assert response.status_code == 404


def test_add_wine_201(client, data):
    payload = {
        "name": data["wine"].name,
        "vintage": str(int(data["wine"].vintage) + 1),  #increment vintage of existing wine
        "producer_id": data["producer"].id
    }
    response = client.post("/wines", json=payload)
    assert response.status_code == 201

def test_add_wine_400(client, data):
    payload = {
        "name": data["wine"].name,
        "vintage": str(int(data["wine"].vintage) + 1),
        "producer_id": 7    #pid doesn't exist
    }
    response = client.post("/wines", json=payload)
    assert response.status_code == 400

def test_add_wine_409(client, data):
    payload = {
        "name": data["wine"].name,
        "vintage": data["wine"].vintage,
        "producer_id": data["producer"].id
    }
    response = client.post("/wines", json=payload)
    assert response.status_code == 409


def test_update_quantity_200(client, data):
    payload = {
        "id" : 1,
        "quantity" : 7
    }
    response = client.put("/wines", json=payload)
    assert response.status_code == 200

def test_update_quantity_400(client, data):
    payload = {
        "id" : 1,
        "quantity" : -1
    }
    response = client.put("/wines", json=payload)
    assert response.status_code == 400

def test_update_quantity_404(client, data):
    payload = {
        "id" : 2,
        "quantity" : 7
    }
    response = client.put("/wines", json=payload)
    assert response.status_code == 404


def test_remove_wine_200(client, data):
    response = client.delete("/wines/1")
    assert response.status_code == 200

def test_remove_wine_404(client, data):
    response = client.delete("/wines/2")
    assert response.status_code == 404


def test_get_producers_200(client, data):
    response = client.get("/producers")
    assert response.status_code == 200


def test_get_producer_200(client, data):
    response = client.get("/producers/1")
    assert response.status_code == 200

def test_get_producer_404(client, data):
    response = client.get("/producers/2")
    assert response.status_code == 404


def test_get_regions_200(client, data):
    response = client.get("/regions")
    assert response.status_code == 200


def test_get_region_200(client, data):
    response = client.get("/regions/1")
    assert response.status_code == 200

def test_get_region_404(client, data):
    response = client.get("/regions/2")
    assert response.status_code == 404


def test_get_countries_200(client, data):
    response = client.get("/countries")
    assert response.status_code == 200


def test_get_country_200(client, data):
    response = client.get("/countries/1")
    assert response.status_code == 200

def test_get_country_404(client, data):
    response = client.get("/countries/2")
    assert response.status_code == 404


def test_csv_upload_200(client, csv_file):
    data = {"file": (csv_file, "test.csv")}
    response = client.post("/csv", data=data, content_type="multipart/form-data")
    assert response.status_code == 200

def test_csv_upload_400(client, csv_file):
    data = {"file": (csv_file, "test.csz")}
    response = client.post("/csv", data=data, content_type="multipart/form-data")
    assert response.status_code == 400


def test_csv_download_200(client, csv_file, uploaded_csv):
   
    response = client.get("/csv")
    assert response.status_code == 200

    '''
    with open("test/output.csv", "w", encoding="utf-8") as f:
        f.write(response.data.decode("utf-8"))
    '''

    df_uploaded = pd.read_csv("test/wines.csv")
    df_downloaded = pd.read_csv(BytesIO(response.data))
    assert df_uploaded.equals(df_downloaded)


