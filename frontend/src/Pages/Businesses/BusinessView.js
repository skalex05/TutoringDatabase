import '../../App.css';
import {useState, useEffect, useMemo} from "react";
import Table from "../../Table/Table";

function Businesses() {
    const [businesses , setBusinesses] = useState([]);
    const [displayForm, setDisplayForm] = useState(false);

    const fetchData = async () => {
        fetch('http://localhost:5000/get_business',
            {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'GET'
            }
        ).then(response => {
            response.json().then(data => {
                console.log(data)
                setBusinesses(data["Business"]);
            });
        }).catch(err => {
            console.log(err);
        })
    }

    function NewBusiness() {
        if (!displayForm) {
            return null;
        }

        const submit = async (event) => {
            event.preventDefault();
            fetch('http://localhost:5000/new_business', {
                headers: {
                    'Content-Type': 'application/json'
                },
                method: 'POST',
                body: JSON.stringify({
                    "BusinessName": document.getElementsByName("businessName")[0].value,
                    "FirstName": document.getElementsByName("firstName")[0].value,
                    "LastName": document.getElementsByName("lastName")[0].value,
                    "Email": document.getElementsByName("email")[0].value,
                    "PhoneNumber": document.getElementsByName("phoneNumber")[0].value
                })
            }).then(response => {
                console.log(response);
            }).catch(err => {
                console.log(err);
            })
            await fetchData();
        }

        return <div>
            <h1>New Business</h1>
            <form>
                <label>Business Name</label>
                <input type="text" name="businessName"/>
                <label>Owner First Name</label>
                <input type="text" name="firstName"/>
                <label>Owner Last Name</label>
                <input type="text" name="lastName"/>
                <label>Email</label>
                <input type="text" name="email"/>
                <label>Phone Number</label>
                <input type="text" name="phoneNumber"/>
                <button onClick={submit}>Submit</button>
            </form>
        </div>
    }

    useEffect(() => {
        fetchData();
    }, []);


    const columns = useMemo(() => [
        {
            name: 'Business Name',
            selector: (row) => row.BusinessName
        },
        {
            name: 'Owner First Name',
            selector: (row) => row.FirstName
        },
        {
            name: 'Owner Last Name',
            selector: (row) => row.LastName
        },
        {
            name: 'Email',
            selector: (row) => row.Email
        },
        {
            name: 'Phone Number',
            selector: (row) => row.PhoneNumber
        }
    ], []);

    const title = "People";
    return (
        <div className="App">
            <header className="App-header">
                Businesses
            </header>

            <Table title={title} rows={businesses} columns={columns}/>
            <button onClick={fetchData}>Refresh</button>
            <button onClick={() => setDisplayForm(true)}>New Business</button>
            <NewBusiness/>
        </div>
    );
}

export default Businesses;