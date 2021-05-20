import {ACTION} from "../action";

const initialState = {
    contact: {
        address: [],
        socials: [],
        positions: [],
    }
};

export default function (state = initialState, {type, payload}) {
    switch (type) {
        case ACTION.INITIAL.GET_CONTACT_INITIAL_DATA:
            return {
                ...state,
                contact: payload,
            };
        default:
            return state;
    }
}