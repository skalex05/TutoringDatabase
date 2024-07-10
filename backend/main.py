import googleapiclient.errors
import sqlalchemy.exc
from flask import request, jsonify
from tables import (Parent, Business, Student, Session, Event,
                    db, app,
                    CALENDAR_ID,
                    calendar_service, gmail_service,
                    calendarResource, eventsResource,
                    TIME_FORMAT)
import traceback
import uuid
from datetime import datetime, timedelta


# A REST API for the Tutoring Database. Each table has its own set of CRUD endpoints.
# The database also connects to google calendar to create Google Meet links for each session
# which can then be emailed to clients.

# Generics

def get(table, data):
    """
        Generic get function for all tables
        :return: {"table": [row JSON]}, 200 - success/ 500 - server error
    """
    try:
        rows = table.query.filter_by(**data).all()
        json = jsonify({table.__name__: [row.to_json() for row in rows]})
        return json, 200
    except Exception as e:
        # If an error occurs, print the traceback and return a 500 status code
        traceback.print_exception(e)
        return {}, 500


def new(table, data):
    """
        Generic function for creating a new row in a given database and returns the new row's JSON.
        :return: {"table": [row JSON]}, 200 - success/ 500 - server error
        """
    try:
        row = table(**data)
        db.session.add(row)
        db.session.commit()
        return jsonify({table.__name__: [row.to_json()]}), 200
    except Exception as e:
        traceback.print_exception(e)
        return {}, 500


def delete(table, data):
    """
        Generic function for deleting a row from a given database.
        :return: 200 - success/ 500 - server error
    """
    try:
        if not any([key.endswith("ID") for key in data]):
            return {}, 500
        rows = table.query.filter_by(**{table.__name__ + "ID": data[table.__name__ + "ID"]}).all()
        json = jsonify({table.__name__: [row.to_json() for row in rows]})
        db.session.execute(
            table.__table__.delete().where(getattr(table, table.__name__ + "ID") == data[table.__name__ + "ID"]))
        db.session.commit()
        return json, 200
    except sqlalchemy.exc.IntegrityError:
        return {}, 400
    except Exception as e:
        traceback.print_exception(e)
        return {}, 500


def update(table, data):
    """
        Generic function for updating a row in a given database.
        :return: {"table": [row JSON]}, 200 - success/ 500 - server error
    """
    try:
        table.query.filter_by(**{table.__name__ + "ID": data[table.__name__ + "ID"]}).update(data)
        row = table.query.filter_by(**{table.__name__ + "ID": data[table.__name__ + "ID"]}).first()
        db.session.commit()
        return jsonify({table.__name__: [row.to_json()]}), 200
    except Exception as e:
        traceback.print_exception(e)
        return {}, 500


# Parent Table

@app.route("/get_parent", methods=["OPTIONS", "GET"])
def get_parent():
    """
        If a ParentID is provided, it will return the parent with that ID.
        Otherwise, it will get all parents from the database.
        :return: {"parents": [parent JSON]}, 200 - success/ 500 - server error
    """
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}

    data = request.get_json() if request.is_json else {}
    response = get(Parent, data)
    return response


@app.route("/new_parent", methods=["OPTIONS", "POST"])
def new_parent():
    """
        Adds a new parent to the database and returns the new parent's JSON.
        :return: {"parent": [parent JSON]}, 200 - success/ 500 - server error
    """
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}

    data = request.get_json()
    response = new(Parent, data)
    return response


@app.route("/del_parent", methods=["OPTIONS", "DELETE"])
def del_parent():
    """
        Deletes a parent from the database.
        :return: 200 - success/ 500 - server error
    """
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}

    data = request.get_json()
    response = delete(Parent, data)
    return response


@app.route("/update_parent", methods=["OPTIONS", "PUT"])
def update_parent():
    """
        Updates a parent in the database. The ParentID must be provided in the JSON.
        :return: {"parent": [parent JSON]}, 200 - success/ 500 - server error
    """
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}

    data = request.get_json()
    response = update(Parent, data)
    return response


