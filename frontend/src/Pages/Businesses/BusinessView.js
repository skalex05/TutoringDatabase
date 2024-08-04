import '../../App.css';
import BusinessTable from "../../Components/BusinessTable/BusinessTable";
import {useNavigate} from "react-router-dom";

function Businesses() {
    return (
        <div className="App">
            <header className="App-header">
                Businesses
            </header>
            <BusinessTable/>
        </div>
    );
}

export default Businesses;