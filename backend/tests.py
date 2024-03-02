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
        response = test_client.get("/get_parent", query_string={"ParentID": 1})
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
        assert response.status_code == 200
        assert "Parent" in response.json
        parent_id = response.json["Parent"][0]["ParentID"]
        response = test_client.delete("/del_parent", json={"ParentID": parent_id})
        assert response.status_code == 200
        response = test_client.get("/get_parent", query_string={"ParentID": parent_id})
        assert response.status_code == 200
        assert "Parent" in response.json
        assert response.json["Parent"] == []


# Business Tests

def test_new_business(app):
    with app.app_context():
        test_client = app.test_client()
        test_json = {"BusinessName": "Test Business",
                     "FirstName": "John",
                     "LastName": "Doe",
                     "Email": "johndoe@hotmail.com",
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
        response = test_client.get("/get_business", query_string={"BusinessID": 1})
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
        response = test_client.get("/get_business", query_string={"BusinessID": business_id})
        assert response.status_code == 200
        assert "Business" in response.json
        assert response.json["Business"] == []


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
        response = test_client.post("/new_student", json=test_json)
        assert response.status_code == 200
        assert "Student" in response.json
        json = response.json["Student"][0]
        del json["StudentID"]
        assert json == test_json


def test_get_student(app):
    test_new_student(app)
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_student")
        assert response.status_code == 200
        assert "Student" in response.json


def test_get_student(app):
    test_new_student(app)
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_student", query_string={"StudentID": 1})
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

        student_id = response.json["Student"][0]["StudentID"]
        response = test_client.delete("/del_student", json={"StudentID": student_id})
        assert response.status_code == 200
        response = test_client.get("/get_student", query_string={"StudentID": student_id})
        assert response.status_code == 200
        assert "Student" in response.json
        assert response.json["Student"] == []

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
                     "WeekdayInt": 1,
                     "StartWeekDate": "2024-02-26",
                     "StartTime": "12:00",
                     "EndTime": "13:00",
                     "Pay": 20}

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
        assert len(response.json["Session"]) == 1


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
                     "WeekdayInt": 1,
                     "StartWeekDate": "2024-02-26",
                     "StartTime": "12:00",
                     "EndTime": "13:00",
                     "Pay": 20}
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

        student_id = response.json["Session"][0]["SessionID"]
        response = test_client.delete("/del_session", json={"SessionID": student_id})
        assert response.status_code == 200
        response = test_client.get("/get_session", query_string={"SessionID": student_id})
        assert response.status_code == 200
        assert "Session" in response.json
        assert response.json["Session"] == []
