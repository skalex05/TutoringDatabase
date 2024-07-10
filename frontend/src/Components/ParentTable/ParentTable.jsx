import {useEffect, useState} from "react";
import {BsFillTrashFill, BsFillPencilFill} from "react-icons/bs";
import {RowEditor} from "./RowEditor";

function ParentTable (props) {
    const [showEditor, setShowEditor] = useState(false);
    const [editorMode, setEditorMode] = useState("Add");
    const [editParentID, setEditParentID] = useState(null);
    const [parents , setParents] = useState([]);

    const fetchData = async () => {
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
    }

    const addParent = async (parent) => {
        fetch('http://localhost:5000/new_parent',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'POST',
                body: JSON.stringify(parent)
            }
        ).then(() => {
            fetchData();
        }).catch(err => {
            console.log(err)
        })
    }

    const updateParent = async (parent) => {
        fetch('http://localhost:5000/update_parent',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'PUT',
                body: JSON.stringify(parent)
            }
        ).then(() => {
            fetchData();
        }).catch(err => {
            console.log(err)
        })
    }

    const deleteParent = async (parent) => {
        fetch('http://localhost:5000/del_parent',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'DELETE',
                body: JSON.stringify({
                    "ParentID" : parent["ParentID"]
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
            update={updateParent}
            add={addParent}
            rowValues = {editorMode === "edit" ? JSON.parse(JSON.stringify(parents.find(business => business["ParentID"] === editParentID))) : {}}
        />}
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone Number</th>
                </tr>
                {parents.map(parent => {
                    return <tr>
                        <td>{parent["FirstName"]+" "+parent["LastName"]}</td>
                        <td>{parent["Email"]}</td>
                        <td>{parent["PhoneNumber"]}</td>
                        <td>
                            <span>
                                <button onClick={() => deleteParent(parent)}>
                                    <BsFillTrashFill/></button>
                                <button onClick={() => {
                                    setEditParentID(parent["ParentID"]);
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

export default ParentTable;