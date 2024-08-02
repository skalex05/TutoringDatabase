import {useParams, Link, useNavigate} from "react-router-dom";
import '../../App.css';
import './eventemail.css';
import {useEffect, useState} from "react";
import {format} from "date-fns";

function EventEmail() {
    const nav = useNavigate();

    const {eventID, type} = useParams();
    const [event, setEvent] = useState(null);
    const [subject, setSubject] = useState("");
    const [emailBody, setEmailBody] = useState("");
    const [recipients, setRecipients] = useState("");
    const [emailSent, setEmailSent] = useState(false);

    const updateEvent = async () => {
        let eventJson = {
            "EventID": eventID
        }
        if (type === "invite") {
            eventJson["LinkEmailSent"] = true;
        } else if (type === "debrief") {
            eventJson["DebriefEmailSent"] = true;
        }
        fetch('http://localhost:5000/update_event',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'PUT',
                body: JSON.stringify(eventJson)
        }).catch(err => {
            console.log(err)
        })
    }

    const sendEmail = () => {
        if (emailSent) {
            return;
        }
        setEmailSent(true);
        fetch('http://localhost:5000/send_email',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'POST',
                body: JSON.stringify({
                    "Subject": subject,
                    "Recipients": recipients,
                    "Body": emailBody
                })
        }).catch(err => {
            console.log(err);
        })
        updateEvent();
        nav("../");
    }

    useEffect(() => {
        fetch('http://localhost:5000/get_event',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'POST',
                body: JSON.stringify({
                    "EventID": eventID
                })
            }
        ).then(response => {
            response.json().then(data => {
                setEvent(data["Event"][0]);
                return data["Event"][0];
            }).then((tEvent) =>
                fetch("http://localhost:5000/get_event_email_info?event_id=" + eventID,
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        method: 'GET'
                    }
                ).then(response => {
                    response.json().then(data => {
                        setSubject(tEvent["EventName"])
                        setRecipients(`${data["ParentEmail"]}, ${data["StudentEmail"]}, ${data["BusinessEmail"]}`)
                        if (type === "invite"){
                            setEmailBody(`Hi ${data["ParentName"]},\n\nHere is the Google Meet link for our ${data["Subject"].toLowerCase()} session on ${format(tEvent["StartTime"], "cccc do LLLL")} at ${format(tEvent["StartTime"], "HH:mm")}\n\n ${tEvent["GoogleMeetLink"] ? tEvent["GoogleMeetLink"] : "<LINK UNAVAILABLE>"}\n\nMany Thanks,\n${data["Sender"]}`)
                        } else if (type === "reminder") {
                            setEmailBody(`Hi ${data["ParentName"]},\n\nThis is a reminder for our tutoring session on ${format(tEvent["StartTime"], "cccc do LLLL")} at  ${format(tEvent["StartTime"], "HH:mm")}. Please let me know if you have any issues joining the call\n\nMany Thanks,\n${data["Sender"]}`)
                        } else if (type === "debrief") {
                            setEmailBody(`Hi ${data["ParentName"]},\n\nI just wanted to check in and see how you felt the tutoring session went. Please let me know if you have any feedback or concerns\n\nMany Thanks,\n${data["Sender"]}`)
                        }
                    })
                }).catch(err => {
                    console.log(err);
                })
            );
        }).catch(err => {
            nav("../");
        })
    }, [nav, eventID]);

    return (
        <div className="App">
            <header className="App-header">Email Sender</header>
            <Link to="../" reference="path">Back</Link>
            {event && <h3>Email for {event["EventName"]} on {format(event["StartTime"], "cccc do LLLL")} at  {format(event["StartTime"], "HH:mm")}</h3>}
            <label className="Subject">Subject: </label><input className="EmailSubject" type="text" defaultValue={subject} onChange={e => setSubject(e.target.value)}/><br/>
            <label className="RecipientLabel">Recipients: </label><input className="EmailRecipients" type="text" defaultValue={recipients} onChange={(e) => setRecipients(e.target.value)}/><br/>
            <textarea className="EmailBody" defaultValue={emailBody} placeholder="Type your email here" onChange={(e) => setEmailBody(e.target.value)}/><br/>
            <button onClick={sendEmail}>Send Email</button>
        </div>
    );
}

export default EventEmail;