import React, {useEffect, useState} from 'react';
import {Column} from "primereact/column";
import {DataTable} from "primereact/datatable";
import {connect} from "react-redux";
import {Badge} from "primereact/badge";
import {Dropdown} from "primereact/dropdown";
import {FaUser, FaUsers} from "react-icons/fa";
import {CONSTANTS} from "../../common/constants";
import {useHistory} from 'react-router-dom';
import {ROUTE} from "../../common/route";
import {ACCOUNT_API} from "../../redux/action/account";
import {InputText} from "primereact/inputtext";

const List = (props) => {
    const history = useHistory();
    const [nameSearch, setNameSearch] = useState([]);
    const [accounts, setAccounts] = useState({
        list: [],
        total: 0,
    });

    const [lazy, setLazy] = useState({
        first: 0,
        rows: 10,
        page: 0,
        totalRecords: props?.totalRecords ?? 0,
    });

    const accountNameTemplate = (rowData) => {
        const icon = rowData.company.key === CONSTANTS.COMPANY_TYPE.ENTERPRISE ? <FaUsers/> : <FaUser/>;
        return <div className='p-d-inline-flex'>
            {icon}
            <span className='p-ml-2'>{rowData.name}</span>
        </div>;
    };

    const companyTypeTemplate = (rowData) => {
        return <div>
            <Badge value={rowData.company.value}
                   severity={rowData.company.key === CONSTANTS.COMPANY_TYPE.ENTERPRISE ? 'info' : 'success'}/>
        </div>
    };

    const onSearchByName = e => {
        setNameSearch(e.target.value);
        if (e.target.value) {
            setTimeout(() => {
                    props.search(e.target.value);
                }
                , 500);
        } else {
            props.resetSearch();
        }
    };

    const companyTypeData = [
        {'label': 'Doanh nghiệp', 'id': 'enterprise'},
        {'label': 'Cá nhân', 'id': 'personal'},
    ];

    const nameFilter = <InputText placeholder='Search by name' style={{width: '100%'}} value={nameSearch}
                                  onChange={onSearchByName}/>;

    const companyFilter = <Dropdown
        options={companyTypeData}
        placeholder="Select an account type"
        optionLabel='label'
        className="p-column-filter"/>;

    const onPageChange = (event) => {
        setLazy({...lazy, ...event});
    };

    useEffect(() => {
        setAccounts({
            list: props.accounts.list,
            total: props.accounts.totalRecords,
        })
    }, [props.accounts.list]);

    useEffect(() => {
        if (props.accounts.search) {
            setAccounts({
                list: props.accounts.search,
                total: props.accounts.searchRecords,
            });
        } else {
            setAccounts({
                list: props.accounts.list,
                total: props.accounts.totalRecords,
            });
        }
    }, [props.accounts.search]);


    useEffect(() => {
            props.getAccounts(lazy.page + 1);
        },
        [lazy]);

    const onSelectRow = ({data}) => {
        history.push(`${ROUTE.ACCOUNT.INDEX}/${data.id}`);
    };

    return (
        <DataTable
            value={accounts.list}
            lazy
            paginator
            rows={10}
            totalRecords={accounts.total}
            onPage={onPageChange}
            rowsPerPageOptions={[10, 25, 50]}
            first={lazy.first}
            selectionMode="single"
            dataKey="id"
            emptyMessage="No customers found."
            onRowClick={onSelectRow}
        >

            <Column header='No.' style={{width: '5%'}}
                    body={(col, row) => row.rowIndex + 1}/>

            <Column
                header="Name"
                filter
                filterElement={nameFilter}
                body={accountNameTemplate}
                bodyStyle={{fontWeight: '700', textTransform: 'uppercase'}}/>

            <Column field="company.value"
                    body={companyTypeTemplate}
                    header="Type"
                    filter
                    filterElement={companyFilter}
                    style={{width: '20%', textAlign: 'center'}}/>

            <Column header='Province'
                    field='province.value'
                    style={{width: '20%', textAlign: 'center'}}
            />

            <Column header="Tax" field="tax_code" style={{width: "10%", textAlign: "center"}}/>
        </DataTable>
    );
};

const mapStateToProps = state => ({
    accounts: state.account,
});

export default connect(mapStateToProps, {
    getAccounts: ACCOUNT_API.getAccounts,
    search: ACCOUNT_API.searchAccountName,
    resetSearch: ACCOUNT_API.resetSearch,
})(List);