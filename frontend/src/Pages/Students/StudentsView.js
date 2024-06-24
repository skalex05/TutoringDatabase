import '../../App.css';
import StudentTable from "../../Components/StudentTable/StudentTable";
import {Link} from "react-router-dom";

function Students() {
    return (
        <div className="App">
            <header className="App-header">
                Students
            </header>
            <Link to="../" relative="path">Back</Link>
            <StudentTable/>
        </div>
    );
}

export default Students;