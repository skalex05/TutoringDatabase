import '../../App.css';
import SessionTable from "../../Components/SessionTable/SessionTable";
import {Link} from "react-router-dom";

function Students() {
    return (
        <div className="App">
            <header className="App-header">
                Sessions
            </header>
            <Link to="../" relative="path">Back</Link>
            <SessionTable/>
        </div>
    );
}

export default Students;