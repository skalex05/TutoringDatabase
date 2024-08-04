import React from 'react';
import ReactDOM from 'react-dom/client';
import reportWebVitals from './reportWebVitals';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import './index.css';
import Main from './Pages/Main/Main';
import Businesses from './Pages/Businesses/BusinessView.js';
import Parents from './Pages/Parents/ParentsView.jsx';
import Students from './Pages/Students/StudentsView.jsx';
import Sessions from './Pages/Sessions/SessionsView.jsx';
import EventEmail from './Pages/EventEmail/EventEmail.jsx';
import * as PropTypes from "prop-types";

const root = ReactDOM.createRoot(document.getElementById('root'));

EventEmail.propTypes = {children: PropTypes.node};
root.render(
    <div className="App">
        <link rel="preconnect" href="https://fonts.googleapis.com"/>
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin/>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet"/>
      <React.StrictMode>
        <Router>
            <Routes>
                <Route path="/" element={<Main />} />
                <Route path="/businesses" element={<Businesses />} />
                <Route path="/parents" element={<Parents />} />
                <Route path="/students" element={<Students />} />
                <Route path="/sessions" element={<Sessions />} />
                <Route path="/event-email/:eventID/:type" element={<EventEmail/>}/>
                <Route path={"*"} element={<h1>404 Not Found</h1>} />
            </Routes>
        </Router>
      </React.StrictMode>
    </div>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
