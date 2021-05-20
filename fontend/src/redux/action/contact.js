import axiosInstance from "../../utils/axiosInstance";
import {API} from "../../api";
import {ACTION} from "./index";
import {CONSTANTS} from "../../common/constants";
import {render_message_err, render_message_ok} from "../constant";

const createContact = payload => dispatch => {
    axiosInstance()
        .post(API.CONTACT.API, payload)
        .then(res => {
            dispatch(render_message_ok(CONSTANTS.SCREEN.CREATE, 'Create successful!'));
        })
        .catch(err => {
            console.log('create contact', err.response.data);
            dispatch(render_message_err(CONSTANTS.SCREEN.CREATE))
        })
};

const updateContact = (id, payload) => dispatch => {
    axiosInstance()
        .put(`${API.CONTACT.API}/${id}`, payload)
        .then(res => {
            dispatch(render_message_ok(CONSTANTS.SCREEN.EDIT, 'Update successful!'));
        })
        .catch(err => {
            console.log('update contact', err.response);
            dispatch(render_message_err(CONSTANTS.SCREEN.EDIT));
        })
};

const removeContact = id => dispatch => {
    axiosInstance()
        .delete(`${API.CONTACT.API}/${id}`)
        .then(res => {
            const messengerOk = render_message_ok(CONSTANTS.SCREEN.DELETE, 'Delete successful!');
            messengerOk['payload']['id'] = id;
            dispatch({
                ...messengerOk
            });
        })
        .catch(err => {
            console.log('delete contact', err.response);
            const messengerError = render_message_err(CONSTANTS.SCREEN.DELETE);
            messengerError['payload']['id'] = id;
            dispatch({
                ...messengerError
            })
        })
};

const searchContactName = name => dispatch => {
    axiosInstance(false)
        .get(`${API.CONTACT.SEARCH}` + name)
        .then(res => {
            dispatch({type: ACTION.CONTACT.SEARCH_ITEM, payload: res.data});
        })
};

const getContacts = () => dispatch => {
    axiosInstance()
        .get(API.CONTACT.API)
        .then(res => {
            dispatch({
                type: ACTION.CONTACT.GET_ALL,
                payload: res.data,
            })
        })
        .catch(err => {
            console.log('contact', err.response);
        })
};

const getContact = id => dispatch => {
    axiosInstance()
        .get(`${API.CONTACT.API}/${id}`)
        .then(res => {
            dispatch({
                type: ACTION.CONTACT.GET_ITEM,
                payload: res.data,
            })
        })
        .catch(err => {
            console.log('contact item', err.response);
        })
};

const getSubListContact = listId => dispatch => {
    const joinId = listId.reduce((result, item) => `${result},${item}`);
    axiosInstance(false)
        .get(`${API.CONTACT.SUBLIST}` + joinId)
        .then(res => {
            dispatch({
                type: ACTION.ACCOUNT.GET_CONTACT,
                payload: res.data,
            })
        })
        .catch(err => {
            console.log('contact item', err.response);
        })
};


const getContactPositionData = () => dispatch => {
    axiosInstance()
        .get(API.INITIAL.CONTACT_POSITION_API)
        .then(res => {
            dispatch({
                type: ACTION.CONTACT.GET_POSITION,
                payload: res.data,
            })
        })
        .catch(err => {
            console.log('contact position', err.response);
        })
};

export const CONTACT_API = {
    getContact,
    getContactPositionData,
    getContacts,
    updateContact,
    createContact,
    removeContact,
    searchContactName,
    getSubListContact,
};