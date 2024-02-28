import sqlite3
import sys
import os
from pandas import read_sql_query

PATH = os.path.dirname(os.path.realpath(__file__))

# Connect to database
conn = sqlite3.connect(f"{PATH}\\TutoringDatabase.db")
csr = conn.cursor()
csr.execute("BEGIN TRANSACTION;")

# Create tables if they don't exist
# Parent Table
csr.execute("""
CREATE TABLE IF NOT EXISTS Parent (
ParentID INTEGER PRIMARY KEY,
FirstName VarChar(20),
LastName VarChar(40),
Email VarChar(50),
PhoneNumber Char(11)
);
""")
# Business Table
csr.execute("""
CREATE TABLE IF NOT EXISTS Business (
BusinessID INTEGER PRIMARY KEY,
BusinessName VarChar(40),
FirstName VarChar(20),
LastName VarChar(40),
Email VarChar(50),
PhoneNumber Char(11)
);
""")

# Student Table
csr.execute("""
CREATE TABLE IF NOT EXISTS Student (
StudentID INTEGER PRIMARY KEY,
FirstName VarChar(20),
LastName VarChar(40),
YearGrade Int,
Email VarChar(50),
PhoneNumber Char(11),
BusinessID INTEGER NOT NULL,
ParentID INTEGER NOT NULL,
FOREIGN KEY (BusinessID) REFERENCES Business (BusinessID),
FOREIGN KEY (ParentID) REFERENCES Parent (ParentID)
);
""")

# Tutoring Session Table
csr.execute("""
CREATE TABLE IF NOT EXISTS Timetable (
SessionID INTEGER PRIMARY KEY,
StudentID INTEGER NOT NULL,
Subject VarChar(50),
WeekdayInt Int Check(Weekday < 8 AND Weekday > 0),
Weekday Char(10) CHECK (Weekday IN ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')),
Repeat Char(10) CHECK (Repeat IN ('No','Weekly','Fortnightly','Monthly')),
StartTime Time NOT NULL,
EndTime Time NOT NULL,
Pay FLOAT,
FOREIGN KEY (StudentID) REFERENCES Student (StudentID)
);
""")


def quit_sql():
    confirm = input("Commit?(Y/n)")
    while confirm not in ["Y", "n"]:
        confirm = input("Commit?(Y/n)")

    if confirm == "Y":
        csr.execute("COMMIT;")
        conn.commit()
        conn.close()
        print("Changes have been committed to the database")
    else:
        csr.execute("ROLLBACK;")
        conn.close()
        print("Aborted. No Changes were made.")
    sys.exit()


def new_record(table, **kwargs):
    keys = kwargs.keys()
    values = [f'"{v}"' for v in kwargs.values()]
    command = f"INSERT INTO {table} ({', '.join(keys)}) VALUES ({', '.join(values)})"
    print(command)
    csr.execute(command)
    print(read_sql_query(f"SELECT * FROM {table}", conn))


def delete_record(table, condition):
    command = f"DELETE FROM {table} WHERE {condition}"
    print(command)
    csr.execute(command)
    print(read_sql_query(f"SELECT * FROM {table}", conn))


def update_record(table, condition, **kwargs):
    for k in kwargs:
        kwargs[k] = f'"{kwargs[k]}"'
    values = [f'"{v}"' for v in kwargs.values()]
    command = f"UPDATE {table} SET {', '.join([f'{k} = {kwargs[k]}' for k in kwargs])} WHERE {condition}"
    print(command)
    csr.execute(command)
    print(read_sql_query(f"SELECT * FROM {args[0]}", conn))


def get_records(table, condition="", *columns):
    if columns:
        columns = ", ".join(columns)
    else:
        columns = "*"
    if condition:
        command = f"SELECT {columns} FROM {table} WHERE {condition}"
    else:
        command = f"SELECT {columns} FROM {table}"
    print(command)
    return csr.execute(command).fetchall()


if len(sys.argv) < 2:
    print("Please provide at least one argument.")
    quit_sql()

op = sys.argv[1]
args = sys.argv[2::]
if op == "New_Business":
    new_record("Business", BusinessName=args[0], FirstName=args[1], LastName=args[2], Email=args[3], PhoneNumber=args[4])
elif op == "New_Student":
    if args[3] == "0":
        args[3] = get_records("Parent", f"ParentID = {args[6]}", "Email")[0][0]
    if args[4] == "0":
        args[4] = get_records("Parent", f"ParentID = {args[6]}", "PhoneNumber")[0][0]

    new_record("Student", FirstName=args[0], LastName=args[1], YearGrade=args[2], Email=args[3],
               PhoneNumber=args[4], BusinessID=args[5], ParentID=args[6])
elif op == "New_Parent":
    new_record("Parent", FirstName=args[0], LastName=args[1], Email=args[2],
               PhoneNumber=args[3])
elif op == "New_Session":
    new_record("Timetable", StudentID=args[0], Weekday=args[1], Repeat=args[2], StartTime=args[3], EndTime=args[4], Pay=args[5])
elif op == "Del" and args[0] in ["Business", "Parent", "Student"]:
    delete_record(args[0], f"{args[0]}ID={args[1]}")
elif op == "Del" and args[0] == "Timetable":
    delete_record("Timetable", f"SessionID={args[0]}")
elif op == "Update" and args[0] in ["Business", "Parent", "Student"]:
    print(args[2::])
    kwArgs = {}
    for i in range(2, len(args), 2):
        kwArgs[args[i]] = args[i+1]
    update_record(args[0], f"{args[0]}ID = {args[1]}", **kwArgs)
elif op == "Update" and args[0] == "Timetable":
    kwArgs = {}
    for i in range(2, len(args), 2):
        kwArgs[args[i]] = args[i+1]
    update_record("Timetable", f"SessionID = {args[1]}", **kwArgs)
elif op == "View":
    print(read_sql_query(f"SELECT * FROM {args[0]}", conn))
    sys.exit()
elif op == "Timetable":
    print(read_sql_query(f"SELECT Subject,Student.FirstName,Student.LastName,Weekday,Repeat,StartTime,EndTime,BusinessName,Business.Email,Student.Email FROM Timetable LEFT JOIN Student ON Timetable.StudentID = Student.StudentID LEFT JOIN Business ON Business.BusinessID = Student.BusinessID LEFT JOIN Parent ON Parent.ParentID = Student.StudentID ORDER BY WeekdayInt", conn))
    sys.exit()
else:
    print("No such command")
    sys.exit()

quit_sql()