# Business Table

@app.route("/get_business", methods=["OPTIONS", "GET"])
def get_business():
    """
        If a BusinessID is provided, it will return the business with that ID.
        Otherwise, it will get all businesses from the database.
        :return: {"businesses": [business JSON]}, 200 - success/ 500 - server error
    """
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}

    data = request.get_json() if request.is_json else {}
    response = get(Business, data)
    return response


@app.route("/new_business", methods=["OPTIONS", "POST"])
def new_business():
    """
        Adds a new business to the database and returns the new business's JSON.
        :return: {"business": [business JSON]}, 200 - success/ 500 - server error
    """
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}

    data = request.get_json()
    response = new(Business, data)
    return response


@app.route("/del_business", methods=["OPTIONS", "DELETE"])
def del_business():
    """
        Deletes a business from the database.
        :return: 200 - success/ 500 - server error
    """
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}

    data = request.get_json()
    response = delete(Business, data)
    return response


@app.route("/update_business", methods=["OPTIONS", "PUT"])
def update_business():
    """
        Updates a business in the database. The BusinessID must be provided in the JSON.
        :return: {"business": [business JSON]}, 200 - success/ 500 - server error
    """
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}

    data = request.get_json()
    response = update(Business, data)
    return response


# Student Table

@app.route("/get_student", methods=["OPTIONS", "GET"])
def get_student():
    """
        If a StudentID is provided, it will return the student with that ID.
        Otherwise, it will get all students from the database.
        :return: {"students": [student JSON]}, 200 - success/ 500 - server error
    """
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}

    data = request.get_json() if request.is_json else {}
    response = get(Student, data)
    return response


@app.route("/new_student", methods=["OPTIONS", "POST"])
def new_student():
    """
       Adds a new student to the database and returns the new student's JSON.
       :return: {"student": [student JSON]}, 200 - success/ 500 - server error
    """
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}

    data = request.get_json()
    response = new(Student, data)
    return response


@app.route("/del_student", methods=["OPTIONS", "DELETE"])
def del_student():
    """
        Deletes a student from the database.
        :return: 200 - success/ 500 - server error
    """
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}

    data = request.get_json()
    response = delete(Student, data)
    return response


@app.route("/update_student", methods=["OPTIONS", "PUT"])
def update_student():
    """
        Updates a student in the database. The StudentID must be provided in the JSON.
        :return: {"student": [student JSON]}, 200 - success/ 500 - server error
    """
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}

    data = request.get_json()
    response = update(Student, data)
    return response


# Session Table

@app.route("/get_session", methods=["OPTIONS", "GET"])
def get_session():
    """
        If a SessionID is provided, it will return the session with that ID.
        Otherwise, it will get all sessions from the database.
        :return: {"sessions": [session JSON]}, 200 - success/ 500 - server error
    """
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}

    data = request.get_json() if request.is_json else {}
    response = get(Session, data)
    return response


@app.route("/new_session", methods=["OPTIONS", "POST"])
def new_session():
    """
        Adds a new session to the database and returns the new session's JSON.
        :return: {"session": [session JSON]}, 200 - success/ 500 - server error
    """
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}

    data = request.get_json()
    try:
        data["StartTime"] = datetime.strptime(data["StartTime"], TIME_FORMAT)
        data["EndTime"] = datetime.strptime(data["EndTime"], TIME_FORMAT)
    except ValueError:
        return {}, 400

    response = new(Session, data)
    return response


@app.route("/del_session", methods=["OPTIONS", "DELETE"])
def del_session():
    print("Delete")
    """
        Deletes a session from the database.
        :return: 200 - success/ 500 - server error
    """
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    print("get data")
    print(request.is_json)
    data = request.get_json()
    print("Data:", data)

    try:
        Event.query.filter_by(SessionID=data["SessionID"]).delete()
    except Exception as e:
        traceback.print_exception(e)
        return {}, 500
    response = delete(Session, data)
    return response


