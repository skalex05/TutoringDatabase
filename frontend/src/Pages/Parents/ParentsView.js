import '../../App.css';
import ParentTable from "../../Components/ParentTable/ParentTable";
import {Link} from "react-router-dom";

function Parents() {
    return (
        <div className="App">
            <header className="App-header">
                Parents
            </header>
            <Link to="../" relative="path">Back</Link>
            <ParentTable/>
        </div>
    );
}

export default Parents;