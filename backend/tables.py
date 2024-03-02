from config import db, app
from datetime import datetime

class Parent(db.Model):
    ParentID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(20))
    LastName = db.Column(db.String(40))
    Email = db.Column(db.String(50))
    PhoneNumber = db.Column(db.String(11))
    students = db.relationship("Student", backref="parent", lazy=True)

    def to_json(self):
        return {
            "ParentID": self.ParentID,
            "FirstName": self.FirstName,
            "LastName": self.LastName,
            "Email": self.Email,
            "PhoneNumber": self.PhoneNumber
        }


class Business(db.Model):
    BusinessID = db.Column(db.Integer, primary_key=True)
    BusinessName = db.Column(db.String(40))
    FirstName = db.Column(db.String(20))
    LastName = db.Column(db.String(40))
    Email = db.Column(db.String(50))
    PhoneNumber = db.Column(db.String(11))
    students = db.relationship("Student", backref="business", lazy=True)

    def to_json(self):
        return {
            "BusinessID": self.BusinessID,
            "BusinessName": self.BusinessName,
            "FirstName": self.FirstName,
            "LastName": self.LastName,
            "Email": self.Email,
            "PhoneNumber": self.PhoneNumber
        }


class Student(db.Model):
    StudentID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(20))
    LastName = db.Column(db.String(40))
    YearGrade = db.Column(db.Integer)
    Email = db.Column(db.String(50))
    PhoneNumber = db.Column(db.String(11))
    BusinessID = db.Column(db.Integer, db.ForeignKey("business.BusinessID"), nullable=False)
    ParentID = db.Column(db.Integer, db.ForeignKey("parent.ParentID"), nullable=False)
    sessions = db.relationship("Session", backref="student", lazy=True)

    def to_json(self):
        return {
            "StudentID": self.StudentID,
            "FirstName": self.FirstName,
            "LastName": self.LastName,
            "YearGrade": self.YearGrade,
            "Email": self.Email,
            "PhoneNumber": self.PhoneNumber,
            "BusinessID": self.BusinessID,
            "ParentID": self.ParentID
        }


class Session(db.Model):
    SessionID = db.Column(db.Integer, primary_key=True)
    SessionName = db.Column(db.String(50))
    StudentID = db.Column(db.Integer, db.ForeignKey("student.StudentID"), nullable=False)
    Subject = db.Column(db.String(50))
    StartWeekDate = db.Column(db.Date)
    WeekdayInt = db.Column(db.Integer)
    StartTime = db.Column(db.Time)
    EndTime = db.Column(db.Time)
    Pay = db.Column(db.Float)

    def to_json(self):
        return {
            "SessionID": self.SessionID,
            "SessionName": self.SessionName,
            "StudentID": self.StudentID,
            "Subject": self.Subject,
            "StartWeekDate": self.StartWeekDate.strftime("%Y-%m-%d") if self.StartWeekDate else None,
            "WeekdayInt": self.WeekdayInt,
            "StartTime": self.StartTime.strftime("%H:%M") if self.StartTime else None,
            "EndTime": self.EndTime.strftime("%H:%M") if self.EndTime else None,
            "Pay": self.Pay
        }

class Event(db.Model):
    EventID = db.Column(db.Integer, primary_key=True)
    SessionID = db.Column(db.Integer, db.ForeignKey("session.SessionID"), nullable=False)
    EventName = db.Column(db.String(50))
    EventDateTime = db.Column(db.DateTime)
    CalendarEventID = db.Column(db.String(50))
    LinkEmailSent = db.Column(db.Boolean)
    FollowupEmailSent = db.Column(db.Boolean)
