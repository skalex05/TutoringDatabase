from flask import request, jsonify
from tables import Parent, Business, Student, Session, db, app
import traceback

# A REST API for the Tutoring Database. Each table has its own set of CRUD endpoints.

# Generics


def get(table, id_str):
    """Generic get function for all tables
    :return: {"table": [row JSON]}, 200 - success/ 500 - server error
    """
    try:
        row_id = request.args.get(id_str)
        if row_id:
            row = table.query.filter_by(**{table.__name__+"ID": row_id}).first()
            if row:
                return jsonify({table.__name__: [row.to_json()]}), 200
            else:
                return {table.__name__: []}, 200
        else:
            rows = table.query.all()
            return jsonify({table.__name__: [row.to_json() for row in rows]}), 200
    except Exception as e:
        # If an error occurs, print the traceback and return a 500 status code
        print()
        traceback.print_exception(e)
        return {}, 500


def new(table):
    """
        Generic function for creating a new row in a given database and returns the new row's JSON.
        :return: {"table": [row JSON]}, 200 - success/ 500 - server error
        """
    try:
        data = request.get_json()
        row = table(**data)
        db.session.add(row)
        db.session.commit()
        return jsonify({table.__name__: [row.to_json()]}), 200
    except Exception as e:
        print()
        traceback.print_exception(e)
        return {}, 500


def delete(table, id_str):
    """
    Generic function for deleting a row from a given database.
    :return: 200 - success/ 500 - server error
    """
    try:
        data = request.get_json()
        table.query.filter_by(**{table.__name__+"ID": data[id_str]}).delete()
        db.session.commit()
        return {}, 200
    except Exception as e:
        print()
        traceback.print_exception(e)
        return {}, 500


def update(table):
    """
    Generic function for updating a row in a given database.
    :return: {"table": [row JSON]}, 200 - success/ 500 - server error
    """
    try:
        data = request.get_json()
        table.query.filter_by(**{table.__name__+"ID": data[table.__name__+"ID"]}).update(data)
        row = table.query.filter_by(**{table.__name__+"ID": data[table.__name__+"ID"]}).first()
        db.session.commit()
        return jsonify({table.__name__: [row.to_json()]}), 200
    except Exception as e:
        print()
        traceback.print_exception(e)
        return {}, 500


# Parent Table

@app.route("/get_parent", methods=["GET"])
def get_parent():
    """
    If a ParentID is provided, it will return the parent with that ID.
    Otherwise, it will get all parents from the database.
    :return: {"parents": [parent JSON]}, 200 - success/ 500 - server error
    """
    response = get(Parent, "ParentID")
    return response


@app.route("/new_parent", methods=["POST"])
def new_parent():
    """
    Adds a new parent to the database and returns the new parent's JSON.
    :return: {"parent": [parent JSON]}, 200 - success/ 500 - server error
    """
    response = new(Parent)
    return response


@app.route("/del_parent", methods=["DELETE"])
def del_parent():
    """
        Deletes a parent from the database.
        :return: 200 - success/ 500 - server error
    """
    response = delete(Parent, "ParentID")
    return response


@app.route("/update_parent", methods=["PUT"])
def update_parent():
    """
        Updates a parent in the database. The ParentID must be provided in the JSON.
        :return: {"parent": [parent JSON]}, 200 - success/ 500 - server error
    """
    response = update(Parent)
    return response


# Business Table

@app.route("/get_business", methods=["GET"])
def get_business():
    """
    If a BusinessID is provided, it will return the business with that ID.
    Otherwise, it will get all businesses from the database.
    :return: {"businesses": [business JSON]}, 200 - success/ 500 - server error
    """
    response = get(Business, "BusinessID")
    return response


@app.route("/new_business", methods=["POST"])
def new_business():
    """
    Adds a new business to the database and returns the new business's JSON.
    :return: {"business": [business JSON]}, 200 - success/ 500 - server error
    """
    response = new(Business)
    return response


@app.route("/del_business", methods=["DELETE"])
def del_business():
    """
        Deletes a business from the database.
        :return: 200 - success/ 500 - server error
    """
    response = delete(Business, "BusinessID")
    return response


@app.route("/update_business", methods=["PUT"])
def update_business():
    """
        Updates a business in the database. The BusinessID must be provided in the JSON.
        :return: {"business": [business JSON]}, 200 - success/ 500 - server error
    """
    response = update(Business)
    return response


# Student Table

@app.route("/get_student", methods=["GET"])
def get_student():
    """
    If a StudentID is provided, it will return the student with that ID.
    Otherwise, it will get all students from the database.
    :return: {"students": [student JSON]}, 200 - success/ 500 - server error
    """
    response = get(Student, "StudentID")
    return response


@app.route("/new_student", methods=["POST"])
def new_student():
    """
    Adds a new student to the database and returns the new student's JSON.
    :return: {"student": [student JSON]}, 200 - success/ 500 - server error
    """
    response = new(Student)
    return response


@app.route("/del_student", methods=["DELETE"])
def del_student():
    """
        Deletes a student from the database.
        :return: 200 - success/ 500 - server error
    """
    response = delete(Student, "StudentID")
    return response


@app.route("/update_student", methods=["PUT"])
def update_student():
    """
        Updates a student in the database. The StudentID must be provided in the JSON.
        :return: {"student": [student JSON]}, 200 - success/ 500 - server error
    """
    response = update(Student)
    return response


# Session Table

@app.route("/get_session", methods=["GET"])
def get_session():
    """
    If a SessionID is provided, it will return the session with that ID.
    Otherwise, it will get all sessions from the database.
    :return: {"sessions": [session JSON]}, 200 - success/ 500 - server error
    """
    response = get(Session, "SessionID")
    return response


@app.route("/new_session", methods=["POST"])
def new_session():
    """
    Adds a new session to the database and returns the new session's JSON.
    :return: {"session": [session JSON]}, 200 - success/ 500 - server error
    """
    response = new(Session)
    return response


@app.route("/del_session", methods=["DELETE"])
def del_session():
    """
        Deletes a session from the database.
        :return: 200 - success/ 500 - server error
    """
    response = delete(Session, "SessionID")
    return response


@app.route("/update_session", methods=["PUT"])
def update_session():
    """
        Updates a session in the database. The SessionID must be provided in the JSON.
        :return: {"session": [session JSON]}, 200 - success/ 500 - server error
    """
    response = update(Session)
    return response


# Create DB if one does not already exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
