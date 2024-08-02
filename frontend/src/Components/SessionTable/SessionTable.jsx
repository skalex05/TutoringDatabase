import {useEffect, useState} from "react";
import {BsFillTrashFill, BsFillPencilFill} from "react-icons/bs";
import {RowEditor} from "./RowEditor";
import {format} from "date-fns";

let timeZone = format(new Date(), "OOOO");


function SessionTable (props) {
    const [showEditor, setShowEditor] = useState(false);
    const [editorMode, setEditorMode] = useState("Add");
    const [editSessionID, setEditSessionID] = useState(null);
    const [students , setStudents] = useState([]);
    const [sessions, setSessions] = useState([]);

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
                    <th>Subject</th>
                    <th>Student</th>
                    <th>Schedule Weekly From</th>
                    <th>Start Time</th>
                    <th>End Time</th>
                    <th>Pay</th>
                    <th>Schedule?</th>
                </tr>
                {sessions.map(session => {
                    const student = students.find(student => student["StudentID"] === session["StudentID"]);
                    return <tr>
                        <td>{session["SessionName"]}</td>
                        <td>{session["Subject"]}</td>
                        {student === undefined ? <td>Student Not Found</td> :
                        <td>{student["FirstName"]+" "+student["LastName"]}</td>
                        }
                        <td>{format(session["StartTime"], "cccc do LLLL y")}</td>
                        <td>{format(session["StartTime"], "HH:mm")}</td>
                        <td>{format(session["EndTime"], "HH:mm")}</td>
                        <td>{session["Pay"]}</td>
                        <td>{<input type="checkbox" checked={session["Schedule"]} disabled={true}/>}</td>
                        <td>
                            <span>
                                <button onClick={() => {setSessions(sessions.filter((sess) => sess === session)) ;deleteSession(session)}}>
                                    <BsFillTrashFill/></button>
                                <button onClick={() => {
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
        <button onClick={()=>{
            setShowEditor(true);
            setEditorMode("add");
        }}>Add</button>
        <div>Timezone: {timeZone}</div>
    </div>;
}

export default SessionTable;