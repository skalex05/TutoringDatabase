import React, {useEffect, useState} from "react";
import "../../App.css";
import {addHours, format} from "date-fns";

let timeZone = format(new Date(), "OOOO");

function adjustTime(datetime, timestring) {
    let time = timestring.split(":");
    datetime.setHours(time[0]);
    datetime.setMinutes(time[1]);
}

function adjustDate(datetime, datestring) {
    let time = datestring.split("-");
    datetime.setFullYear(time[0]);
    datetime.setMonth(time[1]-1);
    datetime.setDate(time[2]);
}

export const RowEditor = (props) => {
    const [errMsg, setErrMsg] = useState("");
    const [startTimeUpdated, setStartTimeUpdated] = useState(false);
    const [displayedStart, setDisplayedStart] = useState(props.rowValues["StartTime"] ? format(props.rowValues["StartTime"], "HH:mm") : "");
    const [displayedEnd, setDisplayedEnd] = useState(props.rowValues["EndTime"] ? format(props.rowValues["EndTime"], "HH:mm") : "");

    if (props.rowValues["Name"] === undefined) {
        props.rowValues["Name"] = props.rowValues["FirstName"] !== undefined && props.rowValues["LastName"] !== undefined ? props.rowValues["FirstName"] + " " + props.rowValues["LastName"] : "";
    }
    if (props.rowValues["StudentID"] === undefined && props.students !== undefined && props.students.length > 0) {
        props.rowValues["StudentID"] = props.students[0]["StudentID"];
    }

    if (props.rowValues["NextScheduleWeekDate"] === undefined) {
        props.rowValues["NextScheduleWeekDate"] = new Date().toISOString().split("T")[0];
    }

    if (props.rowValues["Schedule"] === undefined){
        props.rowValues["Schedule"] = true;
    }

    if (props.rowValues["StartTime"] === undefined) {
        props.rowValues["StartTime"] = new Date();
        props.rowValues["StartTime"].setMilliseconds(0);
        props.rowValues["StartTime"].setSeconds(0);
        setDisplayedStart(format(props.rowValues["StartTime"], "HH:mm"));
        props.rowValues["EndTime"] = addHours(props.rowValues["StartTime"],1);
        setDisplayedEnd(format(props.rowValues["EndTime"], "HH:mm"));
    }

    if (startTimeUpdated){
        props.rowValues["EndTime"] = addHours(props.rowValues["StartTime"],1);
        setDisplayedEnd(format(props.rowValues["EndTime"], "HH:mm"))
        setStartTimeUpdated(false);
    }

    const onSubmit = (e) => {
        e.preventDefault();

        for (const field of ["SessionName", "StudentID","Subject","NextScheduleWeekDate","StartTime","EndTime","Pay","Schedule"]) {
            if (props.rowValues[field] === undefined || props.rowValues[field] === "") {
                setErrMsg("Please fill out all fields");
                return;
            }
        }

        let json = {
            "SessionID": props.rowValues["SessionID"],
            "SessionName": props.rowValues["SessionName"],
            "StudentID": props.rowValues["StudentID"],
            "Subject": props.rowValues["Subject"],
            "StartTime":  props.rowValues["StartTime"].toISOString(),
            "EndTime": props.rowValues["EndTime"].toISOString(),
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
                <h2 className="editHeader">{props.editorMode.charAt(0).toUpperCase()+props.editorMode.slice(1)} Session</h2>
                <form onSubmit={onSubmit}>
                    <table style={{maxWidth:"100%", margin:"auto 10px"}}>
                        <tr>
                            <td><label htmlFor="SessionName">Session Title</label></td>
                            <td><input type="text" defaultValue={props.rowValues["SessionName"]} id="SessionName" name="SessionName"
                                            onChange={(e) => props.rowValues["SessionName"] = e.target.value}/></td>
                        </tr>
                        <tr>
                            <td><label htmlFor="Subject">Subject</label></td>
                            <td><input type="text" defaultValue={props.rowValues["Subject"]} id="Subject" name="Subject"
                                       onChange={(e) => props.rowValues["Subject"] = e.target.value}/></td>
                        </tr>
                        <tr>
                            <td><label htmlFor="Student">Student Name</label></td>
                            <td><select defaultValue={props.rowValues["StudentID"]} id="StudentID" name="StudentID"
                                    onChange={(e) => props.rowValues["StudentID"] = e.target.value}>
                                {props.students.map(student => {
                                    return <option value={student["StudentID"]}>{student["FirstName"]+" "+student["LastName"]}</option>
                                })}
                            </select></td>
                        </tr>
                        <tr>
                            <td><label>Start Date</label></td>
                            <td><input type="date" defaultValue={props.rowValues["StartTime"] ? format(props.rowValues["StartTime"], "yyyy-MM-dd") : ""} id="StartDate" name="StartDate"
                                   onChange={(e) => {
                                       adjustDate(props.rowValues["StartTime"], e.target.value);
                                       adjustDate(props.rowValues["EndTime"],e.target.value);
                                       setDisplayedStart(format(props.rowValues["StartTime"], "HH:mm"));
                                       setDisplayedEnd(format(props.rowValues["EndTime"], "HH:mm"));}
                            }/></td>
                        </tr>
                        <tr>
                            <td><label>Start Time</label></td>
                            <td><input type="time" step="300" value={displayedStart} id="StartTime" name="StartTime"
                                     onChange={(e) => {
                                         adjustTime(props.rowValues["StartTime"],e.target.value);
                                         setDisplayedStart(format(props.rowValues["StartTime"], "HH:mm"));
                                         setStartTimeUpdated(true);}}/>
                                <label className="time-zone-label">{timeZone}</label></td>
                        </tr>
                        <tr>
                            <td><label>End Time</label></td>
                            <td><input type="time" step="300" value={displayedEnd} id="EndTime" name="EndTime"
                                   onChange={(e) => {
                                       adjustTime(props.rowValues["EndTime"],e.target.value);
                                       setDisplayedEnd(format(props.rowValues["EndTime"], "HH:mm"));}}/>
                                <label className="time-zone-label">{timeZone}</label></td>
                        </tr>
                        <tr>
                            <td><label htmlFor="Pay">Pay</label></td>
                            <td><input type="text" defaultValue={props.rowValues["Pay"]} id="Pay" name="Pay"
                                       onChange={(e) => props.rowValues["Pay"] = e.target.value}/></td>
                        </tr>
                        <tr>
                            <td><label htmlFor="Schedule">Schedule</label></td>
                            <td><input type="checkbox" defaultChecked={props.rowValues["Schedule"]} id="Schedule" name="Schedule"
                                       onChange={(e) => props.rowValues["Schedule"] = e.target.checked}/></td>
                        </tr>
                    </table>
                    <div style={{textAlign: "center"}}>
                        <button className="button-first button-last" type="submit">Submit</button>
                    </div>
                </form>
                <div className="Error-Message">{errMsg}</div>
            </div>
        </div>
    );
}