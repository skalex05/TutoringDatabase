import DataTable from "react-data-table-component";

function Table (props) {

    return <div>
        <DataTable
            columns={props.columns}
            data={props.rows}
            fixedHeader={true}
            title={props.title}
            selectableRows={true}
            selectableRowsHighlight={true}
        />
    </div>;
}

export default Table;