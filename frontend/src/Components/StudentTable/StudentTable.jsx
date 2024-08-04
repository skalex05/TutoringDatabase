import {useEffect, useState} from "react";
import {BsFillTrashFill, BsFillPencilFill} from "react-icons/bs";
import {RowEditor} from "./RowEditor";
import "../../App.css";
import {useNavigate} from "react-router-dom";

function StudentTable (props) {
    const [showEditor, setShowEditor] = useState(false);
    const [editorMode, setEditorMode] = useState("Add");
    const [editStudentID, setEditStudentID] = useState(null);
    const [students , setStudents] = useState([]);
    const [parents, setParents] = useState([]);
    const [businesses, setBusinesses] = useState([])
    const nav = useNavigate();

    const fetchData = async () => {
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

        fetch('http://localhost:5000/get_parent',
            {
                method: 'GET'
            }
        ).then(response => {
            response.json().then(data => {
                setParents(data["Parent"]);
            });
        }).catch(err => {
            console.log(err)
        })

        fetch('http://localhost:5000/get_business',
            {
                method: 'GET'
            }
        ).then(response => {
            response.json().then(data => {
                setBusinesses(data["Business"]);
            });
        }).catch(err => {
            console.log(err)
        })
    }

    const addStudent = async (student) => {
        fetch('http://localhost:5000/new_student',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'POST',
                body: JSON.stringify(student)
            }
        ).then(() => {
            fetchData();
        }).catch(err => {
            console.log(err)
        })
    }

    const updateStudent = async (student) => {
        fetch('http://localhost:5000/update_student',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'PUT',
                body: JSON.stringify(student)
            }
        ).then(() => {
            fetchData();
        }).catch(err => {
            console.log(err)
        })
    }

    const deleteStudent = async (student) => {
        fetch('http://localhost:5000/del_student',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'DELETE',
                body: JSON.stringify({
                    "StudentID" : student["StudentID"]
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
            update={updateStudent}
            add={addStudent}
            parents={parents}
            businesses={businesses}
            rowValues = {editorMode === "edit" ? JSON.parse(JSON.stringify(students.find(student => student["StudentID"] === editStudentID))) : {}}
        />}
        <table>
            <thead>
                <tr>
                    <th>Student Name</th>
                    <th className="vline">Year Group</th>
                    <th className="vline">Email</th>
                    <th className="vline">Phone Number</th>
                    <th className="vline">Parent Name</th>
                    <th className="vline">Email</th>
                    <th className="vline">Phone Number</th>
                    <th className="vline">Business Name</th>
                    <th className="vline">Email</th>
                    <th className="vline">Phone Number</th>
                    <th className="vline" style={{position: "sticky", right:-10}}></th>
                </tr>
                {students.map(student => {
                    const parent = parents.find(parent => parent["ParentID"] === student["ParentID"]);
                    const business = businesses.find(business => business["BusinessID"] === student["BusinessID"]);
                    return <tr>
                        <td>{student["FirstName"]+" "+student["LastName"]}</td>
                        <td className="vline">{student["YearGrade"]}</td>
                        <td className="vline">{student["Email"]}</td>
                        <td className="vline">{student["PhoneNumber"]}</td>
                        {parent === undefined ? <><td></td> <td></td> <td></td></>: <>
                        <td className="vline">{parent["FirstName"]+" "+parent["LastName"]}</td>
                        <td className="vline">{parent["Email"]}</td>
                        <td className="vline"> {parent["PhoneNumber"]}</td>
                        </>
                        }
                        {business === undefined ? <><td></td> <td></td> <td></td></>: <>
                        <td className="vline">{business["BusinessName"]}</td>
                        <td className="vline">{business["Email"]}</td>
                        <td className="vline">{business["PhoneNumber"]}</td>
                        </>
                        }
                        <td className="vline" style={{position: "sticky", right:-10}}>
                            <span>
                                <button className="button-first edit-icons" onClick={() => deleteStudent(student)}>
                                    <BsFillTrashFill/></button>
                                <button className="button-last edit-icons" onClick={() => {
                                    setEditStudentID(student["StudentID"]);
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
        <button className="back button-first" onClick={()=>nav("../")}>Back</button>
        <button className="button-last" onClick={()=>{
            setShowEditor(true);
            setEditorMode("add");
        }}>Add Student</button>
    </div>;
}

export default StudentTable;