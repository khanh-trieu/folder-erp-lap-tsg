import React, {useEffect, useRef, useState} from 'react';
import {InputText} from "primereact/inputtext";
import {FaCheck, FaUserTie} from "react-icons/fa";
import {RiAccountBoxFill, RiNumbersFill} from "react-icons/ri";
import {Dropdown} from "primereact/dropdown";
import styled from 'styled-components';
import {Button} from "primereact/button";
import {Divider} from "primereact/divider";
import {ImOffice} from "react-icons/im";
import {AiFillPhone} from "react-icons/ai";
import {MdEmail, MdPermIdentity} from "react-icons/md";
import {Panel} from "primereact/panel";
import {Ripple} from "primereact/ripple";
import {BiNetworkChart} from "react-icons/bi";
import {IoEarthSharp} from "react-icons/io5";
import {useFormik} from "formik";
import {classNames} from "primereact/components/utils/ClassNames";
import {connect, useDispatch} from "react-redux";
import {ACCOUNT_API} from "../../redux/action/account";
import {Toast} from "primereact/toast";
import {ACTION} from "../../redux/action";
import {CONSTANTS} from "../../common/constants";
import {useParams, useHistory} from 'react-router-dom';
import ViewContact from "./ViewContact";
import OwnerInputBox from "./OwnerInputBox";
import swal from "sweetalert";
import {ROUTE} from "../../common/route";

const CreateView = styled.div`
    .p-panel-content {
        padding: 0 !important;
        border: none !important;
    }
`;