@app.route("/update_session", methods=["OPTIONS", "PUT"])
def update_session():
    """
        Updates a session in the database. The SessionID must be provided in the JSON.
        :return: {"session": [session JSON]}, 200 - success/ 500 - server error
    """

    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}

    try:
        data = request.get_json()
        try:
            if "StartTime" in data:
                data["StartTime"] = datetime.strptime(data["StartTime"], TIME_FORMAT)
            if "EndTime" in data:
                data["EndTime"] = datetime.strptime(data["EndTime"], TIME_FORMAT)
        except ValueError:
            return {}, 400
        # if timeChange:
        #     for event in Event.query.filter_by(**{"SessionID": data["SessionID"]}).all():
        #         event_json = event.to_json()
        #         start_time = datetime.strptime(event_json["EventDateTimeStart"], "%Y-%m-%d %H:%M")
        #         if start_time < datetime.now():
        #             continue
        #         end_time = datetime.strptime(event_json["EventDateTimeEnd"], "%Y-%m-%d %H:%M")
        #         start_time = start_time.replace(year=data["NextScheduleWeekDate"].year, month=data["NextScheduleWeekDate"].month,
        #                                         day=data["NextScheduleWeekDate"].day, hour=data["StartTime"].hour,
        #                                         minute=data["StartTime"].minute)
        #         end_time = end_time.replace(year=data["NextScheduleWeekDate"].year, month=data["NextScheduleWeekDate"].month,
        #                                     day=data["NextScheduleWeekDate"].day, hour=data["EndTime"].hour,
        #                                     minute=data["EndTime"].minute)
        #         event_json["EventDateTimeStart"] = start_time
        #         event_json["EventDateTimeEnd"] = end_time
        #         eventsResource.patch(calendarId=event_json["GoogleCalendarID"], eventId=event_json["GoogleEventID"],
        #                              body={"start": {"dateTime": start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        #                                              "timeZone": "Europe/London"},
        #                                    "end": {"dateTime": end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        #                                            "timeZone": "Europe/London"}}).execute()
        #
        #         Event.query.filter_by(**{Event.__name__ + "ID": data[Event.__name__ + "ID"]}).update(data)
        #         row = Event.query.filter_by(**{Event.__name__ + "ID": data[Event.__name__ + "ID"]}).first()
        #         db.session.commit()
        # return jsonify({Event.__name__: [row.to_json()]}), 200

        Session.query.filter_by(**{Session.__name__ + "ID": data[Session.__name__ + "ID"]}).update(data)
        row = Session.query.filter_by(**{Session.__name__ + "ID": data[Session.__name__ + "ID"]}).first()
        db.session.commit()
        return jsonify({Session.__name__: [row.to_json()]}), 200
    except Exception as e:
        traceback.print_exception(e)
        return {}, 500


# Event Table

@app.route("/get_event", methods=["OPTIONS", "GET"])
def get_event():
    """
        If an EventID is provided, it will return the event with that ID.
        Otherwise, it will get all events from the database.
        :return: {"events": [event JSON]}, 200 - success/ 500 - server error
    """
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}

    data = request.get_json() if request.is_json else {}
    response = get(Event, data)
    return response


