import React from "react";
import "./roweditor.css";

export const RowEditor = (props) => {
    const [errMsg, setErrMsg] = React.useState("");

    if (props.rowValues["Name"] === undefined) {
        props.rowValues["Name"] = props.rowValues["FirstName"] !== undefined && props.rowValues["LastName"] !== undefined ? props.rowValues["FirstName"] + " " + props.rowValues["LastName"] : "";
    }
    if (props.rowValues["StudentID"] === undefined && props.students !== undefined && props.students.length > 0) {
        props.rowValues["StudentID"] = props.students[0]["StudentID"];
    }

    const onSubmit = (e) => {
        e.preventDefault();

        for (const field of ["SessionName", "StudentID","Subject", "Weekday","NextScheduleWeekDate","StartTime","EndTime","Pay","Schedule"]) {
            if (props.rowValues[field] === undefined || props.rowValues[field] === "") {
                setErrMsg("Please fill out all fields");
                return;
            }
        }

        let json = {
            "SessionID": props.rowValues["SessionID"],
            "SessionName": props.rowValues["SessionName"],
            "StudentID": props.rowValues["StudentID"],
            "Weekday": props.rowValues["Weekday"],
            "Subject": props.rowValues["Subject"],
            "NextScheduleWeekDate": props.rowValues["NextScheduleWeekDate"],
            "StartTime": props.rowValues["StartTime"],
            "EndTime": props.rowValues["EndTime"],
            "Pay": props.rowValues["Pay"],
            "Schedule": props.rowValues["Schedule"]
        }

        if (props.editorMode === "add") {
            props.add(json);
        }
        else if (props.editorMode === "edit") {
            props.update(json);
        }
        props.setShowEditor(false);
        setErrMsg("")
    }

    return (
        <div className = "RowEditor-Container" onClick={(e) =>
        {
            if (e.target.className === "RowEditor-Container") {
                props.setShowEditor(false);
            }
        }}>
            <div className= "RowEditor">
                <form onSubmit={onSubmit}>
                    <div>
                        <label htmlFor="SessionName">Session Title</label>
                        <input type="text" defaultValue={props.rowValues["SessionName"]} id="SessionName" name="SessionName"
                               onChange={(e) => props.rowValues["SessionName"] = e.target.value}/>
                    </div>
                    <div>
                        <label htmlFor="Subject">Subject</label>
                        <input type="text" defaultValue={props.rowValues["Subject"]} id="Subject" name="Subject"
                               onChange={(e) => props.rowValues["Subject"] = e.target.value}/>
                    </div>
                    <div>
                        <label htmlFor="Student">Student Name</label>
                        <select defaultValue={props.rowValues["StudentID"]} id="StudentID" name="StudentID"
                                onChange={(e) => props.rowValues["StudentID"] = e.target.value}>
                            {props.students.map(student => {
                                return <option value={student["StudentID"]}>{student["FirstName"]+" "+student["LastName"]}</option>
                            })}
                        </select>
                    </div>
                    <div>
                        <label htmlFor="Weekday">Weekday</label>
                        <select defaultValue={props.rowValues["Weekday"]} id="Weekday" name="Weekday"
                                onChange={(e) => props.rowValues["Weekday"] = e.target.value}>
                            {["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"].map((day, i) => {
                                return <option value={i}>{day}</option>
                            })}
                        </select>
                    </div>
                    <div>
                        <label>Next Schedule Date</label>
                        <input type="date" defaultValue={props.rowValues["NextScheduleWeekDate"]} id="NextScheduleWeekDate" name="NextScheduleWeekDate"
                               onChange={(e) => props.rowValues["NextScheduleWeekDate"] = e.target.value}/>
                    </div>
                    <div>
                        <label>Start Time</label>
                        <input type="time" defaultValue={props.rowValues["StartTime"]} id="StartTime" name="StartTime"
                                 onChange={(e) => props.rowValues["StartTime"] = e.target.value}/>
                    </div>
                    <div>
                        <label>End Time</label>
                        <input type="time" defaultValue={props.rowValues["EndTime"]} id="EndTime" name="EndTime"
                               onChange={(e) => props.rowValues["EndTime"] = e.target.value}/>
                    </div>
                    <div>
                        <label htmlFor="Pay">Pay</label>
                        <input type="text" defaultValue={props.rowValues["Pay"]} id="Pay" name="Pay"
                               onChange={(e) => props.rowValues["Pay"] = e.target.value}/>
                    </div>
                    <div>
                        <label htmlFor="Schedule">Schedule</label>
                        <input type="checkbox" defaultChecked={props.rowValues["Schedule"]} id="Schedule" name="Schedule"
                               onChange={(e) => props.rowValues["Schedule"] = e.target.checked}/>
                    </div>
                    <button type="submit">Submit</button>
                </form>
                <div className="Error-Message">{errMsg}</div>
            </div>
        </div>
    );
}