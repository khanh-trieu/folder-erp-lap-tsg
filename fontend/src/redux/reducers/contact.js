import {ACTION} from "../action";

const initState = {
    list: [],
    search: [],
    item: {},
    initial: {
        position: [],
    }
};

export default function (state = initState, {type, payload}) {
    switch (type) {
        case ACTION.CONTACT.GET_ALL:
            return {
                ...state,
                list: payload.results,
            };
        case ACTION.CONTACT.REMOVE_ITEM:
            const newState = state.list.filter(i => i.id !== payload);
            return {
                ...state,
                list: newState
            };
        case ACTION.CONTACT.GET_ITEM:
            return {
                ...state,
                item: payload,
            };
        case ACTION.CONTACT.RESET_ITEM:
            return {
                ...state,
                item: {},
            };
        case ACTION.CONTACT.GET_POSITION:
            return {
                ...state,
                initial: {
                    ...state.initial,
                    position: payload,
                }
            };
        case ACTION.CONTACT.SEARCH_ITEM:
            return {
                ...state,
                search: payload.results
            };
        case ACTION.CONTACT.RESET_SEARCH:
            return {
                ...state,
                search: [],
            };
        default:
            return state;
    }
}