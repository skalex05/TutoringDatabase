import React from 'react';
import ReactDOM from 'react-dom/client';
import reportWebVitals from './reportWebVitals';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import './index.css';
import Main from './Pages/Main/Main';
import Businesses from './Pages/Businesses/BusinessView.js';
import Parents from './Pages/Parents/ParentsView.js';
import Students from './Pages/Students/StudentsView.js';
import Sessions from './Pages/Sessions/SessionsView.js';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
        <Routes>
            <Route path="/" element={<Main />} />
            <Route path="/businesses" element={<Businesses />} />
            <Route path="/parents" element={<Parents />} />
            <Route path="/students" element={<Students />} />
            <Route path="/sessions" element={<Sessions />} />
        </Routes>
    </Router>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
