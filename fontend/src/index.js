import 'react-app-polyfill/ie9';
import {PersistGate} from 'redux-persist/lib/integration/react';
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import {BrowserRouter as Router, Route, Switch} from 'react-router-dom';
import {persistor, store} from './store';
import {Provider} from "react-redux";
import {ROUTE} from "./common/route";
import Login from "./screen/Login/Login";
import PrivateRoute from "./components/PrivateRoute";

ReactDOM.render(
    <Router>
        <Provider store={store}>
            <PersistGate loading={null} persistor={persistor}>
                <Switch>
                    <Route path={ROUTE.AUTH.LOGIN} component={Login}/>
                    <PrivateRoute path={ROUTE.DASHBOARD} component={App}/>
                </Switch>
            </PersistGate>
        </Provider>
    </Router>,
    document.getElementById('root')
);
