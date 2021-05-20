import {ACTION} from "./index";

export const startBlock = () => dispatch => {
    dispatch({type: ACTION.BLOCKER.BLOCK});
};

export const stopBlock = () => dispatch => {
    dispatch({type: ACTION.BLOCKER.UNBLOCK});
};