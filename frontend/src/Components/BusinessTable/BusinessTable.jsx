import {useEffect, useState} from "react";
import {BsFillTrashFill, BsFillPencilFill} from "react-icons/bs";
import {RowEditor} from "./RowEditor";

function BusinessTable (props) {
    const [showEditor, setShowEditor] = useState(false);
    const [editorMode, setEditorMode] = useState("Add");
    const [editBusinessID, setEditBusinessID] = useState(null);
    const [businesses , setBusinesses] = useState([]);

    const fetchData = async () => {
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

    const addBusiness = async (business) => {
        fetch('http://localhost:5000/new_business',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'POST',
                body: JSON.stringify(business)
            }
        ).then(() => {
            fetchData();
        }).catch(err => {
            console.log(err)
        })
    }

    const updateBusiness = async (business) => {
        fetch('http://localhost:5000/update_business',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'PUT',
                body: JSON.stringify(business)
            }
        ).then(() => {
            fetchData();
        }).catch(err => {
            console.log(err)
        })
    }

    const deleteBusiness = async (business) => {
        fetch('http://localhost:5000/del_business',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'DELETE',
                body: JSON.stringify({
                    "BusinessID" : business["BusinessID"]
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
            update={updateBusiness}
            add={addBusiness}
            rowValues = {editorMode === "edit" ? JSON.parse(JSON.stringify(businesses.find(business => business["BusinessID"] === editBusinessID))) : {}}
        />}
        <table>
            <thead>
                <tr>
                    <th>Business Name</th>
                    <th>Business Owner</th>
                    <th>Business Email</th>
                    <th>Business Phone</th>
                </tr>
                {businesses.map(business => {
                    return <tr>
                        <td>{business["BusinessName"]}</td>
                        <td>{business["FirstName"]+" "+business["LastName"]}</td>
                        <td>{business["Email"]}</td>
                        <td>{business["PhoneNumber"]}</td>
                        <td>
                            <span>
                                <button onClick={() => deleteBusiness(business)}>
                                    <BsFillTrashFill/></button>
                                <button onClick={() => {
                                    setEditBusinessID(business["BusinessID"]);
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

export default BusinessTable;