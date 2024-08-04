import {useEffect, useState} from "react";
import {BsFillTrashFill, BsFillPencilFill} from "react-icons/bs";
import {RowEditor} from "./RowEditor";
import {format} from "date-fns";
import "../../App.css";
import {useNavigate} from "react-router-dom";

let timeZone = format(new Date(), "OOOO");


function SessionTable (props) {
    const [showEditor, setShowEditor] = useState(false);
    const [editorMode, setEditorMode] = useState("Add");
    const [editSessionID, setEditSessionID] = useState(null);
    const [students , setStudents] = useState([]);
    const [sessions, setSessions] = useState([]);
    const nav = useNavigate();

    const fetchData = async () => {
        fetch('http://localhost:5000/get_session',
            {
                method: 'GET'
            }
        ).then(response => {
            response.json().then(data => {
                for (let session of data["Session"]) {
                    session["StartTime"] =  new Date(session["StartTime"]);
                    session["EndTime"] = new Date(session["EndTime"]);
                }
                setSessions(data["Session"]);
            });
        }).catch(err => {
            console.log(err)
        })

        fetch('http://localhost:5000/get_student',
            {
                method: 'GET'
            }
        ).then(response => {
            response.json().then(data => {
                setStudents(data["Student"]);
            });
        }).catch(err => {
            console.log(err)
        })
    }

    const addSession = async (session) => {
        fetch('http://localhost:5000/new_session',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'POST',
                body: JSON.stringify(session)
            }
        ).then(() => {
            fetchData();
        }).catch(err => {
            console.log(err)
        })
    }

    const updateSession = async (session) => {
        fetch('http://localhost:5000/update_session',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'PUT',
                body: JSON.stringify(session)
            }
        ).then(() => {
            fetchData();
        }).catch(err => {
            console.log(err)
        })
    }

    const deleteSession = async (session) => {
        fetch('http://localhost:5000/del_session',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'DELETE',
                body: JSON.stringify({
                    "SessionID" : session["SessionID"]
                })
            }
        ).then(() => {
            fetchData();
        }).catch(err => {
            console.log(err)
        })
    }

    useEffect(() => {
        fetchData();
    }, []);

    let rowValues = {};
    if (editorMode === "edit") {
        let session = sessions.find(session => session["SessionID"] === editSessionID);
        if (session !== undefined) {
            rowValues = JSON.parse(JSON.stringify(session));
            rowValues["StartTime"] = session["StartTime"];
            rowValues["EndTime"] = session["EndTime"];
        }
    }

    return <div>
        {showEditor && <RowEditor
            editorMode={editorMode}
            setShowEditor={setShowEditor}
            update={updateSession}
            add={addSession}
            students={students}
            rowValues = {rowValues}
        />}
        <table>
            <thead>
                <tr>
                    <th>Session Title</th>
                    <th className="vline">Subject</th>
                    <th className="vline">Student</th>
                    <th className="vline">Weekday</th>
                    <th className="vline">Start Time</th>
                    <th className="vline">End Time</th>
                    <th className="vline">Pay</th>
                    <th className="vline">Scheduled</th>
                    <th className="vline" style={{position: "sticky", right:-10}}></th>
                </tr>
                {sessions.map(session => {
                    const student = students.find(student => student["StudentID"] === session["StudentID"]);
                    return <tr>
                        <td>{session["SessionName"]}</td>
                        <td className="vline">{session["Subject"]}</td>
                        {student === undefined ? <td>Student Not Found</td> :
                        <td className="vline">{student["FirstName"]+" "+student["LastName"]}</td>
                        }
                        <td className="vline">{format(session["StartTime"], "cccc")}</td>
                        <td className="vline">{format(session["StartTime"], "HH:mm")}</td>
                        <td className="vline">{format(session["EndTime"], "HH:mm")}</td>
                        <td className="vline">{session["Pay"]}</td>
                        <td className="vline">{<input type="checkbox" checked={session["Schedule"]} disabled={true}/>}</td>
                        <td className="vline" style={{position: "sticky", right:-10}}>
                            <span>
                                <button className="button-first edit-icons" onClick={() => {setSessions(sessions.filter((sess) => sess === session)) ;deleteSession(session)}}>
                                    <BsFillTrashFill/></button>
                                <button className="button-last edit-icons" onClick={() => {
                                    setEditSessionID(session["SessionID"]);
                                    setEditorMode("edit");
                                    setShowEditor(true);
                                }}>
                                    <BsFillPencilFill/></button>
                            </span>
                        </td>
                    </tr>
                })}
            </thead>
        </table>
        <p className="time-zone-label">Timezone: {timeZone}</p>
        <button className="back button-first" onClick={()=>nav("../")}>Back</button>
        <button className="button-last" onClick={()=>{
            setShowEditor(true);
            setEditorMode("add");
        }}>Add Session</button>

    </div>;
}

export default SessionTable;