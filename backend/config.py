from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

PATH = os.path.dirname(os.path.realpath(__file__))
CLIENT_SECRET_FILE = "client_secret.json"
# Required scopes for the application from Google apis
SCOPES = ["https://www.googleapis.com/auth/meetings.space.created",
          "https://www.googleapis.com/auth/gmail.send",
          "https://www.googleapis.com/auth/calendar"]

# Try and get an oauth token from the token.json file
creds = None
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

# If the credentials are invalid, refresh them
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server()
    with open("token.json", "w") as token:
        token.write(creds.to_json())

# Build the services for the application
calendar_service = build("calendar", "v3", credentials=creds)
calendarResource = calendar_service.calendars()
eventsResource = calendar_service.events()
gmail_service = build("gmail", "v1", credentials=creds)

try:
    with open("calendarId.txt", "r") as file:
        CALENDAR_ID = file.read()
except FileNotFoundError:
    CALENDAR_ID = None

# If the tutoring calendar is not found, create a new calendar
try:
    tutoringCalendar = calendarResource.get(calendarId=CALENDAR_ID).execute()
except (HttpError, TypeError):
    tutoringCalendar = calendarResource.insert(body={"summary": "Tutoring"}).execute()
    CALENDAR_ID = tutoringCalendar["id"]
    with open("calendarId.txt", "w") as file:
        file.write(CALENDAR_ID)

# Initialize the Flask application
app = Flask("Tutoring Database")
CORS(app)

# If the environment variable TESTMODE is set to 0, run the application in production mode

if os.environ.get("TESTMODE") != "0":
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    print("Running in test mode")
else:
    raise Exception("Careful now!")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{PATH}\\TutoringDatabase.db"
    print("Running in production mode")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db = SQLAlchemy(app, )
