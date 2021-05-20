import React, {useEffect, useRef, useState} from 'react';
import {useHistory, useParams} from 'react-router-dom';
import {InputText} from "primereact/inputtext";
import {FaAddressBook, FaUserCircle} from "react-icons/fa";
import {Chips} from "primereact/chips";
import {AiFillFacebook, AiFillLinkedin, AiFillPhone, AiFillSkype} from "react-icons/ai";
import {MdEmail} from "react-icons/md";
import {Button} from "primereact/button";
import {connect, useDispatch} from "react-redux";
import {ImOffice} from "react-icons/im";
import {Divider} from "primereact/divider";
import {Ripple} from "primereact/ripple";
import {Panel} from "primereact/panel";
import styled from "styled-components";
import {RiShieldUserFill} from "react-icons/ri";
import {Dropdown} from "primereact/dropdown";
import {CONTACT_API} from "../../redux/action/contact";
import swal from "sweetalert";
import {ACTION} from "../../redux/action";
import {ROUTE} from "../../common/route";
import {Toast} from "primereact/toast";
import {CONSTANTS} from "../../common/constants";
import {confirmDialog} from "primereact/confirmdialog";
import {Timeline} from "primereact/timeline";
import {OverlayPanel} from "primereact/overlaypanel";
import {DataTable} from "primereact/datatable";
import {Column} from "primereact/column";
import {Dialog} from "primereact/dialog";
import {Calendar} from "primereact/calendar";
import {AutoComplete} from "primereact/autocomplete";
import {DataScroller} from "primereact/datascroller";

const CreateView = styled.div`
    .p-panel-content {
        padding: 0 !important;
        border: none !important;
    }
    
    .sticky {
        position: sticky;
        z-index: 999;
        top: 70px;
    }
    
    .sticky-wrapper {
        position: relative;
    }
    
    .custom-marker {
        display: flex;
        width: 1.2rem;
        height: 1.2rem;
        align-items: center;
        justify-content: center;
        color: #ffffff;
        border-radius: 50%;
        border: 2px solid var(--blue-500);
        z-index: 1;
        cursor: pointer;
    }
    
    .custom-marker-button {
        display: flex;
        width: 1.2rem;
        height: 1.2rem;
        align-items: center;
        justify-content: center;
        background-color: var(--blue-500);
        color: #ffffff;
        padding: 7px;
        border-radius: 50%;
        border: 2px solid var(--blue-500);
        z-index: 1;
        cursor: pointer;
    }
`;

