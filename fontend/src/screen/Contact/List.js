import React, {Component, useEffect, useRef} from 'react';
import {connect, useDispatch} from "react-redux";
import {useHistory} from 'react-router-dom';
import {CONTACT_API} from "../../redux/action/contact";
import {Column} from "primereact/column";
import {DataTable} from "primereact/datatable";
import {ROUTE} from "../../common/route";
import {Button} from "primereact/button";
import {Tooltip} from "primereact/tooltip";
import {confirmDialog} from "primereact/confirmdialog";
import {Toast} from "primereact/toast";
import {ACTION} from "../../redux/action";
import {CONSTANTS} from "../../common/constants";

const List = (props) => {
    const history = useHistory();
    const toast = useRef(null);
    const dispatch = useDispatch();
    useEffect(() => {
        props.getContacts()
    }, []);

    const actionBodyTemplate = (rowData) => {
        return (
            <React.Fragment>
                <Tooltip target=".btn-edit" content='Edit'/>
                <Button icon="pi pi-pencil" className="p-button-rounded p-button-success p-mr-2 btn-edit"
                        onClick={() => history.push(`${ROUTE.CONTACT.INDEX}/${rowData.id}`)}
                />
                <Tooltip target=".btn-remove" content='Remove'/>
                <Button icon="pi pi-trash" className="p-button-rounded p-button-warning btn-remove"
                        onClick={e => onRemove(e, rowData)}/>
            </React.Fragment>
        );
    };

    const acceptRemove = (id) => {
        // console.log(id);
        props.removeContact(id);
    };

    const onRemove = (e, item) => {
        e.stopPropagation();
        confirmDialog({
            message: `Do you want to delete contact : ${item?.name?.toLocaleUpperCase()}`,
            header: 'Delete',
            icon: 'pi pi-exclamation-triangle',
            acceptClassName: 'p-button-danger p-button-outlined',
            accept: () => acceptRemove(item?.id),
        });
    };

    useEffect(() => {
        if (props.messenger.type !== null) {
            if (props.messenger.type === ACTION.MESSAGE.OK && props.messenger.action === CONSTANTS.SCREEN.DELETE && props.messenger.id !== null) {
                toast.current.show({
                    severity: props.messenger.type === ACTION.MESSAGE.OK ? 'success' : 'error',
                    summary: props.messenger.title,
                    detail: props.messenger.message,
                    life: 3000
                });
                dispatch({type: ACTION.MESSAGE.RESET});
                dispatch({type: ACTION.CONTACT.REMOVE_ITEM, payload: props.messenger.id});
            }
        }
    }, [props.messenger]);


    return (
        <>
            <Toast ref={toast}/>
            <DataTable value={props.contacts} paginator rows={10}
                // globalFilter={globalFilter1}
                       selectionMode="single"
                       dataKey="id"
                       stateStorage="session"
                       stateKey="dt-state-demo-session"
                       emptyMessage="No customers found."
                       onRowClick={(col, row) => history.push(`${ROUTE.CONTACT.INDEX}/${col.data.id}`)}
            >

                <Column header='No.' style={{width: '5%'}}
                        body={(col, row) => row.rowIndex + 1}/>

                <Column
                    header="Name"
                    field='name'
                    sortable
                    filter
                    filterPlaceholder="Search by name"
                    bodyStyle={{fontWeight: '700', textTransform: 'uppercase'}}/>

                <Column field="positions.value"
                        header="Position"
                        filter
                        sortables
                        style={{width: '20%', textAlign: 'center'}}/>

                <Column field="phones.0"
                        header="Phone"
                        filter
                        sortable
                        style={{width: '20%', textAlign: 'center'}}/>

                <Column field="emails.0"
                        header="Email"
                        filter
                        sortable
                        style={{width: '20%', textAlign: 'center'}}/>
                <Column body={actionBodyTemplate}
                        style={{width: '10%'}}
                        header='Action'
                />

            </DataTable>
        </>
    );
};

const mapStateToProps = state => ({
    contacts: state.contact.list,
    messenger: state.messenger,
});

export default connect(mapStateToProps, {...CONTACT_API})(List);