import sqlalchemy.exc
from flask import request, jsonify
from tables import (Parent, Business, Student, Session, Event,
                    db, app,
                    CALENDAR_ID,
                    calendar_service, gmail_service,
                    calendarResource, eventsResource)
import traceback
import uuid
from datetime import datetime, timedelta


# A REST API for the Tutoring Database. Each table has its own set of CRUD endpoints.
# The database also connects to google calendar to create Google Meet links for each session
# which can then be emailed to clients.


# Generics

def get(table, id_str):
    """Generic get function for all tables
    :return: {"table": [row JSON]}, 200 - success/ 500 - server error
    """
    try:
        row_id = request.args.get(id_str)
        if row_id:
            row = table.query.filter_by(**{table.__name__ + "ID": row_id}).first()
            if row:
                return jsonify({table.__name__: [row.to_json()]}), 200
            else:
                return {table.__name__: []}, 200
        else:
            rows = table.query.all()
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


def delete(table, id_str):
    """
    Generic function for deleting a row from a given database.
    :return: 200 - success/ 500 - server error
    """
    try:
        data = request.get_json()
        db.session.execute(table.__table__.delete().where(getattr(table, table.__name__+"ID") == data[id_str]))
        db.session.commit()
        return {}, 200
    except sqlalchemy.exc.IntegrityError:
        return {}, 400
    except Exception as e:
        traceback.print_exception(e)
        return {}, 500


def update(table):
    """
    Generic function for updating a row in a given database.
    :return: {"table": [row JSON]}, 200 - success/ 500 - server error
    """
    try:
        data = request.get_json()
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
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
    If a ParentID is provided, it will return the parent with that ID.
    Otherwise, it will get all parents from the database.
    :return: {"parents": [parent JSON]}, 200 - success/ 500 - server error
    """
    response = get(Parent, "ParentID")
    return response


@app.route("/new_parent", methods=["OPTIONS", "POST"])
def new_parent():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
    Adds a new parent to the database and returns the new parent's JSON.
    :return: {"parent": [parent JSON]}, 200 - success/ 500 - server error
    """
    data = request.get_json()
    response = new(Parent, data)
    return response


@app.route("/del_parent", methods=["OPTIONS", "DELETE"])
def del_parent():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
        Deletes a parent from the database.
        :return: 200 - success/ 500 - server error
    """
    response = delete(Parent, "ParentID")
    return response


@app.route("/update_parent", methods=["OPTIONS", "PUT"])
def update_parent():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
        Updates a parent in the database. The ParentID must be provided in the JSON.
        :return: {"parent": [parent JSON]}, 200 - success/ 500 - server error
    """
    response = update(Parent)
    return response


# Business Table

@app.route("/get_business", methods=["OPTIONS", "GET"])
def get_business():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
    If a BusinessID is provided, it will return the business with that ID.
    Otherwise, it will get all businesses from the database.
    :return: {"businesses": [business JSON]}, 200 - success/ 500 - server error
    """
    response = get(Business, "BusinessID")
    return response


@app.route("/new_business", methods=["OPTIONS", "POST"])
def new_business():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
    Adds a new business to the database and returns the new business's JSON.
    :return: {"business": [business JSON]}, 200 - success/ 500 - server error
    """
    data = request.get_json()
    response = new(Business, data)
    return response


@app.route("/del_business", methods=["OPTIONS", "DELETE"])
def del_business():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
        Deletes a business from the database.
        :return: 200 - success/ 500 - server error
    """
    response = delete(Business, "BusinessID")
    return response


@app.route("/update_business", methods=["OPTIONS", "PUT"])
def update_business():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
        Updates a business in the database. The BusinessID must be provided in the JSON.
        :return: {"business": [business JSON]}, 200 - success/ 500 - server error
    """
    response = update(Business)
    return response


# Student Table

@app.route("/get_student", methods=["OPTIONS", "GET"])
def get_student():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
    If a StudentID is provided, it will return the student with that ID.
    Otherwise, it will get all students from the database.
    :return: {"students": [student JSON]}, 200 - success/ 500 - server error
    """
    response = get(Student, "StudentID")
    return response


@app.route("/new_student", methods=["OPTIONS", "POST"])
def new_student():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
    Adds a new student to the database and returns the new student's JSON.
    :return: {"student": [student JSON]}, 200 - success/ 500 - server error
    """
    data = request.get_json()
    response = new(Student, data)
    return response


@app.route("/del_student", methods=["OPTIONS", "DELETE"])
def del_student():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
        Deletes a student from the database.
        :return: 200 - success/ 500 - server error
    """
    response = delete(Student, "StudentID")
    return response


@app.route("/update_student", methods=["OPTIONS", "PUT"])
def update_student():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
        Updates a student in the database. The StudentID must be provided in the JSON.
        :return: {"student": [student JSON]}, 200 - success/ 500 - server error
    """
    response = update(Student)
    return response


# Session Table

@app.route("/get_session", methods=["OPTIONS", "GET"])
def get_session():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
    If a SessionID is provided, it will return the session with that ID.
    Otherwise, it will get all sessions from the database.
    :return: {"sessions": [session JSON]}, 200 - success/ 500 - server error
    """
    response = get(Session, "SessionID")
    return response


@app.route("/new_session", methods=["OPTIONS", "POST"])
def new_session():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
    Adds a new session to the database and returns the new session's JSON.
    :return: {"session": [session JSON]}, 200 - success/ 500 - server error
    """
    try:
        data = request.get_json()
        try:
            print(data["StartTime"])
            print(data["EndTime"])
            data["StartTime"] = datetime.strptime(data["StartTime"], "%Y-%m-%dT%H:%M:00.000Z")
            data["EndTime"] = datetime.strptime(data["EndTime"], "%Y-%m-%dT%H:%M:00.000Z")
        except ValueError:
            return {}, 400
    except Exception as e:
        traceback.print_exception(e)
        return {}, 500
    response = new(Session, data)
    return response


