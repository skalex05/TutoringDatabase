import "./eventview.css";
import {format} from "date-fns";
import React, {useEffect, useState, useRef} from "react";
import {useNavigate} from "react-router-dom";

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

function EventView (props) {
    const nav = useNavigate();

    const ref = useRef();
    const [session, setSession] = useState(null);
    const [notes, setNotes] = useState("");
    const [startTime, setStartTime] = useState("");
    const [endTime, setEndTime] = useState("");
    const [displayStartTime, setDisplayStartTime] = useState("");
    const [displayEndTime, setDisplayEndTime] = useState("");
    const [displayDate, setDisplayDate] = useState("");
    const [paid, setPaid] = useState(false);
    const [rescheduled, setRescheduled] = useState(false);
    const [eventChanged, setEventChanged] = useState(false);
    const [sessionChanged, setSessionChanged] = useState(false);

    useEffect(() => {
        const clickOutside = (e) => {
            if (ref.current && !ref.current.contains(e.target)) {
                props.showEvent(false);
                props.fetchData();
            }
        }
        document.addEventListener("mousedown", clickOutside);

        return () => {
            document.removeEventListener("mousedown", clickOutside);
        }
    }, []);

    const fetchData = async () => {
        fetch('http://localhost:5000/get_session',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'POST',
                body: JSON.stringify({
                    "SessionID": props.event["SessionID"]
                })
            }
        ).then(response => {
            response.json().then(data => {
                setNotes(data["Session"][0]["Notes"])
                setSession(data["Session"][0]);
            });
        }).catch(err => {
            console.log(err)
        });
    }

    const updateEvent = async () => {
        fetch('http://localhost:5000/update_event',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'PUT',
                body: JSON.stringify({
                    "EventID": props.event["EventID"],
                    "StartTime": startTime.toISOString(),
                    "EndTime": endTime.toISOString(),
                    "Paid": paid,
                    "Rescheduled": rescheduled
                })
            }
        ).then(() => {
            fetchData();
        }).catch(err => {
            console.log(err)
        })
    }

    const updateSession = async () => {
        fetch('http://localhost:5000/update_session',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'PUT',
                body: JSON.stringify({
                    "SessionID": session["SessionID"],
                    "Notes": notes
                })
            }
        ).then(() => {
            fetchData();
        }).catch(err => {
            console.log(err)
        })
    }

    const deleteEvent = async () => {
        fetch('http://localhost:5000/del_event',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'DELETE',
                body: JSON.stringify({
                    "EventID": props.event["EventID"]
                })
            }
        ).then(() => {
            props.showEvent(false);
            props.fetchData();
        }).catch(err => {
            console.log(err)
        })
    }

    useEffect(() => {
        let start = new Date(Date.parse(props.event["StartTime"]));
        let end = new Date(Date.parse(props.event["EndTime"]));
        setStartTime(start);
        setEndTime(end);
        setDisplayDate(format(start, "yyyy-MM-dd"));
        setDisplayStartTime(format(start, "HH:mm"));
        setDisplayEndTime(format(end, "HH:mm"));
        setPaid(props.event["Paid"]);
        setRescheduled(props.event["Rescheduled"]);
        fetchData();
    }, []);

    return (
        <div className="EventViewContainer" >
            <div className="EventView" ref={ref}>
                <h1>{props.event["EventName"]}</h1>
                <h3 style={{margin:"2px auto"}}><a href={props.event["GoogleMeetLink"]}>Google Meet</a></h3><br/>
                <p style={{margin: "2px auto"}} className="Description">{props.event["Description"]}</p>
                <div className="Event-Info-Wrapper">
                    <table className="Event-Datetime-Table">
                        <tr>
                            <td><label>Start Date</label></td>
                            <td><input type="date" value={displayDate} id="StartDate" name="StartDate"
                                   onChange={(e) => {
                                       let sTemp = startTime;
                                       let eTemp = endTime;
                                       adjustDate(sTemp, e.target.value);
                                       adjustDate(eTemp, e.target.value);
                                       setStartTime(sTemp);
                                       setStartTime(eTemp);
                                       setDisplayDate(format(sTemp, "yyyy-MM-dd"));
                                       setRescheduled(true);
                                       setEventChanged(true);
                                   }}/></td>
                        </tr>
                        <tr>
                            <td><label>Start Time</label></td>
                            <td><input type="time" step="300" value={displayStartTime} id="StartTime" name="StartTime"
                                   onChange={(e) => {
                                       console.log(e.target.value)
                                       let time = startTime;
                                       adjustTime(time, e.target.value);
                                       setStartTime(time);
                                       setDisplayStartTime(format(time, "HH:mm"))
                                       console.log(time);
                                       setRescheduled(true);
                                       setEventChanged(true);
                                   }}/><label className="time-zone-label">{timeZone}</label></td>

                        </tr>
                        <tr>
                            <td><label>End Time</label></td>
                            <td><input type="time" step="300" value={displayEndTime} id="EndTime" name="EndTime"
                                   onChange={(e) => {
                                       let time = endTime;
                                       adjustTime(time, e.target.value);
                                       setEndTime(time);
                                       setDisplayEndTime(format(time, "HH:mm"));
                                       setRescheduled(true);
                                       setEventChanged(true);
                                   }}/><label className="time-zone-label">{timeZone}</label></td>


                        </tr>
                    </table>
                        <div className="Event-Misc">
                            <p style={{margin:"5px"}}>Paid: <input type="checkbox" checked={paid} onChange={(e) => {setPaid(e.target.checked); setEventChanged(true)}}/><br/></p>
                            {props.event["DebriefEmailSent"] ? <></> : Date.now() > endTime ? <div><button style={{width:"155px"}} className="button-first button-last" onClick={()=>{
                            nav("/event-email/" + props.event["EventID"] + "/debrief");
                            }}>Send Debrief Email</button><br/></div> :
                            props.event["LinkEmailSent"] ? <div><button style={{width:"155px"}} className="button-first button-last" onClick={() => {
                                nav("/event-email/" + props.event["EventID"] + "/reminder");
                                }}>Send Reminder</button><br/></div> :
                                                     <div><button style={{width:"155px"}} className="button-first button-last" onClick={() => {
                                                            nav("/event-email/" + props.event["EventID"] + "/invite");
                                                     }}>Send Invite Link</button> <br/></div>
                        }
                            <button style={{width:"155px"}} className="button-first button-last" onClick={()=>{
                                deleteEvent();
                                props.showEvent(false);
                                props.fetchData();
                            }
                            }>Delete Event</button>
                        </div>
                </div>
                <div>
                    <h2 style={{margin: "2px", textWrap: "nowrap"}}>Notes</h2><br/> <textarea className="Notes" maxLength="255" placeholder="Use this to write notes about what is going on in a session." defaultValue={session && notes ? notes : ""} onChange={(e) => {setNotes(e.target.value); setSessionChanged(true)}}/><br/>
                </div>
                <button className="button-first button-last" onClick={() => {
                    if (eventChanged) {
                        updateEvent();
                    }
                    if (sessionChanged) {
                        updateSession();
                    }
                    props.showEvent(false);
                    props.fetchData();
                }}>Save Changes</button>
            </div>
        </div>
    );
}

export default EventView;