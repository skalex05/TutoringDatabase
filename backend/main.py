import googleapiclient.errors
import sqlalchemy.exc
from flask import request, jsonify
from tables import (Parent, Business, Student, Session, Event,
                    db, app,
                    CALENDAR_ID, eventsResource, gmailMessagesResource,
                    TIME_FORMAT, SCHEDULE_X_WEEKS)
import traceback
import uuid
import base64
from email.mime.text import MIMEText

from datetime import datetime, timedelta
from event_scheduler import EventScheduler

scheduler = None


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

@app.route("/get_parent", methods=["OPTIONS", "GET", "POST"])
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

    students = Student.query.filter_by(BusinessID=data["ParentID"])
    for student in students:
        sessions = Session.query.filter_by(StudentID=student.StudentID)
        for session in sessions:
            update_session({"SessionID": session.SessionID})

    return response


# Business Table

@app.route("/get_business", methods=["OPTIONS", "GET", "POST"])
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

    students = Student.query.filter_by(BusinessID=data["BusinessID"])
    for student in students:
        sessions = Session.query.filter_by(StudentID=student.StudentID)
        for session in sessions:
            update_session({"SessionID": session.SessionID})

    return response


# Student Table

@app.route("/get_student", methods=["OPTIONS", "GET", "POST"])
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

    sessions = Session.query.filter_by(StudentID=data["StudentID"])
    for session in sessions:
        update_session({"SessionID": session.SessionID})

    return response


# Session Table

@app.route("/get_session", methods=["OPTIONS", "GET", "POST"])
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
        data["NextSchedule"] = (data["StartTime"] - timedelta(days=data["StartTime"].weekday())).date()
    except ValueError:
        return {}, 400

    response = new(Session, data)

    scheduler.schedule_session(response[0].json["Session"][0]["SessionID"])

    return response


@app.route("/del_session", methods=["OPTIONS", "DELETE"])
def del_session():
    """
        Deletes a session from the database.
        :return: 200 - success/ 500 - server error
    """
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    data = request.get_json()

    try:
        events = Event.query.filter_by(SessionID=data["SessionID"])
        for event in events:
            del_event({"EventID": event.EventID})
    except Exception as e:
        traceback.print_exception(e)
        return {}, 500
    response = delete(Session, data)

    scheduler.remove_session(data["SessionID"])

    return response


@app.route("/update_session", methods=["OPTIONS", "PUT"])
def update_session(data=None):
    """
        Updates a session in the database. The SessionID must be provided in the JSON.
        :return: {"session": [session JSON]}, 200 - success/ 500 - server error
    """
    try:
        if not data:
            if request.method == "OPTIONS":
                return {"Access-Control-Allow-Origin": "*"}
            data = request.get_json()

        session, _ = get(Session, {"SessionID": data["SessionID"]})
        session = session.json["Session"][0]
        time_change = False
        start_time_offset = None
        end_time_offset = None

        if "StartTime" in data:
            time_change = True
            data["StartTime"] = datetime.strptime(data["StartTime"], TIME_FORMAT)
            start_time_offset = data["StartTime"] - datetime.strptime(session["StartTime"], TIME_FORMAT)
        if "EndTime" in data:
            time_change = True
            data["EndTime"] = datetime.strptime(data["EndTime"], TIME_FORMAT)
            end_time_offset = data["EndTime"] - datetime.strptime(session["EndTime"], TIME_FORMAT)
        if "NextSchedule" in data:
            data["NextSchedule"] = datetime.strptime(data["NextSchedule"], "%Y-%m-%d")

        response = update(Session, data)

        student, _ = get(Student, {"StudentID": session["StudentID"]})
        student = student.json["Student"][0]

        business, _ = get(Business, {"BusinessID": student["BusinessID"]})
        business = business.json["Business"][0]

        parent, _ = get(Parent, {"ParentID": student["ParentID"]})
        parent = parent.json["Parent"][0]

        events = Event.query.filter_by(SessionID=data["SessionID"])
        for event in events:
            event_json = {"EventID": event.EventID,
                          "Rescheduled": False}
            if time_change:
                if event.StartTime > datetime.now() and not event.Rescheduled:
                    if start_time_offset:
                        event_json["StartTime"] = datetime.strftime(event.StartTime + start_time_offset, TIME_FORMAT)
                    if end_time_offset:
                        event_json["EndTime"] = datetime.strftime(event.EndTime + end_time_offset, TIME_FORMAT)
            if data["SessionName"]:
                event_json["EventName"] = data["SessionName"]

            desc = (f"{session['Subject']} session for {student['FirstName']} {student['LastName']}\n"
                    f"Contact Details:\n"
                    f"{business['BusinessName']} - {business['Email']} - {business['PhoneNumber']}\n"
                    f"{parent['FirstName']} {parent['LastName']} - {parent['Email']} - {parent['PhoneNumber']}\n"
                    f"{student['FirstName']} {student['LastName']} - {student['Email']} - {student['PhoneNumber']}")
            event_json["Description"] = desc

            update_event(event_json)

        return response
    except ValueError:
        return {}, 400
    except Exception as e:
        traceback.print_exception(e)
        return {}, 500