const Create = (props) => {
    const history = useHistory();
    const [formData, setFormData] = useState({});
    const {id} = useParams();
    const SCREEN = id === undefined ? CONSTANTS.SCREEN.CREATE : CONSTANTS.SCREEN.EDIT;
    const toast = useRef(null);
    const dispatch = useDispatch();
    const formik = useFormik({
        enableReinitialize: true,
        initialValues: {
            name: props?.account?.name ?? '',
            en_name: props?.account?.en_name ?? '',
            emails: props?.account?.emails[0] ?? '',
            phones: props?.account?.phones[0] ?? '',
            account_type: props?.account?.company?.key ?? '',
            tax_code: props?.account?.tax_code ?? '',
            address: props?.account?.address ?? '',
            representer: props?.account?.representer ?? '',
            email_provider: props?.account?.email_provider ?? '',
            website: props?.account?.website ?? '',
            province: props?.account?.province ?? '',
            district: props?.account?.district ?? '',
            ward: props?.account?.ward ?? '',
            number_of_pc: props?.account?.number_of_pc ?? 0,
            number_of_server: props?.account?.number_of_server ?? 0,
            contacts: props?.account?.contacts ?? [],
            user_id: props?.account?.user_id ?? '',
        },
        validate: data => {
            let errors = {};
            if (!data.name) {
                errors.name = 'Name is required.';
            }

            if (!data.emails) {
                errors.emails = 'Email is required.';
            } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(data.emails)) {
                errors.emails = 'Invalid email address. E.g. example@email.com';
            }

            if (!data.phones) {
                errors.phones = 'Phone is required.';
            }

            if (!data.tax_code) {
                errors.tax_code = 'Tax number is required.';
            }

            if (!data.account_type) {
                errors.account_type = 'Account type is required.';
            }

            return errors;
        },
        onSubmit: values => {
            setFormData(values);
            const payload = {
                ...values,
                phones: [values.phones],
                emails: [values.emails],
                district: values.district.key,
                ward: values.ward.key,
                province: values.province.key,
                contacts: values.contacts.length > 0 ? values.contacts?.map(i => i.id) : null,
                company: values.account_type,
            };
            if (SCREEN === CONSTANTS.SCREEN.CREATE) {
                props.createAccount(payload);
            }
            if (SCREEN === CONSTANTS.SCREEN.EDIT) {
                if (id !== null) {
                    props.updateAccount(id, payload);
                }
            }
        },
    });

    const isFormFieldValid = name => !!(formik.touched[name] && formik.errors[name]);
    const getFormErrorMessage = name => {
        return isFormFieldValid(name) && <small className='p-error'>{formik.errors[name]}</small>
    };

    const checkTaxCode = (e) => {
        e.stopPropagation();

        if (!formik.values.tax_code) {
            toast.current.show({
                severity: 'error',
                summary: 'Error',
                detail: 'Tax number is empty',
                timeout: 3000,
            });
            return;
        }
        props.checkTaxNumber(formik.values.tax_code);
    };

    const onChooseAccount = (id) => {
        const oldState = formik.values.contacts;
        const newState = [id, ...oldState];
        formik.setValues({
            ...formik.values, contacts: newState
        });
    };

    const onRemoveAccount = (id) => {
        const newState = formik.values.contacts.filter(i => i.id !== id);
        formik.setValues({
            ...formik.values, contacts: newState,
        })
    };

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

    useEffect(() => {
        if (SCREEN === CONSTANTS.SCREEN.CREATE) {
            dispatch({type: ACTION.ACCOUNT.RESET_ITEM});
        }
        if (SCREEN === CONSTANTS.SCREEN.EDIT) {
            props.getAccount(id);
        }
    }, []);

    useEffect(() => {
        if (props.messenger.type !== null) {
            switch (props.messenger.action) {
                case CONSTANTS.SCREEN.CHECK_TAX:
                    toast.current.show({
                        severity: props.messenger.type === ACTION.MESSAGE.OK ? 'success' : 'error',
                        summary: props.messenger.title,
                        detail: props.messenger.message,
                        life: 3000
                    });
                    break;
                case CONSTANTS.SCREEN.EDIT:
                    toast.current.show({
                        severity: props.messenger.type === ACTION.MESSAGE.OK ? 'success' : 'error',
                        detail: props.messenger.message,
                        summary: props.messenger.title,
                        life: 3000,
                    });
                    break;
                case CONSTANTS.SCREEN.CREATE:
                    swal({
                        title: props.messenger.title,
                        text: props.messenger.message,
                        icon: props.messenger.type === ACTION.MESSAGE.OK ? 'success' : 'error',
                        button: "OK",
                    }).then(value => {
                        if (props.messenger.type === ACTION.MESSAGE.OK) {
                            history.push(ROUTE.ACCOUNT.INDEX);
                        }
                    });
                    break;
            }
            dispatch({type: ACTION.MESSAGE.RESET});
        }

    }, [props.messenger]);

    return (
        <CreateView>
            <Toast ref={toast}/>
            <form onSubmit={formik.handleSubmit}>
                <div className='p-grid'>
                    <div className='p-col-8'>
                        <div className='p-fluid p-grid p-formgrid'>
                            <div className='p-field p-col-12'>
                                <label htmlFor='name' className={classNames({'p-error': isFormFieldValid('name')})}>
                                    Name
                                    <span className='required'>*</span>
                                </label>
                                <div className='p-inputgroup'>
                                    <span className='p-inputgroup-addon'><MdPermIdentity/></span>
                                    <InputText
                                        id='name'
                                        name='name'
                                        autoFocus={true}
                                        value={formik.values.name}
                                        onChange={formik.handleChange}
                                        className={classNames({'p-invalid': isFormFieldValid('name')})}
                                    />
                                </div>
                                {getFormErrorMessage('name')}
                            </div>

                            <div className='p-field p-col-12'>
                                <label htmlFor='en_name'>Other name</label>
                                <InputText id='en_name'
                                           type='text'
                                           name='en_name'
                                           value={formik.values.en_name}
                                           onChange={formik.handleChange}/>
                            </div>

                            <div className='p-field p-col-6'>
                                <label htmlFor='tax_code'
                                       className={classNames({'p-error': isFormFieldValid('tax_code')})}>
                                    Tax number
                                    <span className='required'>*</span>
                                </label>
                                <div className='p-inputgroup'>
                                    <span className='p-inputgroup-addon'><RiNumbersFill/></span>
                                    <InputText id='tax_code'
                                               name='tax_code'
                                               format={false}
                                               className={classNames({'p-invalid': isFormFieldValid('tax_code')})}
                                               value={formik.values.tax_code}
                                               onChange={formik.handleChange}
                                    />
                                    <Button type='button' onClick={checkTaxCode}>
                                        <FaCheck/>
                                    </Button>
                                </div>
                                {getFormErrorMessage('tax_code')}
                            </div>

                            <div className='p-field p-col-6'>
                                <label htmlFor='account_type'
                                       className={classNames({'p-error': isFormFieldValid('account_type')})}
                                >Type
                                    <span className='required'>*</span>
                                </label>
                                <div className='p-inputgroup'>
                                    <span className='p-inputgroup-addon'><RiAccountBoxFill/></span>
                                    <Dropdown options={[
                                        {label: 'Company', key: 'enterprise'},
                                        {label: 'Personal', key: 'personal'},
                                    ]}
                                              className={classNames({'p-invalid': isFormFieldValid('account_type')})}
                                              id='account_type'
                                              name='account_type'
                                              optionValue='key'
                                              optionLabel='label'
                                              value={formik.values.account_type}
                                              onChange={formik.handleChange}
                                    />
                                </div>
                                {getFormErrorMessage('account_type')}
                            </div>

                            <div className='p-field p-col-4'>
                                <label htmlFor='phones'
                                       className={classNames({'p-error': isFormFieldValid('phones')})}
                                >Phone
                                    <span className='required'>*</span>
                                </label>
                                <div className='p-inputgroup'>
                                    <span className='p-inputgroup-addon'><AiFillPhone/></span>
                                    <InputText name='phones'
                                               id='phones'
                                               className={classNames({'p-invalid': isFormFieldValid('phones')})}
                                               value={formik.values.phones}
                                               onChange={formik.handleChange}
                                    />
                                </div>
                                {getFormErrorMessage('phones')}
                            </div>

                            <div className='p-field p-col-4'>
                                <label htmlFor='emails'
                                       className={classNames({'p-error': isFormFieldValid('emails')})}
                                >Email
                                    <span className='required'>*</span>
                                </label>
                                <div className='p-inputgroup'>
                                    <span className='p-inputgroup-addon'><MdEmail/></span>
                                    <InputText
                                        name='emails'
                                        id='emails'
                                        value={formik.values.emails}
                                        onChange={formik.handleChange}
                                        className={classNames({'p-invalid': isFormFieldValid('emails')})}
                                    />
                                </div>
                                {getFormErrorMessage('emails')}
                            </div>

                            <div className='p-field p-col-4'>
                                <label htmlFor='owner'>Owner</label>
                                <OwnerInputBox value={formik.values.user_id}
                                               setValue={(id) => {
                                                   formik.setValues({...formik.values, user_id: id});
                                               }}/>
                            </div>

                            <div className='p-field p-col-12'>
                                <label htmlFor='address'>Address

                                </label>
                                <div className='p-inputgroup'>
                                    <span className='p-inputgroup-addon'><ImOffice/></span>
                                    <InputText name='address'
                                               id='address'
                                               value={formik.values.address}
                                               onChange={formik.handleChange}/>
                                </div>
                            </div>

                            <div className='p-field p-col-12'>
                                <Panel toggleable collapsed={true} headerTemplate={extraTemplate} header='Extra'>
                                    <div className='p-fluid p-formgrid p-grid'>
                                        <div className='p-field p-col-4'>
                                            <label htmlFor='representer'>Representer</label>
                                            <div className='p-inputgroup'>
                                                <span className='p-inputgroup-addon'><FaUserTie/></span>
                                                <InputText name='representer'
                                                           id='representer'
                                                           value={formik.values.representer}
                                                           onChange={formik.handleChange}/>
                                            </div>
                                        </div>

                                        <div className='p-field p-col-4'>
                                            <label htmlFor='email_provider'>Email Provider</label>
                                            <div className='p-inputgroup'>
                                                <span className='p-inputgroup-addon'><BiNetworkChart/></span>
                                                <Dropdown name='email_provider' id='email_provider'
                                                          options={[
                                                              {label: 'Office365', key: 'Office365'},
                                                              {label: 'GSuite', key: 'Gsuite'},
                                                          ]}
                                                          optionValue='key'
                                                          optionLabel='label'
                                                          value={formik.values.email_provider}
                                                          onChange={formik.handleChange}
                                                />
                                            </div>
                                        </div>

                                        <div className='p-field p-col-4'>
                                            <label htmlFor='website'>Website</label>
                                            <div className='p-inputgroup'>
                                                <span className='p-inputgroup-addon'><IoEarthSharp/></span>
                                                <InputText name='website'
                                                           id='website'
                                                           value={formik.values.website}
                                                           onChange={formik.handleChange}/>
                                            </div>
                                        </div>

                                        <div className='p-field p-col-4'>
                                            <label htmlFor='province'>Province</label>
                                            <InputText name='province'
                                                       id='province'
                                                       value={formik.values.province.value}
                                                       onChange={formik.handleChange}
                                            />
                                        </div>

                                        <div className='p-field p-col-4'>
                                            <label htmlFor='district'>District</label>
                                            <InputText name='district'
                                                       id='district'
                                                       value={formik.values.district.value}
                                                       onChange={formik.handleChange}
                                            />
                                        </div>

                                        <div className='p-field p-col-4'>
                                            <label htmlFor='ward'>Ward</label>
                                            <InputText name='ward'
                                                       id='ward'
                                                       value={formik.values.ward.value}
                                                       onChange={formik.handleChange}
                                            />
                                        </div>

                                        <div className='p-field p-col-2'>
                                            <label htmlFor='number_of_pc'>No. PC</label>
                                            <InputText keyfilter='pint'
                                                       name='number_of_pc'
                                                       id='number_of_pc'
                                                       value={formik.values.number_of_pc}
                                                       onChange={formik.handleChange}
                                            />
                                        </div>

                                        <div className='p-field p-col-2'>
                                            <label htmlFor='number_of_server'>No. Server</label>
                                            <InputText keyfilter='pint'
                                                       name='number_of_server'
                                                       id='number_of_server'
                                                       value={formik.values.number_of_server}
                                                       onChange={formik.handleChange}
                                            />
                                        </div>
                                    </div>
                                </Panel>
                            </div>

                            <div className='p-field p-col-12'>
                                <Panel toggleable collapsed={true} headerTemplate={extraTemplate} header={'Contact'}>
                                    <ViewContact contacts={formik.values.contacts} addContacts={onChooseAccount}
                                                 removeContacts={onRemoveAccount}/>
                                </Panel>
                            </div>
                        </div>
                    </div>
                    <Divider layout='vertical'/>
                    <div className='p-col-1 p-d-flex p-as-end'>
                        <div className='p-field'>
                            <div>
                                <Button label={SCREEN === CONSTANTS.SCREEN.CREATE ? 'Create' : 'Update'}
                                        icon='pi pi-send' type='submit'/>
                            </div>
                        </div>
                    </div>
                </div>
            </form>
        </CreateView>
    );
};

const mapStateToProps = (state) => ({
    messenger: state.messenger,
    account: state.account.item,
});

export default connect(mapStateToProps, {
    ...ACCOUNT_API
})(Create);