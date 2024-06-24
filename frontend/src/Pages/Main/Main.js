import logo from '../../logo.svg';
import '../../App.css';
import {Link} from "react-router-dom";


function Main() {
  return (
    <div className="App">
        <header className="App-header">
          Tutoring Database
        </header>
        <nav>
            <Link to="/businesses" relative="path">View Businesses</Link>
            <br/>
            <Link to="/parents" relative="path">View Parents</Link>
            <br/>
            <Link to="/students" relative="path">View Students</Link>
            <br/>
            <Link to="/sessions" relative="path">View Sessions</Link>
        </nav>
    </div>
  );
}

export default Main;
