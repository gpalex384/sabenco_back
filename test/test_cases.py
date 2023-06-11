from fastapi.testclient import TestClient
from numpy import size
from database import SessionLocal
from sabenco import app
from sql.restore_test_db import restore_test_database

import crud

client = TestClient(app)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

restore_test_database()

##########
# Register a new user
##########
def test_register_success():
    response = client.post(
        "users/register",
        #headers={"Authorization":"Bearer admin1"}
        json= {
            "username": "visitor",
            "usermail": "visitor@sabenco.com",
            "password": "visitor"
        }
    )
    assert response.status_code == 200
    assert list(response.json()) == ["username","usermail"]

def test_register_no_username():
    userdata = {
            "usermail": "visitor@sabenco.com",
            "password": "visitor"
        }
    response = client.post(
        "users/register",
        json= userdata
    )
    assert response.status_code == 422 # Unprocessable Entity
    assert response.json()['detail'][0]['msg'] == 'field required'

def test_register_no_usermail():
    userdata = {
            "username": "visitor",
            "password": "visitor"
        }
    response = client.post(
        "users/register",
        json= userdata
    )
    assert response.status_code == 422 # Unprocessable Entity
    assert response.json()['detail'][0]['msg'] == 'field required'

def test_register_incorrect_usermail():
    userdata = {
            "username": "visitor",
            "usermail": "visitor.com",
            "password": "visitor"
        }
    response = client.post(
        "users/register",
        json= userdata
    )
    assert response.status_code == 400 # Unprocessable Entity
    assert response.json() == {"detail":"Incorrect email format"}

def test_register_no_password():
    userdata = {
            "username": "visitor",
            "usermail": "visitor@sabenco.com",
        }
    response = client.post(
        "users/register",
        json= userdata
    )
    assert response.status_code == 422 # Unprocessable Entity
    assert response.json()['detail'][0]['msg'] == 'field required'

##########
# Assign an editor role to the user
##########

# Create editor user
def test_assign_editor_role_success():
    client.post(
        "users/register",
        #headers={"Authorization":"Bearer admin1"}
        json= {
            "username": "editor",
            "usermail": "editor@sabenco.com",
            "password": "editor"
        }
    )
    editor_id = crud.get_user_by_username(SessionLocal(), "editor").id
    visitor_id = crud.get_user_by_username(SessionLocal(), "visitor").id
    role_id = crud.get_role_by_name(SessionLocal(), "editor").id
    response = client.post(
        "users/%s/role/%s"%(editor_id,role_id),
        headers={"Authorization":"Bearer admin1"}
    )
    assert response.status_code == 200
    assert response.json() == {"ok": "The user 'editor' has been linked to the role 'editor'"}

