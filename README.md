# Tutoring Management System

## Technical Overview
This project is a full-stack web application for managing my tutoring clients.

- The backend consists of a **REST API** powered with **Flask**. All information is stored using **SQLAlchemy** and an **SQLite** database.

- The frontend is a **React** application that allows users to modify and view information through the **Flask API**.

- All backend testing is done in a Pytest environment.

## Features

### View Associated Tutoring Businesses

![Picture of businesses table](README-IMAGES%2FBusinessesTable.png)

- It's possible that an individual may work with multiple tutoring businesses at the same time. 

- They also may also take on clients themselves and so it was an important feature to allow clients to be associated with multiple businesses.

![Picture of adding a new business](README-IMAGES%2FAdd%20Business.png)
![Picture of editing a business' information](README-IMAGES%2FEdit%20Business.png)

### View Associated Parents

![ParentTable.png](README-IMAGES%2FParentTable.png)

- Parent information is stored so that any contact details can be quickly retrieved for any correspondence.

- **Automated emailing** will also require a parent's email address.

Like the business table, parents may be added and modified with appropriate forms.

### View Associated Students

![StudentsTable.png](README-IMAGES%2FStudentsTable.png)

- There is the ability to include contact information for students as well. Typically older students will be able to receive emails directly.
- Each student is associated with a parent and a business to create a network of all necessary contacts.
- The database ensures Referential integrity so that no student can exist without a parent or business.

![Edit Student.png](README-IMAGES%2FEdit%20Student.png)


### View Associated Sessions

![SessionTable.png](README-IMAGES%2FSessionTable.png)

- The main purpose of this application is to track tutoring sessions.
- Each session is associated with a student and a date and time.
- Sessions can be selected to be automatically scheduled each week at the specified time.

![Edit Session.png](README-IMAGES%2FEdit%20Session.png)

### Viewing timetabled sessions

![MonthView.png](README-IMAGES%2FMonthView.png)
![Weekview.png](README-IMAGES%2FWeekview.png)

- A calendar view is available to see all sessions for a given month, week or day.
- The calendar can be synced to a Google Calendar. 
- Parent's and students may also choose to include these events on their Google Calendar.

![Google Calendar.png](README-IMAGES%2FGoogle%20Calendar.png)

### Viewing Individual Events

- Each event on the calendar can be interacted with to bring up a pop-up with more information.
- It is quite often tutoring sessions may need to be rescheduled so each event can be modified to a better time.
- Notes can be written about how sessions are progressing.
- These notes carry over to the next session, so they can be quickly referred back to in the future.
- Each event also has a Google Meet link associated with it. These can be used by tutors to host online sessions for students.

![ViewEventCS.png](README-IMAGES%2FViewEventCS.png)
![ViewEventMaths.png](README-IMAGES%2FViewEventMaths.png)
![ViewEventChemistry.png](README-IMAGES%2FViewEventChemistry.png)

### Automatic Emailing 

- Emails can be sent to:
    - Invite students to sessions.
    - Remind students of upcoming sessions
    - Send debrief emails to parents after sessions to let them know how it went.

- Emails are sent using the **Gmail API**. This requires a Google account to be set up with the necessary permissions prior.
- Emails are autofilled using data associated with the session, so they feel personalised and contain all key information.

![Invite.png](README-IMAGES%2FInvite.png)
![Reminder.png](README-IMAGES%2FReminder.png)
![Debrief.png](README-IMAGES%2FDebrief.png)
