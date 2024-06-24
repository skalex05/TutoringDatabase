import {useEffect, useState} from "react";
import {BsFillTrashFill, BsFillPencilFill} from "react-icons/bs";
import {RowEditor} from "./RowEditor";

function SessionTable (props) {
    const [showEditor, setShowEditor] = useState(false);
    const [editorMode, setEditorMode] = useState("Add");
    const [editSessionID, setEditSessionID] = useState(null);
    const [students , setStudents] = useState([]);
    const [sessions, setSessions] = useState([]);

    const fetchData = async () => {
        fetch('http://localhost:5000/get_session',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'GET'
            }
        ).then(response => {
            response.json().then(data => {
                setSessions(data["Session"]);
            });
        }).catch(err => {
            console.log(err)
        })

        fetch('http://localhost:5000/get_student',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
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

    return <div>
        {showEditor && <RowEditor
            editorMode={editorMode}
            setShowEditor={setShowEditor}
            update={updateSession}
            add={addSession}
            students={students}
            rowValues = {editorMode === "edit" ? JSON.parse(JSON.stringify(sessions.find(session => session["SessionID"] === editSessionID))) : {}}
        />}
        <table>
            <thead>
                <tr>
                    <th>Session Title</th>
                    <th>Subject</th>
                    <th>Student</th>
                    <th>Weekday</th>
                    <th>Next Schedule Date</th>
                    <th>Start Time</th>
                    <th>End Time Time</th>
                    <th>Pay</th>
                    <th>Schedule?</th>
                </tr>
                {sessions.map(session => {
                    const student = students.find(student => student["StudentID"] === session["StudentID"]);
                    console.log("The Student: ",student);
                    return <tr>
                        <td>{session["SessionName"]}</td>
                        <td>{session["Subject"]}</td>
                        {student === undefined ? <td>Student Not Found</td> :
                        <td>{student["FirstName"]+" "+student["LastName"]}</td>
                        }
                        <td>{["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"][session["Weekday"]]}</td>
                        <td>{session["NextScheduleWeekDate"]}</td>
                        <td>{session["StartTime"]}</td>
                        <td>{session["EndTime"]}</td>
                        <td>{session["Pay"]}</td>
                        <td>{session["Schedule"]}</td>
                        <td>
                            <span>
                                <button onClick={() => deleteSession(session)}>
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
    </div>;
}

export default SessionTable;