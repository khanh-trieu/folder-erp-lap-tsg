import React from 'react';
import {ROUTE} from "../../common/route";
import {Link, Route, Switch, useRouteMatch} from "react-router-dom";
import List from './List';
import {Button} from "primereact/button";
import Create from "./Create";
import PrivateRoute from "../../components/PrivateRoute";

const Contact = () => {
    const matchCreateRoute = useRouteMatch(ROUTE.CONTACT.CREATE);
    const matchIndexRoute = useRouteMatch(ROUTE.CONTACT.INDEX);
    const matchEditRoute = useRouteMatch(ROUTE.CONTACT.EDIT);

    return (
        <div className='main-content'>
            <div className='content-section introduction'>
                {
                    matchIndexRoute?.isExact ?
                        <h2>Contacts</h2> :
                        <Link to={ROUTE.CONTACT.INDEX}>
                            <Button className='p-button-outlined' label='Back' icon='pi pi-arrow-left'/>
                        </Link>
                }
                <div>
                    {
                        matchCreateRoute?.isExact ?
                            <h2>Create Contact</h2> :
                            matchEditRoute?.isExact ?
                                <h2>Edit Contact</h2> :
                                <Link to={ROUTE.CONTACT.CREATE}>
                                    <Button icon='pi pi-plus' label='New'/>
                                </Link>
                    }
                </div>
            </div>
            <div className='content-section documentation '>
                <Switch>
                    <PrivateRoute exact path={ROUTE.CONTACT.CREATE}>
                        <Create/>
                    </PrivateRoute>
                    <PrivateRoute exact path={ROUTE.CONTACT.EDIT}>
                        <Create/>
                    </PrivateRoute>
                    <PrivateRoute exact path={ROUTE.CONTACT.INDEX}>
                        <List/>
                    </PrivateRoute>
                </Switch>
            </div>
        </div>
    );
};

export default Contact;