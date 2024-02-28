from flask import request, jsonify
from tables import Parent, Business, Student, Timetable, db, app
import traceback

# A REST API for the Tutoring Database. Each table has its own set of CRUD endpoints.

# Generics


def get(id_str, table):
    """Generic get function for all tables
    :return: {"table": [...row JSON...]}, 200 - success/ 500 - server error
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
            rows = Parent.query.all()
            return jsonify({table.__name__: [row.to_json() for row in rows]}), 200
    except Exception as e:
        # If an error occurs, print the traceback and return a 500 status code
        print()
        traceback.print_exception(e)
        return {}, 500


# Parent Table
@app.route("/get_parent", methods=["GET"])
def get_parent():
    """
    If a ParentID is provided, it will return the parent with that ID.
    Otherwise, it will get all parents from the database.
    :return: {"parents": [...parent JSON...]}, 200 - success/ 500 - server error
    """
    response = get("ParentID", Parent)
    return response


@app.route("/new_parent", methods=["POST"])
def new_parent():
    """
    Adds a new parent to the database and returns the new parent's JSON.
    :return: {"parent": parent JSON}, 200 - success/ 500 - server error
    """
    try:
        data = request.get_json()
        parent = Parent(**data)
        db.session.add(parent)
        db.session.commit()
        return jsonify({"Parent": [parent.to_json()]}), 200
    except Exception as e:
        print()
        traceback.print_exception(e)
        return {}, 500


@app.route("/del_parent", methods=["DELETE"])
def del_parent():
    """
    Deletes a parent from the database.
    :return: 200 - success/ 500 - server error
    """
    try:
        data = request.get_json()
        Parent.query.filter_by(ParentID=data["ParentID"]).delete()
        db.session.commit()
        return {}, 200
    except Exception as e:
        print()
        traceback.print_exception(e)
        return {}, 500


@app.route("/update_parent", methods=["PUT"])
def update_parent():
    """
    Updates a parent in the database. The ParentID must be provided in the JSON.
    :return: {"parent": parent JSON}, 200 - success/ 500 - server error
    """
    try:
        data = request.get_json()
        Parent.query.filter_by(ParentID=data["ParentID"]).update(data)
        parent = Parent.query.filter_by(ParentID=data["ParentID"]).first()
        db.session.commit()
        return {"Parent": [parent.to_json()]}, 200
    except Exception as e:
        print()
        traceback.print_exception(e)
        return {}, 500


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
