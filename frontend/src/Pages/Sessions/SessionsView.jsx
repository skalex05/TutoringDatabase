import '../../App.css';
import SessionTable from "../../Components/SessionTable/SessionTable";
import {useNavigate} from "react-router-dom";

function Students() {
    const nav = useNavigate();

    return (
        <div className="App">
            <header className="App-header">
                Sessions
            </header>
            <SessionTable/>
        </div>
    );
}

export default Students;