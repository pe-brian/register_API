from flask import jsonify
from flask.testing import FlaskClient
import pytest

from app import app
from src.helpers import field


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@app.route("/test", methods=["POST"])
@field("test_field", str, required=True)
def new_route(test_field: str):
    return jsonify(success=True), 200


def test_with_required_field(client: FlaskClient):
    response = client.post("/test", json={"test_field": "value"})
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["success"]


def test_without_required_field(client: FlaskClient):
    response = client.post("/test", json={})
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["message"] == "test_field is required"
