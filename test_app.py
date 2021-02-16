from flask import Flask
import json
import pytest
import math
from handlers.routes import configure_routes

#Test route 1
def test_route_one():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = "/api/ping"
    response = client.get(url)
    assert response.get_data() == b'{"success":true}\n'
    assert response.status_code == 200
#Test url with no tags
def test_no_tags():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = "/api/posts"
    response = client.get(url)
    assert response.status_code == 400
    assert response.get_data() == b'{"error":"Missing tags parameter"}\n'
#Test url with one tag
def test_1_tag():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = "/api/posts?tags=science"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json["posts"]
    for p in response.json["posts"]:
        assert "science" in p["tags"]
#Test url with two tags
def test_2_tags():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = "/api/posts?tags=science,tech"
    response = client.get(url)
    assert response.status_code == 200
    assert response.json["posts"]
    for p in response.json["posts"]:
        assert "science" in p["tags"] or "tech" in p["tags"]
#Test Sort and Ascend
def test_sort():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = "/api/posts?tags=science,tech&sortBy=popularity"
    response = client.get(url)
    previous = 0
    assert response.status_code == 200
    for p in response.json["posts"]:
        assert p['popularity'] >= previous
        previous = p['popularity']
#Test Descend 
def test_desc():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = "/api/posts?tags=science,tech&sortBy=popularity&direction=desc"
    response = client.get(url)
    previous = math.inf
    assert response.status_code == 200
    for p in response.json["posts"]:
        assert p['popularity'] <= previous
        previous = p['popularity']
#Test invalid sortBy parameter
def test_sort_false():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = "/api/posts?tags=science,tech&sortBy=hghgfk"
    response = client.get(url)
    assert response.status_code == 400
    assert b'{"error": "Invalid sortBy parameter"}\n'
#Test invalid direction parameter
def test_dir_false():
    app = Flask(__name__)
    configure_routes(app)
    client = app.test_client()
    url = "/api/posts?tags=science,tech&sortBy=popularity&direction=ghggh"
    response = client.get(url)
    assert response.status_code == 400
    assert b'{"error": "Invalid direction parameter"}\n'