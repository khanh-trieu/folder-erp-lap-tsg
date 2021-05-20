import React from 'react';
import {Button} from "primereact/button";
import {Link, Redirect, Route, Switch, useHistory} from "react-router-dom";
import List from "./List";
import Create from "./Create";
import {ROUTE} from "../../common/route";
import PrivateRoute from "../../components/PrivateRoute";

const Account = () => {
    let history = useHistory();
    return (
        <div className="main-content">
            <div className='content-section introduction'>
                {
                    ROUTE.ACCOUNT.INDEX === history.location.pathname ?
                        <h1>Account</h1> :
                        <Link to={ROUTE.ACCOUNT.INDEX}>
                            <Button label='Back' icon={'pi pi-arrow-left'} className='p-button-outlined'/>
                        </Link>
                }
                <div>
                    {
                        ROUTE.ACCOUNT.INDEX === history.location.pathname ?
                            <Link to={ROUTE.ACCOUNT.CREATE}>
                                <Button label={'New'} icon={'pi pi-plus'} className='p-button-info'/>
                            </Link> : ROUTE.ACCOUNT.CREATE === history.location.pathname ?
                            <h2>Create Account</h2> : <h2>&nbsp;</h2>
                    }
                </div>
            </div>
            <div className='content-section documentation '>
                <Switch>
                    <PrivateRoute path={ROUTE.ACCOUNT.CREATE}>
                        <Create/>
                    </PrivateRoute>
                    <PrivateRoute path={ROUTE.ACCOUNT.EDIT}>
                        <Create/>
                    </PrivateRoute>
                    <PrivateRoute exact path={ROUTE.ACCOUNT.INDEX}>
                        <List/>
                    </PrivateRoute>
                </Switch>
            </div>
        </div>
    );
};


export default Account;