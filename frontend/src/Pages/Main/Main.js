import logo from '../../logo.svg';
import '../../App.css';


function Main() {
  return (
    <div className="App">
        <header className="App-header">
          Tutoring Database
        </header>
        <ul>
            <li><a href="/businesses">View Businesses</a> </li>

            <li> <a href="/businesses">View Parents</a> </li>

            <li> <a href="/businesses">View Students</a> </li>

            <li> <a href="/businesses">View Sessions</a></li>
        </ul>
    </div>
  );
}

export default Main;