@app.route("/del_session", methods=["OPTIONS", "DELETE"])
def del_session():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
        Deletes a session from the database.
        :return: 200 - success/ 500 - server error
    """
    response = delete(Session, "SessionID")
    return response


@app.route("/update_session", methods=["OPTIONS", "PUT"])
def update_session():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
        Updates a session in the database. The SessionID must be provided in the JSON.
        :return: {"session": [session JSON]}, 200 - success/ 500 - server error
    """

    try:
        data = request.get_json()
        timeChange = False
        try:
            if "StartTime" in data:
                timeChange = True
                data["StartTime"] = datetime.strptime(data["StartTime"], "%Y-%m-%dT%H:%M:00.000Z")
            if "EndTime" in data:
                timeChange = True
                data["EndTime"] = datetime.strptime(data["EndTime"], "%Y-%m-%dT%H:%M:00.000Z")
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
                #return jsonify({Event.__name__: [row.to_json()]}), 200

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
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
    If an EventID is provided, it will return the event with that ID.
    Otherwise, it will get all events from the database.
    :return: {"events": [event JSON]}, 200 - success/ 500 - server error
    """
    response = get(Event, "EventID")
    return response


@app.route("/new_event", methods=["OPTIONS", "POST"])
def new_event():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
    Adds a new event to the database and returns the new event's JSON.
    :return: {"event": [event JSON]}, 200 - success/ 500 - server error
    """
    data = request.get_json()
    try:
        session, status = get_session()
        session = session.json["Session"][0]
        if status != 200:
            return {}, 500
        data["StudentID"] = session["StudentID"]
        student, status = get_student()
        student = student.json["Student"][0]
        if status != 200:
            return {}, 500
        data["ParentID"] = student["ParentID"]
        parent, status = get_parent()
        parent = parent.json["Parent"][0]
        if status != 200:
            return {}, 500
        data["BusinessID"] = student["BusinessID"]
        business, status = get_business()
        business = business.json["Business"][0]
        if status != 200:
            return {}, 500
        del data["BusinessID"]
        week_start = datetime.strptime(session["NextScheduleWeekDate"], "%Y-%m-%d")
        week_start = week_start + timedelta(days=session["Weekday"] - week_start.weekday() - 1)
        del data["NextScheduleWeekDate"]

        start_time = datetime.strptime(session["StartTime"], "%H:%M")
        start_time = datetime(week_start.year, week_start.month, week_start.day, start_time.hour, start_time.minute)
        data["EventDateTimeStart"] = start_time
        start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        end_time = datetime.strptime(session["EndTime"], "%H:%M")
        end_time = datetime(week_start.year, week_start.month, week_start.day, end_time.hour, end_time.minute)
        data["EventDateTimeEnd"] = end_time
        end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        data["EventName"] = session["SessionName"]
        eventBody = {
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
                "dateTime": start_time,
                "timeZone": "Europe/London"
            },
            "end": {
                "dateTime": end_time,
                "timeZone": "Europe/London"
            }
        }

        response = eventsResource.insert(calendarId=CALENDAR_ID, body=eventBody, conferenceDataVersion=1).execute()
    except Exception as e:
        traceback.print_exception(e)
        return {}, 500
    data["GoogleCalendarID"] = CALENDAR_ID
    data["GoogleEventID"] = response["id"]
    data["GoogleMeetLink"] = response["hangoutLink"]

    del data["StudentID"]
    del data["ParentID"]
    response = new(Event, data)
    return response


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
        if "EventDateTimeStart" in data:
            strEventDateTimeStart = data["EventDateTimeStart"]
            data["EventDateTimeStart"] = datetime.strptime(strEventDateTimeStart, "%Y-%m-%dT%H:%M:%S.000Z")
        if "EventDateTimeEnd" in data:
            strEventDateTimeEnd = data["EventDateTimeEnd"]
            data["EventDateTimeEnd"] = datetime.strptime(strEventDateTimeEnd, "%Y-%m-%dT%H:%M:%S.000Z")

    except Exception as e:
        traceback.print_exception(e)
        return {}, 500
    response = update(Event)
    event_json = response[0].json["Event"][0]
    try:
        json_body = {}
        if "EventDateTimeStart" in data:
            json_body["start"] = {"dateTime": strEventDateTimeStart, "timeZone": "Europe/London"}
        if "EventDateTimeEnd" in data:
            json_body["end"] = {"dateTime": strEventDateTimeEnd, "timeZone": "Europe/London"}
        if "EventName" in data:
            json_body["summary"] = data["EventName"]
        eventsResource.patch(calendarId=event_json["GoogleCalendarID"], eventId=event_json["GoogleEventID"],
                             body=json_body).execute()
    except Exception as e:
        traceback.print_exception(e)
        return {}, 500
    return response


@app.route("/del_event", methods=["OPTIONS", "DELETE"])
def del_event():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    """
        Deletes an event from the database.
        :return: 200 - success/ 500 - server error
    """
    response, status = delete(Event, "EventID")
    try:
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
    new(Parent, {"FirstName": "John", "LastName": "Doe", "Email": "jd@gmail.com", "PhoneNumber":1234})
    new(Business, {"BusinessName": "Tutoring", "FirstName": "Jamal", "LastName": "Dequavious", "Email": "jamal@mail.com", "PhoneNumber":1234})
    new(Student, {"FirstName": "Jane", "LastName": "Dale", "YearGrade": 12, "Email": "dale@mailo.co", "PhoneNumber":1234, "BusinessID": 1, "ParentID": 1})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
