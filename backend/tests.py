import pytest
from main import app as test_app


@pytest.fixture()
def app():
    test_app.config.update({"TESTING": True,
                            "DEBUG": True,
                            "ENV": "development",
                            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})

    yield test_app


def client(app):
    return app.test_client()


def runner(app):
    return app.test_cli_runner()


# Parent Tests

def test_new_parent(app):
    with app.app_context():
        test_client = app.test_client()
        test_json = {"FirstName": "John",
                     "LastName": "Doe",
                     "Email": "johndoe@hotmail.com",
                     "PhoneNumber": "1234567890"}
        response = test_client.post("/new_parent", json=test_json)
        assert response.status_code == 200
        assert "Parent" in response.json
        json = response.json["Parent"][0]
        del json["ParentID"]
        assert json == test_json


def test_get_parents(app):
    test_new_parent(app)
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_parent")
        assert response.status_code == 200
        assert "Parent" in response.json


def test_get_parent(app):
    test_new_parent(app)
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_parent", json={"ParentID": 1})
        assert response.status_code == 200
        assert "Parent" in response.json


def test_update_parent(app):
    test_new_parent(app)
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_parent")
        assert response.status_code == 200
        assert "Parent" in response.json
        parent_id = response.json["Parent"][0]["ParentID"]
        test_json = {"ParentID": parent_id,
                     "FirstName": "Jane",
                     "LastName": "Doe",
                     "Email": "janedoe@hotmail.com",
                     "PhoneNumber": "1234567890"}
        response = test_client.put("/update_parent", json=test_json)
        assert response.status_code == 200
        assert "Parent" in response.json
        json = response.json["Parent"][0]
        assert json == test_json


def test_del_parent(app):
    test_new_parent(app)
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_parent")
        print(test_client.get("/get_student").json)
        assert response.status_code == 200
        assert "Parent" in response.json
        count = len(response.json["Parent"])
        parent_id = response.json["Parent"][0]["ParentID"]
        response = test_client.delete("/del_parent", json={"ParentID": parent_id})
        assert response.status_code == 200
        response = test_client.get("/get_parent", json={"ParentID": parent_id})
        assert response.status_code == 200
        assert "Parent" in response.json
        assert len(response.json["Parent"]) + 1 == count


# Business Tests

def test_new_business(app):
    with app.app_context():
        test_client = app.test_client()
        test_json = {"BusinessName": "Test Business",
                     "FirstName": "John",
                     "LastName": "Doe",
                     "Email": "johndoebusiness@hotmail.com",
                     "PhoneNumber": "1234567890"}
        response = test_client.post("/new_business", json=test_json)
        assert response.status_code == 200
        assert "Business" in response.json
        json = response.json["Business"][0]
        del json["BusinessID"]
        assert json == test_json


def test_get_business(app):
    test_new_business(app)
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_business")
        assert response.status_code == 200
        assert "Business" in response.json


def test_get_business(app):
    test_new_business(app)
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_business", json={"BusinessID": 1})
        assert response.status_code == 200
        assert "Business" in response.json
        assert response.json["Business"][0]["BusinessID"] == 1
        assert len(response.json["Business"]) == 1


def test_update_business(app):
    test_new_business(app)
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_business")
        assert response.status_code == 200
        assert "Business" in response.json
        parent_id = response.json["Business"][0]["BusinessID"]
        test_json = {"BusinessID": parent_id,
                     "BusinessName": "New Test Business",
                     "FirstName": "Jane",
                     "LastName": "Doe",
                     "Email": "janedoe@hotmail.com",
                     "PhoneNumber": "1234567890"}
        response = test_client.put("/update_business", json=test_json)
        assert response.status_code == 200
        assert "Business" in response.json
        json = response.json["Business"][0]
        assert json == test_json


def test_del_business(app):
    test_new_business(app)
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_business")
        assert response.status_code == 200
        assert "Business" in response.json
        business_id = response.json["Business"][0]["BusinessID"]
        response = test_client.delete("/del_business", json={"BusinessID": business_id})
        assert response.status_code == 200
        response = test_client.get("/get_business", json={"BusinessID": business_id})
        assert response.status_code == 200
        assert "Business" in response.json


