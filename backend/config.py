from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

PATH = os.path.dirname(os.path.realpath(__file__))

app = Flask("Tutoring Database")
CORS(app)

if os.environ.get("TESTMODE") == "1":
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    print("Running in test mode")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{PATH}\\TutoringDatabase.db"
    print("Running in production mode")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
