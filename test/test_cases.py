import inspect
from fastapi import FastAPI
from fastapi.testclient import TestClient

from sabenco import app, get_db

client = TestClient(app)

"""
def test_read_users_me():
    response = client.get("/users/me", headers={"Authorization":"Bearer admin1"})
    assert response.status_code == 200
    assert response != ''
"""
    
def test_register():
    response = client.post(
        "users/register",
        #headers={"Authorization":"Bearer admin1"}
        json= {
            "username": "anystring",
            "usermail": "anystring",
            "password": "anystring"
        }
    )
    assert response.status_code == 200

