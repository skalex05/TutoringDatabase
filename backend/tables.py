from config import db, app


class Parent(db.Model):
    ParentID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(20))
    LastName = db.Column(db.String(40))
    Email = db.Column(db.String(50), unique=True)
    PhoneNumber = db.Column(db.String(11))
    students = db.relationship('Student', backref='parent', lazy=True)

    def to_json(self):
        return {
            'ParentID': self.ParentID,
            'FirstName': self.FirstName,
            'LastName': self.LastName,
            'Email': self.Email,
            'PhoneNumber': self.PhoneNumber
        }


class Business(db.Model):
    BusinessID = db.Column(db.Integer, primary_key=True)
    BusinessName = db.Column(db.String(40))
    FirstName = db.Column(db.String(20))
    LastName = db.Column(db.String(40))
    Email = db.Column(db.String(50), unique=True)
    PhoneNumber = db.Column(db.String(11))
    students = db.relationship('Student', backref='business', lazy=True)

    def to_json(self):
        return {
            'BusinessID': self.BusinessID,
            'BusinessName': self.BusinessName,
            'FirstName': self.FirstName,
            'LastName': self.LastName,
            'Email': self.Email,
            'PhoneNumber': self.PhoneNumber
        }


class Student(db.Model):
    StudentID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(20))
    LastName = db.Column(db.String(40))
    YearGrade = db.Column(db.Integer)
    Email = db.Column(db.String(50), unique=True)
    PhoneNumber = db.Column(db.String(11))
    BusinessID = db.Column(db.Integer, db.ForeignKey('business.BusinessID'), nullable=False)
    ParentID = db.Column(db.Integer, db.ForeignKey('parent.ParentID'), nullable=False)
    sessions = db.relationship('Timetable', backref='student', lazy=True)

    def to_json(self):
        return {
            'StudentID': self.StudentID,
            'FirstName': self.FirstName,
            'LastName': self.LastName,
            'YearGrade': self.YearGrade,
            'Email': self.Email,
            'PhoneNumber': self.PhoneNumber,
            'BusinessID': self.BusinessID,
            'ParentID': self.ParentID
        }


class Timetable(db.Model):
    SessionID = db.Column(db.Integer, primary_key=True)
    StudentID = db.Column(db.Integer, db.ForeignKey('student.StudentID'), nullable=False)
    Subject = db.Column(db.String(50))
    WeekdayInt = db.Column(db.Integer)
    Weekday = db.Column(db.String(10))
    Repeat = db.Column(db.String(10))
    StartTime = db.Column(db.Time)
    EndTime = db.Column(db.Time)
    Pay = db.Column(db.Float)

    def to_json(self):
        return {
            'SessionID': self.SessionID,
            'StudentID': self.StudentID,
            'Subject': self.Subject,
            'WeekdayInt': self.WeekdayInt,
            'Weekday': self.Weekday,
            'Repeat': self.Repeat,
            'StartTime': self.StartTime,
            'EndTime': self.EndTime,
            'Pay': self.Pay
        }

    def __repr__(self):
        return f"Timetable('{self.Subject}', '{self.Weekday}', '{self.StartTime}', '{self.EndTime}', '{self.Pay}')"
