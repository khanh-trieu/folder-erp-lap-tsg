import {ACTION} from "../action";

const initialState = {
    isAuthenticated: false,
    accessToken: null,
    refreshToken: null,
    username: null,
    users: [],
};

export default (state = initialState, {type, payload}) => {
    switch (type) {
        case ACTION.AUTH.LOGIN_SUCCESS:
            return {
                ...state,
                ...payload,
            };
        case ACTION.USER.USER_GET_ALL:
            return {
                ...state,
                users: payload.results,
            };
        default:
            return state;
    }
}