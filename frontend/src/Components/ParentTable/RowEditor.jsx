import React from "react";
import "./roweditor.css";

export const RowEditor = (props) => {
    const [errMsg, setErrMsg] = React.useState("");

    if (props.rowValues["Name"] === undefined) {
        props.rowValues["Name"] = props.rowValues["FirstName"] !== undefined && props.rowValues["LastName"] !== undefined ? props.rowValues["FirstName"] + " " + props.rowValues["LastName"] : "";
    }
    const onSubmit = (e) => {
        e.preventDefault();

        for (const field of ["Name", "Email", "PhoneNumber"]) {
            if (props.rowValues[field] === undefined || props.rowValues[field] === "") {
                setErrMsg("Please fill out all fields");
                return;
            }
        }

        if (props.rowValues["Name"].split(" ").length !== 2) {
            setErrMsg("Please enter a valid first and last name for the parent");
            return;
        }

        let json = {
            "ParentID": props.rowValues["ParentID"],
            "FirstName": props.rowValues["Name"].split(" ")[0],
            "LastName": props.rowValues["Name"].split(" ")[1],
            "Email": props.rowValues["Email"],
            "PhoneNumber": props.rowValues["PhoneNumber"]
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
                <form onSubmit={onSubmit}>
                    <div>
                        <label htmlFor="Name">Name</label>
                        <input type="text" defaultValue={props.rowValues["Name"]} id="Name" name="Name"
                               onChange={(e) => props.rowValues["Name"] = e.target.value}/>
                    </div>
                    <div>
                        <label htmlFor="Email">Email</label>
                        <input type="text" defaultValue={props.rowValues["Email"]} id="Email" name="Email"
                               onChange={(e) => props.rowValues["Email"] = e.target.value}/>
                    </div>
                    <div>
                        <label htmlFor="PhoneNumber">Phone Number</label>
                        <input type="text" defaultValue={props.rowValues["PhoneNumber"]} id="PhoneNumber" name="PhoneNumber"
                               onChange={(e) => props.rowValues["PhoneNumber"] = e.target.value}/>
                    </div>
                    <button type="submit">Submit</button>
                </form>
                <div className="Error-Message">{errMsg}</div>
            </div>
        </div>
    );
}