# Event Table

@app.route("/get_event", methods=["OPTIONS", "GET", "POST"])
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


@app.route("/get_event_period", methods=["OPTIONS", "POST"])
def get_event_period():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}

    try:
        data = request.get_json()
        period_start = datetime.strptime(data["Start"], "%Y-%m-%d")
        period_end = datetime.strptime(data["End"], "%Y-%m-%d")
        events = Event.query.filter(Event.StartTime >= period_start).filter(Event.EndTime <= period_end).all()
        json = jsonify({"Event": [event.to_json() for event in events]})
        return json, 200
    except Exception as e:
        traceback.print_exception(e)
        return {}, 500


@app.route("/new_event", methods=["OPTIONS", "POST"])
def new_event(data=None):
    """
        Adds a new event to the database and returns the new event's JSON.
        :return: {"event": [event JSON]}, 200 - success/ 500 - server error
    """
    if not data:
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

        data["EventName"] = session["SessionName"]
        desc = (f"{session['Subject']} session for {student['FirstName']} {student['LastName']}\n"
                f"Contact Details:\n"
                f"{business['BusinessName']} - {business['Email']} - {business['PhoneNumber']}\n"
                f"{parent['FirstName']} {parent['LastName']} - {parent['Email']} - {parent['PhoneNumber']}\n"
                f"{student['FirstName']} {student['LastName']} - {student['Email']} - {student['PhoneNumber']}\n")
        data["Description"] = desc
        event_body = {
            "attendees": [
                {"email": parent["Email"]},
                {"email": student["Email"]}
            ],
            "summary": session["SessionName"],
            "description": data["Description"],
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
        try:
            response = eventsResource.insert(calendarId=CALENDAR_ID,
                                             body=event_body,
                                             conferenceDataVersion=1,
                                             sendUpdates="none").execute()
            data["GoogleEventID"] = response["id"]
            data["GoogleMeetLink"] = response["hangoutLink"]
        except Exception as e:
            data["GoogleEventID"] = None
            data["GoogleMeetLink"] = None
            traceback.print_exception(e)

        data["StartTime"] = datetime.strptime(data["StartTime"], TIME_FORMAT)
        data["EndTime"] = datetime.strptime(data["EndTime"], TIME_FORMAT)
        data["GoogleCalendarID"] = CALENDAR_ID

        data["LinkEmailSent"] = False
        data["DebriefEmailSent"] = False
        data["Paid"] = False
        data["Rescheduled"] = False
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

        timeChange = False
        if "StartTime" in data:
            timeChange = True
            data["StartTime"] = datetime.strptime(data["StartTime"], TIME_FORMAT)

        if "EndTime" in data:
            timeChange = True
            data["EndTime"] = datetime.strptime(data["EndTime"], TIME_FORMAT)

        if timeChange and "Rescheduled" not in data:
            data["Rescheduled"] = True

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
        if "Description" in data:
            json_body["description"] = data["Description"]
        if json_body != {}:
            try:
                eventsResource.patch(calendarId=event_json["GoogleCalendarID"], eventId=event_json["GoogleEventID"],
                                 body=json_body).execute()
            except Exception as e:
                traceback.print_exception(e)
        return response
    except Exception as e:
        traceback.print_exception(e)
        return {}, 500


@app.route("/del_event", methods=["OPTIONS", "DELETE"])
def del_event(data=None):
    """
        Deletes an event from the database.
        :return: 200 - success/ 500 - server error
    """
    try:
        if not data:
            if request.method == "OPTIONS":
                return {"Access-Control-Allow-Origin": "*"}
            data = request.get_json()
        response, status = delete(Event, data)
        if status != 200:
            return {}, status
        calendarID = response.json["Event"][0]["GoogleCalendarID"]
        eventID = response.json["Event"][0]["GoogleEventID"]
        try:
            eventsResource.delete(calendarId=calendarID, eventId=eventID).execute()
        except Exception as e:
            traceback.print_exception(e)
    except Exception as e:
        traceback.print_exception(e)
        return {}, 500

    return response


def check_session_for_schedule(session_id):
    with app.app_context():
        session = Session.query.filter_by(SessionID=session_id).first()
        if not session.Schedule:
            return
        next_schedule = session.NextSchedule

        schedule_until = datetime.now().date() + timedelta(days=7 * SCHEDULE_X_WEEKS)
        while next_schedule < schedule_until:
            schedule_date = next_schedule + timedelta(days=session.StartTime.weekday())
            event_data = {"SessionID": session.SessionID,
                          "EventName": session.SessionName,
                          "StartTime": datetime.strftime(
                              datetime.combine(schedule_date, session.StartTime.time()), TIME_FORMAT),
                          "EndTime": datetime.strftime(
                              datetime.combine(schedule_date, session.EndTime.time()), TIME_FORMAT),
                          "LinkEmailSent": False,
                          "DebriefEmailSent": False,
                          }
            new_event(event_data)
            next_schedule = next_schedule + timedelta(days=7)

        update(Session, {
            "SessionID": session.SessionID,
            "NextSchedule": next_schedule
        })
        next_schedule = datetime.combine(next_schedule, datetime.min.time())
        scheduler.schedule_session(session_id, next_schedule.timestamp())

@app.route("/get_event_email_info", methods = ["OPTIONS","GET"])
def get_event_email_info():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}
    try:
        event_id = request.args["event_id"]
    except KeyError:
        return {}, 400

    emails = db.session.query(Student.Email, Parent.Email, Business.Email, Session.Subject,
                              Parent.FirstName, Parent.LastName, Student.FirstName, Student.LastName).filter(
                               Event.EventID == event_id).filter(
                               Session.SessionID == Event.SessionID).filter(
                               Student.StudentID == Session.StudentID).filter(
                               Parent.ParentID == Student.ParentID).filter(
                               Business.BusinessID == Student.BusinessID).first()

    return {
        "StudentEmail": emails[0],
        "ParentEmail": emails[1],
        "BusinessEmail": emails[2],
        "Subject": emails[3],
        "ParentName": emails[4] + " " + emails[5],
        "StudentName": emails[6] + " " + emails[7],
        "Sender": "Alex"
    }, 200


