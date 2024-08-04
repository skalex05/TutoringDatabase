import "react-big-calendar/lib/css/react-big-calendar.css"
import "../../App.css";
import {useNavigate} from "react-router-dom";
import {Calendar, Views, momentLocalizer} from 'react-big-calendar';
import moment from "moment";
import {useCallback, useEffect, useState} from "react";
import EventView from "../../Components/EventView/EventView";
import {addWeeks, subWeeks, startOfWeek, format} from "date-fns";

moment.locale('en', {
    week: {
        dow: 1,
        doy: 1
    }
});

const localizer = momentLocalizer(moment);

function Main() {
    const [calendarEvents, setCalendarEvents] = useState([]);
    const [events, setEvents] = useState([]);
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [showEventView, setShowEventView] = useState(false);

    let week = subWeeks(startOfWeek(Date.now()), 1);
    const [periodStart, setPeriodStart] = useState(week);
    week = addWeeks(week, 5)
    const [periodEnd, setPeriodEnd] = useState(week);
    const nav = useNavigate();

    const getEventJson = (eventId) => {
        for (let e of events) {
            if (e["EventID"] === eventId) {
                return e;
            }
        }
    }

    const handleSelect = useCallback(
        (event) => {
            setSelectedEvent(event);
            setShowEventView(true);
        }, []
    )

    const onNavigate = (date, view, action) => {
        if (action === "PREV") {
            date = startOfWeek(date)
            setPeriodStart(subWeeks(date, 1));
            setPeriodEnd(addWeeks(date, 4));
        } else if (action === "NEXT") {
            date = startOfWeek(date)
            setPeriodStart(subWeeks(date, 1));
            setPeriodEnd(addWeeks(date, 4));
        }
    }
    const eventStyleGetter = (event, start, end, isSelected) => {
        let eventJSON = getEventJson(event.id);
        console.log(eventJSON);
        let style = {
            borderRadius: '5px',
            justifyContent: 'center',
            opacity: 1,
            color: 'black',
            border: '0px',
            display: 'flex'
        };
        if (eventJSON["Paid"] && eventJSON["DebriefEmailSent"]){
            style["backgroundColor"] = "#388538";
        } else if (Date.parse(eventJSON["EndTime"]) < Date.now()) {
            style["backgroundColor"] = "#bb9746";
        } else {
            style["backgroundColor"] = "#ab2a2a";
        }
        console.log(style);
        return {"style": style};
    }

    const fetchData = async () => {
        fetch('http://localhost:5000/get_event_period',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'POST',
                body: JSON.stringify({
                    "Start": format(periodStart, "yyyy-MM-dd"),
                    "End": format(periodEnd, "yyyy-MM-dd")
                })
            }
        ).then(response => {
            response.json().then(data => {
                const eventData = data["Event"];
                let calEvents = [];
                for (let event of eventData) {
                    let obj = {
                        id: event["EventID"],
                        title: event["EventName"],
                        start: new Date(Date.parse(event["StartTime"])),
                        end: new Date(Date.parse(event["EndTime"])),
                        desc: event["Description"]
                    }
                    calEvents.push(obj);
                }
                setEvents(eventData);
                setCalendarEvents(calEvents);
            });
        }).catch(err => {
            console.log(err)
        })
    }

    useEffect(() => {
        fetchData();
    }, []);

    let eventJSON = {};
    if (selectedEvent) {
        eventJSON = getEventJson(selectedEvent.id)
    }

    return (
    <div className="App">
        {showEventView && <EventView
            event={eventJSON}
            showEvent={setShowEventView}
            fetchData={fetchData}
        />}
        <header className="App-header">
          Tutoring Management System
        </header>
            <button className="button-first" onClick={() => nav("/businesses")}>Businesses</button>
            <button onClick={() => nav("/parents")}>Parents</button>
            <button onClick={() => nav("/students")}>Students</button>
            <button className="button-last" onClick={() => nav("/sessions")}>Sessions</button>
        <div className="calendar-wrapper">
            <Calendar
                localizer={localizer}
                events={calendarEvents}
                onSelectEvent={handleSelect}
                views={['month','week', 'day', ]}
                step="60"
                timeslots="1"
                onNavigate={onNavigate}
                defaultView={Views.WEEK}
                eventPropGetter={eventStyleGetter}
                style={{height: "80vh"}}
            />
        </div>
    </div>
  );
}

export default Main;
