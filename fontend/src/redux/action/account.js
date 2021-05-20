import {API} from "../../api";
import {ACTION} from "./index";
import axiosInstance from "../../utils/axiosInstance";
import {render_message_err, render_message_ok} from "../constant";
import {CONSTANTS} from "../../common/constants";
import {CONTACT_API} from "./contact";

const getAccounts = (page = 1) => dispatch => {
    axiosInstance().get(API.ACCOUNT.PAGE + page)
        .then(res => {
            dispatch({
                type: ACTION.ACCOUNT.GET_ALL,
                payload: res.data,
            })
        })
        .catch(err => {
            console.log(err);
        })
};

const getAccount = id => dispatch => {
    axiosInstance()
        .get(`${API.ACCOUNT.API}/${id}`)
        .then(res => {
            dispatch({
                type: ACTION.ACCOUNT.GET_ITEM,
                payload: res.data,
            });
            if (res.data.contacts) {
                CONTACT_API.getSubListContact(res.data.contacts)(dispatch);
            }
        })
        .catch(err => {
            console.log(err.response);
        })
};

const checkTaxNumber = number => dispatch => {
    axiosInstance()
        .get(API.ACCOUNT.CHECK_TAX_NUMBER + number)
        .then(res => {
            dispatch(render_message_ok(CONSTANTS.SCREEN.CHECK_TAX, 'Tax number is valid'));
        })
        .catch(err => {
            console.log('check tax number', err.response);
            dispatch(render_message_err(CONSTANTS.SCREEN.CHECK_TAX, 'Tax number is invalid'));
        })
};

const createAccount = payload => dispatch => {
    axiosInstance()
        .post(API.ACCOUNT.API, payload)
        .then(res => {
            dispatch(render_message_ok(CONSTANTS.SCREEN.CREATE, 'Create successful!'));
        })
        .catch(err => {
            console.log('create contact', err.response);
            dispatch(render_message_err(CONSTANTS.SCREEN.CREATE));
        })
};

const updateAccount = (id, payload) => dispatch => {
    axiosInstance()
        .put(`${API.ACCOUNT.API}/${id}`, payload)
        .then(res => {
            dispatch(render_message_ok(CONSTANTS.SCREEN.EDIT, 'Update successful!'));
        })
        .catch(err => {
            console.log('update contact', err.response);
            dispatch(render_message_err(CONSTANTS.SCREEN.EDIT));
        })
};

const searchAccountName = name => dispatch => {
    axiosInstance(false)
        .get(`${API.ACCOUNT.SEARCH}` + name)
        .then(res => {
            dispatch({
                type: ACTION.ACCOUNT.SEARCH_ITEM,
                payload: res.data,
            })
        })
        .catch(err => {
            console.log('search account', err.response);
        })
};

const resetSearch = () => dispatch => {
    dispatch({
        type: ACTION.ACCOUNT.RESET_SEARCH,
    });
};

export const ACCOUNT_API = {
    getAccounts,
    getAccount,
    checkTaxNumber,
    createAccount,
    updateAccount,
    searchAccountName,
    resetSearch,
};