@app.route("/send_email", methods=["OPTIONS","POST"])
def send_email():
    if request.method == "OPTIONS":
        return {"Access-Control-Allow-Origin": "*"}

    try:
        data = request.get_json()
        message = MIMEText(data["Body"], "plain")
        message["to"] = data["Recipients"]
        message["from"] = "alexdent005@gmail.com"
        message["subject"] = data["Subject"]
        encoded_message = {"raw": base64.urlsafe_b64encode(message.as_bytes()).decode()}

        gmailMessagesResource.send(userId="me", body=encoded_message).execute()
    except Exception as e:
        traceback.print_exception(e)
        return {}, 400

    return {}, 200

if __name__ == "__main__":
    # Create DB if one does not already exist
    with app.app_context():
        db.create_all()
        # new(Parent, {"FirstName": "John", "LastName": "Doe", "Email": "jd@gmail.com", "PhoneNumber": 1234})
        # new(Business,
        #     {"BusinessName": "Tutoring", "FirstName": "Jamal", "LastName": "Dequavious", "Email": "jamal@mail.com",
        #      "PhoneNumber": 1234})
        # new(Student,
        #     {"FirstName": "Jane", "LastName": "Dale", "YearGrade": 12, "Email": "dale@mailo.co", "PhoneNumber": 1234,
        #      "BusinessID": 1, "ParentID": 1})
        # startTime = datetime.strptime("2024-07-28T12:00:00.000Z", TIME_FORMAT)
        # new(Session, {"StudentID": 1,
        #               "SessionName": "Maths Session",
        #               "Subject": "Math",
        #               "StartTime": startTime,
        #               "EndTime": datetime.strptime("2024-07-28T13:00:00.000Z", TIME_FORMAT),
        #               "Pay": 20,
        #               "Schedule": True,
        #               "NextSchedule": (startTime - timedelta(days=startTime.weekday())).date(),
        #               "Notes": "Very educational session"})

        sessions, _ = get(Session, {})
        sessions = sessions.json["Session"]

        scheduler = EventScheduler(check_session_for_schedule)

        for session in sessions:
            if session["Schedule"]:
                scheduler.schedule_session(session["SessionID"])
        scheduler.start()
        app.run(port=5000)
        scheduler.join()
