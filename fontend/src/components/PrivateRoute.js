import React, {Component} from 'react';
import {connect} from "react-redux";
import {Redirect, Route} from "react-router-dom";
import {ROUTE} from "../common/route";

const PrivateRoute = ({component: Component, auth, ...rest}) => {
    return <Route
        {...rest}
        render={
            props => {
                if (auth.isAuthenticated) {
                    return <Component {...props} />
                } else {
                    return <Redirect to={ROUTE.AUTH.LOGIN}/>
                }
            }
        }
    />
};

const mapStateToProps = (state) => ({
    auth: state.user,
});

export default connect(mapStateToProps)(PrivateRoute);