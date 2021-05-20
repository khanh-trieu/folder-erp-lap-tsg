import React, {useEffect, useState} from 'react';
import {DataTable} from "primereact/datatable";
import {Column} from "primereact/column";
import {AutoComplete} from "primereact/autocomplete";
import styled from 'styled-components';
import {connect} from "react-redux";
import {CONTACT_API} from "../../redux/action/contact";
import axiosInstance from "../../utils/axiosInstance";
import {API} from "../../api";
import {Tooltip} from "primereact/tooltip";
import {Button} from "primereact/button";
import {ROUTE} from "../../common/route";
import {confirmPopup} from "primereact/confirmpopup";

const ViewContactView = styled.div`
    .panel {
        display: flex;
        align-items: center;
        padding: 1rem;
        width: 100%;
    }
    
    .contact-name {
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .extra {
        margin: 0 0 1rem 0;
        font-size: 0.9rem;
        color: var(--bluegray-200);
    }
`;

const ViewContact = (props) => {

    const itemTemplate = (item) => {
        return (
            <div className='p-d-flex p-ai-center'>
                <div className='p-mr-2'><i className='pi pi-user'/></div>
                <div className='p-d-flex p-flex-column p-jc-center'>
                    <div className='contact-name p-text-uppercase'>{item.name}</div>
                    <p className='extra'>
                        <span>{item?.phones.reduce((r, i) => <>{r}/{i}</>)}</span>-<span>{item?.positions.value ?? ''}</span>

                    </p>
                </div>
            </div>
        );
    };

    const removeContact = (e, data) => {
        confirmPopup({
            target: e.currentTarget,
            message: `Are you sure you remove ${data.name}?`,
            icon: 'pi pi-exclamation-triangle',
            acceptClassName: 'p-button-danger p-button-outlined',
            accept: () => props.removeContacts(data.id),
        });
    };

    const actionRemoveTemplate = (rowData) => {
        return (
            <React.Fragment>
                <Tooltip target=".btn-remove" content='Remove'/>
                <Button icon="pi pi-trash" className="p-button-rounded p-button-warning btn-remove"
                        onClick={e => removeContact(e, rowData)}
                        type='button'
                />
            </React.Fragment>
        );
    };

    const [searchItem, setSearchItem] = useState([]);

    const searchContact = e => {
        let query = e.query;
        props.search(query);
    };

    return (
        <ViewContactView>
            <div className='p-text-secondary'>Find & Add Contact</div>
            <div className="p-inputgroup p-mb-5">
                <AutoComplete itemTemplate={itemTemplate} suggestions={props.contactSearch}
                              completeMethod={searchContact}
                              value={typeof (searchItem) === "string" ? searchItem : searchItem.name}
                              onChange={(e) => setSearchItem(e.value)}
                              onSelect={(e) => {
                                  setSearchItem('');
                                  props.addContacts(e.value);
                              }}
                              delay={500}
                />
                <span className="p-inputgroup-addon"><i className="pi pi-search"/></span>
            </div>
            {props.contacts !== null && props.contacts.length > 0 ?
                <DataTable value={props.contacts} header='List of Contacts'>
                    <Column header={'Name'} field='name'/>
                    <Column header={'Phones'} body={(col, row) => col?.phones?.reduce((r, i) => `${r}/${i}`)}/>
                    <Column body={actionRemoveTemplate}
                            style={{width: '10%', textAlign: 'center'}}
                            header='Remove'
                    />
                </DataTable> : null}

        </ViewContactView>
    );
};

const mapStateToProps = state => ({
    contactSearch: state.contact.search,
});

export default connect(mapStateToProps, {
    search: CONTACT_API.searchContactName,
})(ViewContact);