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
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_parent")
        assert response.status_code == 200
        assert "Parent" in response.json


def test_get_parent(app):
    with app.app_context():
        test_client = app.test_client()
        response = test_client.get("/get_parent", query_string={"ParentID": 1})
        assert response.status_code == 200
        assert "Parent" in response.json


def test_update_parent(app):
    with app.app_context():
        test_client = app.test_client()
        test_json = {"ParentID": 1,
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
    with app.app_context():
        test_client = app.test_client()
        response = test_client.delete("/del_parent", json={"ParentID": 0})
        assert response.status_code == 200
