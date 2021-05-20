import React, {Component} from 'react';
import {Redirect, Route, Switch, withRouter} from 'react-router-dom';
import AppContentContext from './AppContentContext';
import Account from "../../screen/Account/Account";
import {ROUTE} from "../../common/route";
import Contact from "../../screen/Contact/Contact";
import PrivateRoute from "../PrivateRoute";

class AppRouter extends Component {
    render() {
        return (
            <AppContentContext.Consumer>
                {
                    context => (
                        <Switch>
                            <Route path={[ROUTE.ACCOUNT.INDEX]} component={Account}/>
                            <Route path={ROUTE.CONTACT.INDEX} component={Contact}/>
                            <Route path={ROUTE.DASHBOARD}>
                                <Redirect to={ROUTE.ACCOUNT.INDEX} />
                            </Route>
                        </Switch>
                    )
                }
            </AppContentContext.Consumer>);
    }
}

export default withRouter(AppRouter);
