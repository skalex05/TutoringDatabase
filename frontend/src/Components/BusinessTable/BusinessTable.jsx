import {useEffect, useState} from "react";
import {BsFillTrashFill, BsFillPencilFill} from "react-icons/bs";
import {RowEditor} from "./RowEditor";
import "../../App.css";
import {useNavigate} from "react-router-dom";

function BusinessTable (props) {
    const [showEditor, setShowEditor] = useState(false);
    const [editorMode, setEditorMode] = useState("Add");
    const [editBusinessID, setEditBusinessID] = useState(null);
    const [businesses , setBusinesses] = useState([]);
    const nav = useNavigate();

    const fetchData = async () => {
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
                    <th className="vline">Business Owner</th>
                    <th className="vline">Business Email</th>
                    <th className="vline">Business Phone</th>
                    <th className="vline"></th>
                </tr>
                {businesses.map(business => {
                    return <tr>
                        <td>{business["BusinessName"]}</td>
                        <td className="vline">{business["FirstName"]+" "+business["LastName"]}</td>
                        <td className="vline">{business["Email"]}</td>
                        <td className="vline">{business["PhoneNumber"]}</td>
                        <td className="vline">
                            <span>
                                <button className="button-first edit-icons" onClick={() => deleteBusiness(business)}>
                                    <BsFillTrashFill/></button>
                                <button className="button-last edit-icons" onClick={() => {
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
        <button className="back button-first" onClick={()=>nav("../")}>Back</button>
        <button className=" button-last" onClick={()=>{
            setShowEditor(true);
            setEditorMode("add");
        }}>Add Business</button>
    </div>;
}

export default BusinessTable;