const Create = (props) => {

    // template html for extra form
    const extraTemplate = (options) => {
        const toggleIcon = options.collapsed ? 'pi pi-chevron-down' : 'pi pi-chevron-up';
        const titleClassName = `${options.titleClassName} p-pl-1`;
        return (
            <Divider align='right'>
                <button className={options.togglerClassName} onClick={options.onTogglerClick}>
                    <span className={toggleIcon}/>
                    <Ripple/>
                </button>
                <span className={titleClassName}>
                    {options.props.header}
                </span>
            </Divider>
        )
    };


    const timelineMarker = (item) => {
        return (
            <span className="custom-marker" onClick={(e) => onShowAccount(e, item.year)}/>
        );
    };
    const timelineContent = (item) => {
        return <span>{item?.year ?? ''}</span>;
    };

    const footerDialog = () => {
        return (
            <div>
                <Button label="No" icon="pi pi-times" className="p-button-text"/>
                <Button label="Yes" icon="pi pi-check" autoFocus/>
            </div>
        );
    };

    /**
     * defined variable area
     */
    const ref = useRef(null);
    const toast = useRef(null);
    const history = useHistory();
    const {id} = useParams();
    const screen = id === undefined ? CONSTANTS.SCREEN.CREATE : CONSTANTS.SCREEN.EDIT;
    const dispatch = useDispatch();
    const [sticky, setSticky] = useState(false);
    const [address, setAddress] = useState({});
    const [socials, setSocials] = useState({});
    const [values, setValues] = useState({
        name: {
            value: '',
            isValid: true,
            errorMessage: '',
        },
        position: {
            value: '',
            isValid: true,
            errorMessage: '',
        },
        phones: {
            value: [],
            isValid: true,
            errorMessage: ''
        },
        emails: {
            value: [],
            isValid: true,
            errorMessage: '',
        },
        socials: [],
        address: [],
        formValid: false,
    });
    const op = useRef(null);
    const [accounts, setAccounts] = useState([]);
    const [showDialog, setShowDialog] = useState(false);

    const event = [
        {status: ['Account 1', 'Account 2'], year: 2020},
        {status: ['Account 3', 'Account 4'], year: 2021},
    ];


    const onChangeValue = (e) => {
        setValues({
            ...values,
            [e.target.name]: {
                ...values[e.target.name],
                value: e.target.value,
            }
        });
    };

    const onChangeAddress = (e) => {
        setAddress({
            ...address,
            [e.target.name]: e.target.value,
        })
    };

    const onChangeSocial = e => {
        setSocials({
            ...socials,
            [e.target.name]: e.target.value
        })
    };

    const handleScroll = () => {
        if (ref.current) {
            setSticky(ref.current.getBoundingClientRect().top <= 0);
        }
    };

    const validateInput = (name, value) => {
        switch (name) {
            case 'name':
                if (value === null || value.length === 0) {
                    return {isValid: false, errorMessage: 'Name is not empty.'};
                }
                break;
            case 'position':
                if (value === null || value.length === 0) {
                    return {isValid: false, errorMessage: 'Position is not empty.'};
                }
                break;
            case 'phones':
                if (value === null || value.length === 0) {
                    return {isValid: false, errorMessage: 'Phones is not empty.'};
                }
                break;
            case 'emails':
                if (value === null || value.length === 0) {
                    return {isValid: false, errorMessage: 'Emails is not empty.'};
                }
                break;
            default:
                return {isValid: true, errorMessage: ''};
        }
        return {isValid: true, errorMessage: ''};
    };

    const handleValidateInput = (name, value) => {
        const validation = validateInput(name, value);
        const {isValid, errorMessage} = validation;
        const newState = {...values[name]};
        newState.isValid = isValid;
        newState.errorMessage = errorMessage;

        setValues(prev => ({
            ...prev,
            [name]: newState
        }));

        return isValid;
    };

    const onSubmit = (e) => {
        e.preventDefault();
        const nameValid = handleValidateInput('name', values.name.value);
        const positionValid = handleValidateInput('position', values.position.value);
        const emailsValid = handleValidateInput('emails', values.emails.value);
        const phonesValid = handleValidateInput('phones', values.phones.value);

        const isFormValid = nameValid && positionValid && emailsValid && phonesValid;
        if (isFormValid) {
            const addressList = Object.keys(address).map(key => {
                return {
                    key: key, value: address[key]
                }
            });

            const socialList = Object.keys(socials).map(key => {
                return {
                    key: key, value: socials[key]
                }
            });

            setValues(prev => ({
                ...prev,
                socials: socialList,
                address: addressList,
                formValid: true
            }));
        }
    };

    const acceptRemove = () => {
        props.removeContact(id);
    };

    const onRemove = () => {
        confirmDialog({
            message: `Do you want to delete contact : ${props.contact?.name?.toLocaleUpperCase()}`,
            header: 'Delete',
            icon: 'pi pi-exclamation-triangle',
            acceptClassName: 'p-button-danger p-button-outlined',
            accept: acceptRemove,
        });
    };

    const onShowAccount = (e, year) => {
        op.current.toggle(e);
        const accounts = event.find(i => i.year === year);
        setAccounts(accounts.status);
    };

    useEffect(() => {
        window.addEventListener('scroll', handleScroll);

        return () => {
            window.removeEventListener('scroll', () => handleScroll);
        };
    }, []);

    // send payload
    useEffect(() => {
        if (values.formValid) {
            const payload = {
                name: values.name.value,
                address: values.address,
                socials: values.socials,
                positions: values.position.value,
                phones: values.phones.value,
                emails: values.emails.value,
            };
            if (screen === CONSTANTS.SCREEN.CREATE)
                props.createContact(payload);
            if (screen === CONSTANTS.SCREEN.EDIT)
                props.updateContact(id, payload);

            setValues({...values, formValid: false});
        }
    }, [values.formValid]);

    // show messenger
    useEffect(() => {
        if (props.messenger.type !== null) {
            switch (props.messenger.action) {
                case CONSTANTS.SCREEN.CREATE:
                case CONSTANTS.SCREEN.DELETE:
                    swal({
                        title: props.messenger.title,
                        text: props.messenger.message,
                        icon: props.messenger.type === ACTION.MESSAGE.OK ? 'success' : 'error',
                        button: "OK",
                    }).then(value => {
                        if (props.messenger.type === ACTION.MESSAGE.OK) {
                            history.push(ROUTE.CONTACT.INDEX);
                        }
                    });
                    break;
                case CONSTANTS.SCREEN.EDIT:
                    toast.current.show({
                        severity: props.messenger.type === ACTION.MESSAGE.OK ? 'success' : 'error',
                        summary: props.messenger.title,
                        detail: props.messenger.message,
                        life: 3000
                    });
                    break;
            }
            dispatch({type: ACTION.MESSAGE.RESET});
        }
    }, [props.messenger]);

    // get contact for edit or reset contact item for create screen
    useEffect(() => {
        if (screen === CONSTANTS.SCREEN.EDIT) {
            props.getContact(id);
        }
        if (screen === CONSTANTS.SCREEN.CREATE) {
            dispatch({type: ACTION.CONTACT.RESET_ITEM});
        }
    }, []);

    // set state for initial data edit screen
    useEffect(() => {
        if (props.contact !== null) {
            setValues({
                ...values,
                name: {
                    ...values.name,
                    value: props.contact?.name ?? '',
                },
                position: {
                    ...values.position,
                    value: props.contact?.positions?.key ?? '',
                },
                phones: {
                    ...values.phones,
                    value: props.contact?.phones ?? []
                },
                emails: {
                    ...values.emails,
                    value: props.contact?.emails ?? []
                },
            });
            setAddress({
                home: props.contact?.address?.find(i => i.key.key === 'home')?.value ?? '',
                company: props.contact?.address?.find(i => i.key.key === 'company')?.value ?? '',
            });
            setSocials({
                facebook: props.contact?.socials?.find(i => i.key === 'facebook')?.value ?? '',
                skype: props.contact?.socials?.find(i => i.key === 'skype')?.value ?? '',
                linkedin: props.contact?.socials?.find(i => i.key === 'linkedin')?.value ?? '',
                zalo: props.contact?.socials?.find(i => i.key === 'zalo')?.value ?? '',
            })
        }

    }, [props.contact]);

    return (
        <CreateView>
            {screen === CONSTANTS.SCREEN.EDIT ? <Toast ref={toast}/> : null}
            <OverlayPanel ref={op} breakpoints={{'960px': '75vw', '640px': '100vw'}} style={{width: '450px'}}
                          onHide={() => setAccounts([])}
                          id='overlay_panel' showCloseIcon>
                <DataTable value={accounts}>
                    <Column header="No." body={(col, row) => row.rowIndex + 1} style={{width: '5%'}}/>
                    <Column header='Account' body={(col, row) => col} style={{textAlign: 'center'}}/>
                </DataTable>
            </OverlayPanel>
            <Dialog header="Header" visible={showDialog} style={{width: '50vw'}} footer={footerDialog}
                    onHide={() => setShowDialog(!showDialog)}>
                <div className='p-formgrid p-grid p-fluid'>
                    <div className='p-field p-col-12'>
                        <label>Year</label>
                        <Calendar view="month" dateFormat="mm/yy" yearNavigator yearRange="2010:2030"/>
                    </div>
                    <div className='p-field p-col-12'>
                        <label>Accounts</label>
                        <AutoComplete/>
                        <DataScroller value={[]} rows={5} inline scrollHeight="200px" header="Account List"/>
                    </div>
                </div>
            </Dialog>
            <form onSubmit={onSubmit}>
                <div className="p-grid p-fluid" ref={ref}>
                    <div className='p-col-6'>
                        <div className='p-fluid p-grid p-formgrid'>
                            <div className='p-field p-col-12'>
                                <label htmlFor='name' className='p-overlay-badge'>
                                    Full Name
                                    <span className='required'>*</span>
                                </label>
                                <div className='p-inputgroup'>
                                    <span className='p-inputgroup-addon'>
                                       <FaUserCircle/>
                                    </span>
                                    <InputText id='name'
                                               required
                                               placeholder='Please enter your contact name'
                                               name='name'
                                               onChange={onChangeValue}
                                               value={values.name.value}
                                    />
                                </div>
                                {values.name.isValid ? null : <small id="name-help"
                                                                     className="p-error p-d-block">{values.name.errorMessage}</small>}
                            </div>
                            <div className='p-field p-col-12'>
                                <label htmlFor='positions'>Position<span className='required'>*</span></label>
                                <div className='p-inputgroup'>
                                    <span className='p-inputgroup-addon'>
                                       <RiShieldUserFill/>
                                    </span>
                                    <Dropdown options={props.initial.contact.positions}
                                              placeholder='Please select a position'
                                              optionLabel='value'
                                              id='positions'
                                              optionValue='key'
                                              onChange={onChangeValue}
                                              name='position'
                                              required
                                              value={values.position.value}
                                    />
                                </div>
                                {values.position.isValid ? null : <small id="position-help"
                                                                         className="p-error p-d-block">{values.position.errorMessage}</small>}
                            </div>
                            <div className='p-field p-col-12'>
                                <label htmlFor='phones'>Phones
                                    <span className='required'>*</span></label>
                                <div className='p-inputgroup'>
                                    <span className='p-inputgroup-addon'>
                                       <AiFillPhone/>
                                    </span>
                                    <Chips id='phones'
                                           separator=','
                                           placeholder='Enter at least a phone number'
                                           allowDuplicate={false}
                                           value={values.phones.value}
                                           onChange={e => setValues({
                                               ...values,
                                               phones: {
                                                   ...values.phones,
                                                   value: e.value
                                               }
                                           })}
                                           onRemove={e => setValues({
                                               ...values,
                                               phones: {
                                                   ...values.phones,
                                                   value: values.phones.value.filter(i => i !== e.value)
                                               }
                                           })}
                                    />
                                </div>
                                {values.phones.isValid ? null : <small id="phones-help"
                                                                       className="p-error p-d-block">{values.phones.errorMessage}</small>}
                            </div>
                            <div className='p-field p-col-12'>
                                <label htmlFor='emails'>Emails
                                    <span className='required'>*</span></label>
                                <div className='p-inputgroup'>
                                    <span className='p-inputgroup-addon'>
                                       <MdEmail/>
                                    </span>
                                    <Chips id='emails' separator=','
                                           placeholder='Enter at least an email'
                                           allowDuplicate={false}
                                           value={values.emails.value}
                                           onChange={e => setValues({
                                               ...values,
                                               emails: {
                                                   ...values.emails,
                                                   value: e.value
                                               }
                                           })}
                                           onRemove={e => setValues({
                                               ...values,
                                               emails: {
                                                   ...values.emails,
                                                   value: values.emails.value.filter(i => i !== e.value)
                                               }
                                           })}
                                    />
                                </div>
                                {values.emails.isValid ? null : <small id="emails-help"
                                                                       className="p-error p-d-block">{values.emails.errorMessage}</small>}
                            </div>
                            <div className='p-field p-col-12'>
                                <label htmlFor='company'>Office Address:</label>
                                <div className='p-inputgroup'>
                                    <span className='p-inputgroup-addon'>
                                        <ImOffice/>
                                    </span>
                                    <InputText placeholder='Please enter your office address'
                                               id='company'
                                               name='company'
                                               value={address.company}
                                               onChange={onChangeAddress}/>
                                </div>
                            </div>
                            <div className='p-field p-col-12'>
                                <label htmlFor='home'>Personal Address:</label>
                                <div className='p-inputgroup'>
                                    <span className='p-inputgroup-addon'>
                                        <FaAddressBook/>
                                    </span>
                                    <InputText placeholder='Please enter your personal address'
                                               id='home'
                                               name='home'
                                               value={address.home}
                                               onChange={onChangeAddress}/>
                                </div>
                            </div>
                            <div className='p-field p-col-12'>
                                <Panel headerTemplate={extraTemplate} header='Social' toggleable collapsed={true}>
                                    <div className='p-field p-col-12'>
                                        <label htmlFor='zalo'>Zalo:</label>
                                        <div className="p-inputgroup">
                                            <span className="p-inputgroup-addon">
                                                <img src={process.env.PUBLIC_URL + '/showcase/images/zalo.svg'} />
                                            </span>
                                            <InputText
                                                id='zalo'
                                                placeholder='Enter zalo social'
                                                name='zalo'
                                                value={socials.zalo ?? ''}
                                                onChange={onChangeSocial}
                                            />
                                        </div>
                                    </div>

                                    <div className='p-field p-col-12'>
                                        <label htmlFor='facebook'>Facebook:</label>
                                        <div className='p-inputgroup'>
                                            <span className='p-inputgroup-addon'>
                                                <AiFillFacebook/>
                                            </span>
                                            <InputText
                                                id='facebook'
                                                name='facebook'
                                                value={socials.facebook ?? ''}
                                                onChange={onChangeSocial}
                                                placeholder='Enter facebook social'/>
                                        </div>
                                    </div>

                                    <div className='p-field p-col-12'>
                                        <label htmlFor='skype'>Skype:</label>
                                        <div className='p-inputgroup'>
                                            <span className='p-inputgroup-addon'>
                                                <AiFillSkype/>
                                            </span>
                                            <InputText
                                                id='skype'
                                                value={socials.skype ?? ''}
                                                placeholder='Enter skype social'
                                                name='skype'
                                                onChange={onChangeSocial}
                                            />
                                        </div>
                                    </div>

                                    <div className='p-field p-col-12'>
                                        <label htmlFor='linkedin'>Linkedin:</label>
                                        <div className='p-inputgroup'>
                                            <span className='p-inputgroup-addon'>
                                                <AiFillLinkedin/>
                                            </span>
                                            <InputText
                                                id='linkedin'
                                                placeholder='Enter linkedin social'
                                                name='linkedin'
                                                value={socials.linkedin ?? ''}
                                                onChange={onChangeSocial}
                                            />
                                        </div>
                                    </div>
                                </Panel>
                            </div>

                            {/*<div className='p-field p-col-12'>*/}
                            {/*<Panel headerTemplate={extraTemplate} header='History' toggleable*/}
                            {/*collapsed={true}>*/}
                            {/*<div className='p-field p-col-12'>*/}
                            {/*<label htmlFor='assign'>&nbsp;</label>*/}
                            {/*<div className='p-inputgroup'>*/}

                            {/*<Timeline value={event} layout="horizontal" align="top"*/}
                            {/*marker={timelineMarker}*/}
                            {/*content={timelineContent}/>*/}
                            {/*</div>*/}
                            {/*</div>*/}
                            {/*</Panel>*/}
                            {/*</div>*/}
                        </div>

                    </div>
                    <div className={`p-col-2 sticky-wrapper `}>
                        <div className={`p-field ${sticky ? 'sticky' : ''}`}>
                            <label>
                                &nbsp;
                            </label>
                            <div>
                                <Button icon='pi pi-send'
                                        label={screen === CONSTANTS.SCREEN.CREATE ? 'Create' : 'Update'}
                                />
                            </div>
                            {screen === CONSTANTS.SCREEN.CREATE ? null : <div className='p-mt-3'>
                                <Button icon='pi pi-trash'
                                        className='p-button-outlined p-button-danger'
                                        type='button'
                                        onClick={onRemove}
                                        label='Remove'
                                />
                            </div>}
                        </div>
                    </div>
                </div>
            </form>
        </CreateView>
    );
};


const mapStateToProps = state => ({
    initial: state.initial,
    messenger: state.messenger,
    contact: state.contact.item,
});

export default connect(mapStateToProps, {...CONTACT_API})(Create);