# Student Tests

def test_new_student(app):
    test_new_business(app)
    test_new_parent(app)
    with app.app_context():
        # Get a business to use in the test
        test_client = app.test_client()
        response = test_client.get("/get_business")
        assert response.status_code == 200
        assert "Business" in response.json
        business_id = response.json["Business"][0]["BusinessID"]

        # Get a parent to use in the test
        response = test_client.get("/get_parent")
        assert response.status_code == 200
        assert "Parent" in response.json
        parent_id = response.json["Parent"][0]["ParentID"]

        test_json = {"FirstName": "John",
                     "LastName": "Doe",
                     "YearGrade": 12,
                     "Email": "johndoe@hotmail.com",
                     "PhoneNumber": "1234567890",
                     "BusinessID": business_id,
                     "ParentID": parent_id}
        response = test_client.post("/new_student", json=test_json, headers={"Content-Type": "application/json"})
        assert response.status_code == 200
        assert "Student" in response.json
        json = response.json["Student"][0]
        del json["StudentID"]
        assert json == test_json


def test_get_student(app):
    test_new_student(app)
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_student", headers={"Content-Type": "application/json"})
        assert response.status_code == 200
        assert "Student" in response.json


def test_get_student(app):
    test_new_student(app)
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_student", json={"StudentID": 1},
                                   headers={"Content-Type": "application/json"})
        assert response.status_code == 200
        assert "Student" in response.json
        assert response.json["Student"][0]["StudentID"] == 1
        assert len(response.json["Student"]) == 1


def test_update_student(app):
    test_new_student(app)
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_student")
        assert response.status_code == 200
        assert "Student" in response.json
        student_id = response.json["Student"][0]["StudentID"]
        parent_id = response.json["Student"][0]["ParentID"]
        business_id = response.json["Student"][0]["BusinessID"]
        test_json = {"StudentID": student_id,
                     "FirstName": "Jane",
                     "LastName": "Doe",
                     "YearGrade": 13,
                     "Email": "jdoe@hotmail.com",
                     "PhoneNumber": "1234567890",
                     "BusinessID": business_id,
                     "ParentID": parent_id}
        response = test_client.put("/update_student", json=test_json)
        assert response.status_code == 200
        assert "Student" in response.json
        json = response.json["Student"][0]
        assert json == test_json


def test_del_student(app):
    test_new_student(app)
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_student")
        assert response.status_code == 200
        assert "Student" in response.json
        count = len(response.json["Student"])
        student_id = response.json["Student"][0]["StudentID"]
        response = test_client.delete("/del_student", json={"StudentID": student_id})
        assert response.status_code == 200
        response = test_client.get("/get_student", query_string={"StudentID": student_id})
        assert response.status_code == 200
        assert "Student" in response.json
        assert len(response.json["Student"]) + 1 == count

# Session Tests

def test_new_session(app):
    test_new_student(app)
    with app.app_context():
        # Get a student to use in the test
        test_client = app.test_client()
        response = test_client.get("/get_student")
        assert response.status_code == 200
        assert "Student" in response.json
        student_id = response.json["Student"][0]["StudentID"]

        test_json = {"StudentID": student_id,
                     "SessionName": "Test Session",
                     "Subject": "Math",
                     "StartTime": "2024-02-26T12:00:00.000Z",
                     "EndTime": "2024-02-26T13:00:00.000Z",
                     "Pay": 20,
                     "Schedule": True,
                     "Notes": "Very educational session"}

        response = test_client.post("/new_session", json=test_json)
        assert response.status_code == 200
        assert "Session" in response.json
        json = response.json["Session"][0]
        del json["SessionID"]
        assert json == test_json


def test_get_sessions(app):
    test_new_session(app)
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_session")
        assert response.status_code == 200
        assert "Session" in response.json


def test_get_session(app):
    test_new_session(app)
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_session", query_string={"SessionID": 1})
        assert response.status_code == 200
        assert "Session" in response.json
        assert response.json["Session"][0]["SessionID"] == 1

