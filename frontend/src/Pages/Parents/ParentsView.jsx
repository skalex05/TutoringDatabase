import '../../App.css';
import ParentTable from "../../Components/ParentTable/ParentTable";
import {useNavigate} from "react-router-dom";

function Parents() {
    const nav = useNavigate();

    return (
        <div className="App">
            <header className="App-header">
                Parents
            </header>
            <ParentTable/>
        </div>
    );
}

export default Parents;