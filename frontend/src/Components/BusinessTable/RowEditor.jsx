import React from "react";
import "./roweditor.css";

export const RowEditor = (props) => {
    const [errMsg, setErrMsg] = React.useState("");

    if (props.rowValues["OwnerName"] === undefined) {
        props.rowValues["OwnerName"] = props.rowValues["FirstName"] !== undefined && props.rowValues["LastName"] !== undefined ? props.rowValues["FirstName"] + " " + props.rowValues["LastName"] : "";
    }
    const onSubmit = (e) => {
        e.preventDefault();

        for (const field of ["BusinessName", "OwnerName", "Email", "PhoneNumber"]) {
            if (props.rowValues[field] === undefined || props.rowValues[field] === "") {
                setErrMsg("Please fill out all fields");
                return;
            }
        }

        if (props.rowValues["OwnerName"].split(" ").length !== 2) {
            setErrMsg("Please enter a valid first and last name for the owner's name");
            return;
        }

        let json = {
            "BusinessID": props.rowValues["BusinessID"],
            "BusinessName": props.rowValues["BusinessName"],
            "FirstName": props.rowValues["OwnerName"].split(" ")[0],
            "LastName": props.rowValues["OwnerName"].split(" ")[1],
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
                        <label htmlFor="BusinessName">Business Name</label>
                        <input type="text" defaultValue={props.rowValues["BusinessName"]} id="Business Name" name="Business Name"
                               onChange={(e) => props.rowValues["BusinessName"] = e.target.value}/>
                    </div>
                    <div>
                        <label htmlFor="OwnerName">Owner Name</label>
                        <input type="text" defaultValue={props.rowValues["OwnerName"]} id="Owner Name" name="Owner Name"
                               onChange={(e) => props.rowValues["OwnerName"] = e.target.value}/>
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