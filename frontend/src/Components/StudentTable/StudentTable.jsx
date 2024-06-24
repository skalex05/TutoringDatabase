import {useEffect, useState} from "react";
import {BsFillTrashFill, BsFillPencilFill} from "react-icons/bs";
import {RowEditor} from "./RowEditor";

function StudentTable (props) {
    const [showEditor, setShowEditor] = useState(false);
    const [editorMode, setEditorMode] = useState("Add");
    const [editStudentID, setEditStudentID] = useState(null);
    const [students , setStudents] = useState([]);
    const [parents, setParents] = useState([]);
    const [businesses, setBusinesses] = useState([])

    const fetchData = async () => {
        fetch('http://localhost:5000/get_student',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'GET'
            }
        ).then(response => {
            response.json().then(data => {
                console.log(data["Student"])
                setStudents(data["Student"]);
            });
        }).catch(err => {
            console.log(err)
        })

        fetch('http://localhost:5000/get_parent',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
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
                headers: {
                    'Content-Type': 'application/json'
                },
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
                    <th>Year Group</th>
                    <th>Student Email</th>
                    <th>Student Phone Number</th>
                    <th>Parent Name</th>
                    <th>Parent Email</th>
                    <th>Parent Phone Number</th>
                    <th>Business Name</th>
                    <th>Business Email</th>
                    <th>Business Phone Number</th>
                </tr>
                {students.map(student => {
                    const parent = parents.find(parent => parent["ParentID"] === student["ParentID"]);
                    const business = businesses.find(business => business["BusinessID"] === student["BusinessID"]);
                    return <tr>
                        <td>{student["FirstName"]+" "+student["LastName"]}</td>
                        <td>{student["YearGrade"]}</td>
                        <td>{student["Email"]}</td>
                        <td>{student["PhoneNumber"]}</td>
                        {parent === undefined ? <><td></td> <td></td> <td></td></>: <>
                        <td>{parent["FirstName"]+" "+parent["LastName"]}</td>
                        <td>{parent["Email"]}</td>
                        <td>{parent["PhoneNumber"]}</td>
                        </>
                        }
                        {business === undefined ? <><td></td> <td></td> <td></td></>: <>
                        <td>{business["BusinessName"]}</td>
                        <td>{business["Email"]}</td>
                        <td>{business["PhoneNumber"]}</td>
                        </>
                        }
                        <td>
                            <span>
                                <button onClick={() => deleteStudent(student)}>
                                    <BsFillTrashFill/></button>
                                <button onClick={() => {
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
        <button onClick={()=>{
            setShowEditor(true);
            setEditorMode("add");
        }}>Add</button>
    </div>;
}

export default StudentTable;