import '../../App.css';
import BusinessTable from "../../Components/BusinessTable/BusinessTable";
import {Link} from "react-router-dom";

function Businesses() {
    const title = "People";
    return (
        <div className="App">
            <header className="App-header">
                Businesses
            </header>
            <Link to="../" relative="path">Back</Link>
            <BusinessTable/>
        </div>
    );
}

export default Businesses;