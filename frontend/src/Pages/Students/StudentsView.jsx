import '../../App.css';
import StudentTable from "../../Components/StudentTable/StudentTable";
import {useNavigate} from "react-router-dom";

function Students() {
    const nav = useNavigate();

    return (
        <div className="App">
            <header className="App-header">
                Students
            </header>
            <StudentTable/>
        </div>
    );
}

export default Students;