def test_update_session(app):
    test_new_student(app)
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_session")
        assert response.status_code == 200
        assert "Session" in response.json
        session_id = response.json["Session"][0]["SessionID"]
        student_id = response.json["Session"][0]["StudentID"]
        test_json = {"SessionID": session_id,
                     "StudentID": student_id,
                     "SessionName": "Test Session",
                     "Subject": "Math",
                     "StartTime": "2024-02-26T18:00:00.000Z",
                     "EndTime": "2024-02-26T19:00:00.000Z",
                     "Pay": 20.0,
                     "Schedule": False,
                     "Notes": "Tough days"}
        response = test_client.put("/update_session", json=test_json)
        assert response.status_code == 200
        assert "Session" in response.json
        json = response.json["Session"][0]
        assert json == test_json


def test_del_session(app):
    test_new_session(app)
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_session")
        assert response.status_code == 200
        assert "Session" in response.json
        count = len(response.json["Session"])
        student_id = response.json["Session"][0]["SessionID"]
        response = test_client.delete("/del_session", json={"SessionID": student_id})
        assert response.status_code == 200
        response = test_client.get("/get_session", query_string={"SessionID": student_id})
        assert response.status_code == 200
        assert "Session" in response.json
        assert len(response.json["Session"]) + 1 == count


# Event Tests

def test_new_event_default_datetime(app):
    test_new_session(app)
    with app.app_context():
        # Get a session to use in the test
        test_client = app.test_client()
        test_client.get("/get_session")
        response = test_client.get("/get_session")
        assert response.status_code == 200
        assert "Session" in response.json
        session = response.json["Session"][0]

        test_json = {"SessionID": session["SessionID"],
                     "EventName": session["SessionName"],
                     "LinkEmailSent": False,
                     "DebriefEmailSent": False
                     }

        response = test_client.post("/new_event", json=test_json)
        assert response.status_code == 200
        assert "Event" in response.json
        json = response.json["Event"][0]
        del json["EventID"]
        del json["GoogleCalendarID"]
        del json["GoogleEventID"]
        del json["GoogleMeetLink"]
        del json["StartTime"]
        del json["EndTime"]
        del json["Rescheduled"]
        assert json == test_json

def test_new_event_custom_datetime(app):
    test_new_session(app)
    with app.app_context():
        # Get a session to use in the test
        test_client = app.test_client()
        test_client.get("/get_session")
        response = test_client.get("/get_session")
        assert response.status_code == 200
        assert "Session" in response.json
        session = response.json["Session"][0]

        test_json = {"SessionID": session["SessionID"],
                     "EventName": session["SessionName"],
                     "LinkEmailSent": False,
                     "DebriefEmailSent": False,
                     "StartTime": "2024-02-28T17:30:00.000Z",
                     "EndTime": "2024-02-28T18:30:00.000Z",
                     }

        response = test_client.post("/new_event", json=test_json)
        assert response.status_code == 200
        assert "Event" in response.json
        json = response.json["Event"][0]
        del json["EventID"]
        del json["GoogleCalendarID"]
        del json["GoogleEventID"]
        del json["GoogleMeetLink"]
        del json["Rescheduled"]
        assert json == test_json

def test_get_event(app):
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_event")
        assert response.status_code == 200
        assert "Event" in response.json

def test_update_event(app):
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_event")
        assert response.status_code == 200
        assert "Event" in response.json
        test_json = {
            "EventID": response.json["Event"][0]["EventID"],
            "StartTime": "2024-03-04T13:00:00.000Z",
            "EndTime":   "2024-03-04T15:00:00.000Z",
            "EventName": "New Event Name"
        }
        response = test_client.put("/update_event", json=test_json)
        assert response.status_code == 200
        assert "Event" in response.json


def test_del_event(app):
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_event")
        assert response.status_code == 200
        assert "Event" in response.json
        count = len(response.json["Event"])
        event_id = response.json["Event"][0]["EventID"]
        response = test_client.delete("/del_event", json={"EventID": event_id})
        assert response.status_code == 200
        response = test_client.get("/get_event", query_string={"EventID": event_id})
        assert response.status_code == 200
        assert "Event" in response.json
        assert len(response.json["Event"]) + 1 == count
