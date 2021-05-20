import axiosInstance from "../../utils/axiosInstance";
import {API} from "../../api";
import {ACTION} from "./index";

const getListOwner = () => dispatch => {
    axiosInstance(false)
        .get(API.USER.API)
        .then(res => {
            dispatch({type: ACTION.USER.USER_GET_ALL, payload: res.data});
        })
        .catch(err => {
            console.log(err.response);
        })
};

export const USER_API = {
    getListOwner,
};