@app.route("/new_event", methods=["OPTIONS", "POST"])
def new_event():
    """
        Adds a new event to the database and returns the new event's JSON.
        :return: {"event": [event JSON]}, 200 - success/ 500 - server error
    """
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    data = request.get_json()
    try:
        session, _ = get(Session, {"SessionID": data["SessionID"]})
        session = session.json["Session"][0]

        student, _ = get(Student, {"StudentID": session["StudentID"]})
        student = student.json["Student"][0]

        parent, _ = get(Parent, {"ParentID": student["ParentID"]})
        parent = parent.json["Parent"][0]

        business, _ = get(Business, {"BusinessID": student["BusinessID"]})
        business = business.json["Business"][0]

        if "StartTime" not in data or "EndTime" not in data:
            data["StartTime"] = session["StartTime"]
            data["EndTime"] = session["EndTime"]

        data["EventName"] = session["SessionName"]

        event_body = {
            "attendees": [
                {"email": parent["Email"]},
                {"email": student["Email"]}
            ],
            "summary": session["SessionName"],
            "description": f"{session['Subject']} Session for {student['FirstName']} {student['LastName']}\n- {business['BusinessName']} - {business['Email']}",
            "conferenceData": {
                "createRequest": {
                    "requestId": str(uuid.uuid4()),
                    "conferenceSolutionKey": {
                        "type": "hangoutsMeet"
                    },
                }
            },
            "start": {
                "dateTime": data["StartTime"],
                "timeZone": "Etc/UTC"
            },
            "end": {
                "dateTime": data["EndTime"],
                "timeZone": "Etc/UTC"
            }
        }
        response = eventsResource.insert(calendarId=CALENDAR_ID, body=event_body, conferenceDataVersion=1).execute()

        data["GoogleCalendarID"] = CALENDAR_ID
        data["GoogleEventID"] = response["id"]
        data["GoogleMeetLink"] = response["hangoutLink"]
        data["StartTime"] = datetime.strptime(data["StartTime"], TIME_FORMAT)
        data["EndTime"] = datetime.strptime(data["EndTime"], TIME_FORMAT)
        response = new(Event, data)
        return response
    except googleapiclient.errors.HttpError as e:
        traceback.print_exception(e)
        return {}, 400
    except Exception as e:
        traceback.print_exception(e)
        return {}, 500


@app.route("/update_event", methods=["OPTIONS", "PUT"])
def update_event(data=None):
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
        Updates an event in the database. The EventID must be provided in the JSON.
        :return: {"event": [event JSON]}, 200 - success/ 500 - server error
    """
    try:
        if not data:
            data = request.get_json()

        if "StartTime" in data:
            data["StartTime"] = datetime.strptime(data["StartTime"], TIME_FORMAT)

        if "EndTime" in data:
            data["EndTime"] = datetime.strptime(data["EndTime"], TIME_FORMAT)

        response, status = update(Event, data)
        if status != 200:
            return {}, status
        event_json = response.json["Event"][0]

        json_body = {}
        if "StartTime" in data:
            json_body["start"] = {"dateTime": datetime.strftime(data["StartTime"], TIME_FORMAT), "timeZone": "Etc/UTC"}
        if "EndTime" in data:
            json_body["end"] = {"dateTime": datetime.strftime(data["EndTime"], TIME_FORMAT), "timeZone": "Etc/UTC"}
        if "EventName" in data:
            json_body["summary"] = data["EventName"]
        if json_body != {}:
            eventsResource.patch(calendarId=event_json["GoogleCalendarID"], eventId=event_json["GoogleEventID"],
                                 body=json_body).execute()
        return response
    except Exception as e:
        traceback.print_exception(e)
        return {}, 500


@app.route("/del_event", methods=["OPTIONS", "DELETE"])
def del_event():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
        Deletes an event from the database.
        :return: 200 - success/ 500 - server error
    """
    try:
        data = request.get_json()
        response, status = delete(Event, data)
        if status != 200:
            return {}, status
        calendarID = response.json["Event"][0]["GoogleCalendarID"]
        eventID = response.json["Event"][0]["GoogleEventID"]
        eventsResource.delete(calendarId=calendarID, eventId=eventID).execute()
    except Exception as e:
        traceback.print_exception(e)
        return {}, 500

    return response


# Create DB if one does not already exist
with app.app_context():
    db.create_all()
    new(Parent, {"FirstName": "John", "LastName": "Doe", "Email": "jd@gmail.com", "PhoneNumber": 1234})
    new(Business,
        {"BusinessName": "Tutoring", "FirstName": "Jamal", "LastName": "Dequavious", "Email": "jamal@mail.com",
         "PhoneNumber": 1234})
    new(Student,
        {"FirstName": "Jane", "LastName": "Dale", "YearGrade": 12, "Email": "dale@mailo.co", "PhoneNumber": 1234,
         "BusinessID": 1, "ParentID": 1})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
