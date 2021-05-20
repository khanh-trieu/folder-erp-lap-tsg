import React, {Component, useEffect, useState} from 'react';
import {Dropdown} from "primereact/dropdown";
import {connect} from "react-redux";
import {USER_API} from "../../redux/action/user";

const OwnerInputBox = (props) => {
    const [owner, setOwner] = useState(null);

    useEffect(() => {
        props.getUsers();
    }, []);

    const onChangeOwner = (e) => {
        setOwner(e.value);
        props.setValue(e.value);
    };

    const ownerInputTemplate = (option) => {
        return (
            <div className='p-d-flex p-ai-center'>
                <i className='pi pi-user p-mr-3'/>
                <div className='p-d-flex p-flex-column'>
                    <>{option.full_name}</>
                    <div>{option.role.value}</div>
                </div>
            </div>
        );
    };

    return (
        <Dropdown value={owner === null ? props.value : owner} options={props.users} optionLabel='full_name' optionValue='id'
                  itemTemplate={ownerInputTemplate} onChange={onChangeOwner}/>
    )
};

const mapStateToProps = (state) => ({
    users: state.user.users,
});

export default connect(mapStateToProps, {
    getUsers: USER_API.getListOwner,
})(OwnerInputBox);