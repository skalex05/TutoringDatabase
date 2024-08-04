import React from "react";
import "../../App.css";

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
                <h2 className="editHeader">{props.editorMode.charAt(0).toUpperCase()+props.editorMode.slice(1)} Business</h2>
                <form onSubmit={onSubmit}>
                    <table style={{maxWidth:"100%", margin:"auto 10px"}}>
                        <tr>
                            <td><label htmlFor="BusinessName">Business Name</label></td>
                            <td><input type="text" defaultValue={props.rowValues["BusinessName"]} id="Business Name" name="Business Name"
                                       onChange={(e) => props.rowValues["BusinessName"] = e.target.value}/></td>
                        </tr>
                        <tr>
                            <td><label htmlFor="OwnerName">Owner Name</label></td>
                            <td><input type="text" defaultValue={props.rowValues["OwnerName"]} id="Owner Name" name="Owner Name"
                                       onChange={(e) => props.rowValues["OwnerName"] = e.target.value}/></td>
                        </tr>
                        <tr>
                            <td><label htmlFor="Email">Email</label></td>
                            <td><input type="text" defaultValue={props.rowValues["Email"]} id="Email" name="Email"
                                       onChange={(e) => props.rowValues["Email"] = e.target.value}/></td>
                        </tr>
                        <tr>
                            <td><label htmlFor="PhoneNumber">Phone Number</label></td>
                            <td><input maxLength={11} type="text" defaultValue={props.rowValues["PhoneNumber"]} id="PhoneNumber" name="PhoneNumber"
                                       onChange={(e) => props.rowValues["PhoneNumber"] = e.target.value}/></td>
                        </tr>
                    </table>
                    <div style={{textAlign: "center"}}>
                        <button className="button-first button-last" type="submit">Submit</button>
                    </div>
                </form>
                <div className="Error-Message">{errMsg}</div>
            </div>
        </div>
    );
}