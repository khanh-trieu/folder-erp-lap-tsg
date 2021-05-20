import React, {useState} from 'react';
import 'core-js/stable';
import 'regenerator-runtime/runtime';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';
import 'prismjs/themes/prism-coy.css';
import '../../assets/style/app/App.scss';

import {useFormik} from 'formik';
import {InputText} from 'primereact/inputtext';
import {Button} from 'primereact/button';
import {Password} from 'primereact/password';
import {Divider} from 'primereact/divider';
import {classNames} from "primereact/components/utils/ClassNames";
import './Login.css';
import {Card} from "primereact/card";
import {loginRequest, msalConfig} from "../../config/config";
import * as msal from "@azure/msal-browser";
import {connect, useDispatch} from "react-redux";
import {Redirect} from "react-router-dom";
import {ROUTE} from "../../common/route";
import {ACTION} from "../../redux/action";

const Login = (props) => {

    const [formData, setFormData] = useState({});
    const msalInstance = new msal.PublicClientApplication(msalConfig);
    const formik = useFormik({
        initialValues: {
            name: '',
            email: '',
            password: '',
            date: null,
            country: null,
            accept: false
        },
        validate: (data) => {
            let errors = {};

            if (!data.name) {
                errors.name = 'Name is required.';
            }

            if (!data.email) {
                errors.email = 'Email is required.';
            } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(data.email)) {
                errors.email = 'Invalid email address. E.g. example@email.com';
            }

            if (!data.password) {
                errors.password = 'Password is required.';
            }

            if (!data.accept) {
                errors.accept = 'You need to agree to the terms and conditions.';
            }

            return errors;
        },
        onSubmit: (data) => {
            setFormData(data);

            formik.resetForm();
        }
    });
    const dispatch = useDispatch();


    const isFormFieldValid = (name) => !!(formik.touched[name] && formik.errors[name]);
    const getFormErrorMessage = (name) => {
        return isFormFieldValid(name) && <small className="p-error">{formik.errors[name]}</small>;
    };


    const handleLogin = async (e) => {
        await msalInstance.loginPopup(loginRequest);
        const accounts = msalInstance.getAllAccounts();
        if (accounts.length > 0) {
            dispatch({type: ACTION.AUTH.LOGIN_SUCCESS, payload: {isAuthenticated: true, username: accounts[0].username}});
        }
    };
    return (
        props.auth.isAuthenticated ? <Redirect to={ROUTE.DASHBOARD}/> :
            <div className="form-demo">
                <div className="p-d-flex p-jc-center p-ai-center p-shadow-2" style={{height: '100%'}}>
                    <Card>
                        <div className="card">
                            <h3 className="p-text-center p-text-bold p-text-uppercase title">ERP System</h3>
                            <h5 className="p-text-center p-text-secondary">Login</h5>

                            <form onSubmit={formik.handleSubmit} className="p-fluid p-mb-5">

                                <div className="p-field">
                            <span className="p-float-label p-input-icon-right">
                                <i className="pi pi-envelope"/>
                                <InputText id="email" name="email" value={formik.values.email}
                                           onChange={formik.handleChange}
                                           className={classNames({'p-invalid': isFormFieldValid('email')})}/>
                                <label htmlFor="email"
                                       className={classNames({'p-error': isFormFieldValid('email')})}>Email*</label>
                            </span>
                                    {getFormErrorMessage('email')}
                                </div>
                                <div className="p-field">
                            <span className="p-float-label">
                                <Password id="password" name="password" value={formik.values.password}
                                          onChange={formik.handleChange} toggleMask
                                          className={classNames({'p-invalid': isFormFieldValid('password')})}
                                />
                                <label htmlFor="password"
                                       className={classNames({'p-error': isFormFieldValid('password')})}>Password*</label>
                            </span>
                                    {getFormErrorMessage('password')}
                                </div>


                                <Button type="submit" label="Submit" className="p-mt-2"/>
                            </form>

                            <Divider layout="horizontal" align='center'>
                                <b>OR</b>
                            </Divider>

                            <div className='p-d-flex p-flex-row p-jc-around p-mt-5'>
                                <Button label='Login with Microsoft'
                                        className='p-button-outlined p-button-secondary'
                                        icon='pi pi-microsoft'
                                        onClick={handleLogin}
                                />

                                <Button label='Login with Google' className='p-button-outlined p-button-secondary'
                                        icon='pi pi-google'/>
                            </div>
                        </div>
                    </Card>
                </div>
            </div>

    );
};

const mapStateToProps = state => ({
    auth: state.user,
});

export default connect(mapStateToProps)(Login);