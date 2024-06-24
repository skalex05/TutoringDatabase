import React from "react";
import "./roweditor.css";

export const RowEditor = (props) => {
    const [errMsg, setErrMsg] = React.useState("");

    if (props.rowValues["Name"] === undefined) {
        props.rowValues["Name"] = props.rowValues["FirstName"] !== undefined && props.rowValues["LastName"] !== undefined ? props.rowValues["FirstName"] + " " + props.rowValues["LastName"] : "";
    }
    if (props.rowValues["ParentID"] === undefined && props.parents !== undefined && props.parents.length > 0) {
        props.rowValues["ParentID"] = props.parents[0]["ParentID"];
    }
    if (props.rowValues["BusinessID"] === undefined && props.businesses !== undefined && props.businesses.length > 0) {
        props.rowValues["BusinessID"] = props.businesses[0]["BusinessID"];
    }

    const onSubmit = (e) => {
        e.preventDefault();

        for (const field of ["Name", "YearGrade","Email", "PhoneNumber","BusinessID","ParentID"]) {
            if (props.rowValues[field] === undefined || props.rowValues[field] === "") {
                setErrMsg("Please fill out all fields");
                return;
            }
        }

        if (props.rowValues["Name"].split(" ").length !== 2) {
            setErrMsg("Please enter a valid first and last name for the student");
            return;
        }

        let json = {
            "StudentID": props.rowValues["StudentID"],
            "FirstName": props.rowValues["Name"].split(" ")[0],
            "LastName": props.rowValues["Name"].split(" ")[1],
            "YearGrade": props.rowValues["YearGrade"],
            "Email": props.rowValues["Email"],
            "PhoneNumber": props.rowValues["PhoneNumber"],
            "BusinessID": props.rowValues["BusinessID"],
            "ParentID": props.rowValues["ParentID"],
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
                        <label htmlFor="Name">Student Name</label>
                        <input type="text" defaultValue={props.rowValues["Name"]} id="Name" name="Name"
                               onChange={(e) => props.rowValues["Name"] = e.target.value}/>
                    </div>
                    <div>
                        <label htmlFor="YearGrade">Year Group</label>
                        <input type="text" defaultValue={props.rowValues["YearGrade"]} id="YearGrade" name="YearGrade"
                               onChange={(e) => props.rowValues["YearGrade"] = e.target.value}/>
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
                    <div>
                        <label htmlFor="ParentID">Parent</label>
                        <select defaultValue={props.rowValues["ParentID"]} id="ParentID" name="Parent"
                               onChange={(e) => props.rowValues["ParentID"] = e.target.value}>
                                {props.parents.map(parent => {
                                    return <option value={parent["ParentID"]}>{parent["FirstName"] + " " + parent["LastName"]}</option>
                                })}
                        </select>
                    </div>
                    <div>
                        <label htmlFor="BusinessID">Business</label>
                        <select defaultValue={props.rowValues["BusinessID"]} id="BusinessID" name="Business"
                                onChange={(e) => props.rowValues["BusinessID"] = e.target.value}>
                            {props.businesses.map(business => {
                                return <option value={business["BusinessID"]}>{business["BusinessName"]}</option>
                            })}
                        </select>
                    </div>
                    <button type="submit">Submit</button>
                </form>
                <div className="Error-Message">{errMsg}</div>
            </div>
        </div>
    );
}