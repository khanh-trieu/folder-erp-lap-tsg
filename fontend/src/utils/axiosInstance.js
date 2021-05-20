import axios from 'axios';
import {startBlock, stopBlock} from "../redux/action/blocker";
import {store} from '../store';

export default (block = true) => {
    let headers = {
        'Content-type': 'Application/json'
    };
    const axiosInstance = axios.create({
        headers
    });

    const {dispatch} = store;

    axiosInstance.interceptors.request.use(config => {
        if(block)
            dispatch(startBlock());
        return config;
    });

    axiosInstance.interceptors.response.use(
        response => {
            if(block)
                dispatch(stopBlock());
            return response;
        },
        error => {
            if(block)
                dispatch(stopBlock());
            return new Promise((resolve, reject) => {
                reject(error);
            });
        }
    );

    return axiosInstance;
}