def test_assign_editor_role_incorrect_user():
    role_id = crud.get_role_by_name(SessionLocal(), "editor").id
    response = client.post(
        "users/foo/role/%s"%(role_id),
        headers={"Authorization":"Bearer admin1"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail":"User not found"}

def test_assign_editor_role_incorrect_role():
    editor_id = crud.get_user_by_username(SessionLocal(), "editor").id
    response = client.post(
        "users/%s/role/foo"%(editor_id),
        headers={"Authorization":"Bearer admin1"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail":"Role not found"}

def test_assign_editor_role_incorrect_privilege():
    editor_id = crud.get_user_by_username(SessionLocal(), "editor").id
    response = client.post(
        "users/%s/role/foo"%(editor_id),
        headers={"Authorization":"Bearer visitor"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "User is not an administrator"}

##########
# Create eventdraft
##########

def test_create_eventdraft_success():
    event_json = {
            "title": "Event title",
            "detail": "Event detail",
            "startdate": "2023-06-01",
            "enddate": "2023-06-30",
            "pub_requested": 1
        }
    response = client.post(
            "/eventdraft/create",
            headers={"Authorization":"Bearer editor"},
            json= event_json
        )
    assert response.status_code == 200
    list(response.json()) == ["title","detail","startdate","enddate","pub_requested"]

def test_create_eventdraft_no_title():
    event_json = {
            "detail": "Event detail",
            "startdate": "2023-06-01",
            "enddate": "2023-06-30",
            "pub_requested": 1
        }
    response = client.post(
            "/eventdraft/create",
            headers={"Authorization":"Bearer editor"},
            json= event_json
        )
    assert response.status_code == 422 # Unprocessable Entity
    assert response.json()['detail'][0]['msg'] == 'field required'

def test_create_eventdraft_no_detail():
    event_json = {
            "title": "Event title",
            "startdate": "2023-06-01",
            "enddate": "2023-06-30",
            "pub_requested": 1
        }
    response = client.post(
            "/eventdraft/create",
            headers={"Authorization":"Bearer editor"},
            json= event_json
        )
    assert response.status_code == 422 # Unprocessable Entity
    assert response.json()['detail'][0]['msg'] == 'field required'

def test_create_eventdraft_no_startdate():
    event_json = {
            "title": "Event title",
            "detail": "Event detail",
            "enddate": "2023-06-30",
            "pub_requested": 1
        }
    response = client.post(
            "/eventdraft/create",
            headers={"Authorization":"Bearer editor"},
            json= event_json
        )
    assert response.status_code == 422 # Unprocessable Entity
    assert response.json()['detail'][0]['msg'] == 'field required'

def test_create_eventdraft_wrong_enddate():
    event_json = {
            "title": "Event title",
            "detail": "Event detail",
            "startdate": "2023-06-01",
            "enddate": "2023-06-31",
            "pub_requested": 1
        }
    response = client.post(
            "/eventdraft/create",
            headers={"Authorization":"Bearer editor"},
            json= event_json
        )
    assert response.status_code == 422 # Unprocessable Entity
    assert response.json()['detail'][0]['msg'] == 'invalid date format'

def test_create_eventdraft_no_pubrequested_success():
    event_json = {
            "title": "Event title 2",
            "detail": "Event detail",
            "startdate": "2023-06-01",
            "enddate": "2023-06-30"
        }
    response = client.post(
            "/eventdraft/create",
            headers={"Authorization":"Bearer editor"},
            json= event_json
        )
    assert response.status_code == 200
    list(response.json()) == ["title","detail","startdate","enddate","pub_requested"]


##########
# Publish eventdraft
##########

def test_publish_eventdraft_eventdraft_not_found():
    eventdraft_id = "foo"
    response = client.post(
        "eventdraft/"+eventdraft_id+"/publish",
        headers={"Authorization":"Bearer admin1"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail":"Event draft not found"}

def test_publish_eventdraft_unauthorized():
    db_eventdrafts = crud.get_eventdraft(SessionLocal())
    eventdraft_id = db_eventdrafts[0].id
    response = client.post(
        "eventdraft/"+eventdraft_id+"/publish",
        headers={"Authorization":"Bearer editor"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail":"User is not a moderator"}

def test_publish_eventdraft_success():
    db_eventdrafts = crud.get_eventdraft(SessionLocal())
    eventdraft_id = db_eventdrafts[0].id
    response = client.post(
        "eventdraft/"+eventdraft_id+"/publish",
        headers={"Authorization":"Bearer admin1"}
    )
    assert response.status_code == 200
    assert list(response.json()) == ["title","detail","startdate","enddate","id","created","updated","published","categories"]


##########
# Visualize published events
##########

def test_read_events_success():
    startdate = "2023-04-01"
    enddate = "2023-06-30"
    category_id = crud.get_category_by_name(SessionLocal(),"myself").id
    response = client.get(
        "/event/%s/%s/%s"%(category_id,startdate,enddate)
    )
    assert response.status_code == 200
    assert size(response) == 1

def test_read_events_wrong_startdate():
    startdate = "2023-04-015"
    enddate = "2023-06-30"
    category_id = crud.get_category_by_name(SessionLocal(),"myself").id
    response = client.get(
        "/event/%s/%s/%s"%(category_id,startdate,enddate)
    )
    assert response.status_code == 400
    assert response.json() == {"detail":"Incorrect data format, should be YYYY-MM-DD"}

def test_read_events_wrong_enddate():
    startdate = "2023-04-01"
    enddate = "2023-06-31"
    category_id = crud.get_category_by_name(SessionLocal(),"myself").id
    response = client.get(
        "/event/%s/%s/%s"%(category_id,startdate,enddate)
    )
    assert response.status_code == 400
    assert response.json() == {"detail":"Incorrect data format, should be YYYY-MM-DD"}

def test_read_events_category_not_found():
    startdate = "2023-04-01"
    enddate = "2023-06-30"
    category_id = "foo"
    response = client.get(
        "/event/%s/%s/%s"%(category_id,startdate,enddate)
    )
    assert response.status_code == 404
    assert response.json() == {"detail":"Category not found"}

    restore_test_database()

