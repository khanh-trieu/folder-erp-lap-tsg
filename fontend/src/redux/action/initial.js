import {API} from "../../api";
import {ACTION} from "./index";
import axios from 'axios';

export const getContactType = () => async dispatch => {
    // await axiosInstance().get()
};

export const getContactInitData = () => async dispatch => {
    await axios
        .get(API.INITIAL.CONTACT_INITIAL_API)
        .then(res => {
            dispatch({
                type: ACTION.INITIAL.GET_CONTACT_INITIAL_DATA,
                payload: res.data,
            })
        })
        .catch(err => {
            console.log('get contact address', err.response);
        })
};