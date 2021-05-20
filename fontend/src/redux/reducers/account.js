import {ACTION} from "../action";

const initState = {
    list: [],
    item: null,
    search: [],
    searchRecords: 0,
    totalRecords: 0,
};

export default function (state = initState, {type, payload}) {
    switch (type) {
        case ACTION.ACCOUNT.GET_ALL:
            return {
                ...state,
                list: [...payload.results],
                totalRecords: payload.count,
            };
        case ACTION.ACCOUNT.SEARCH_ITEM:
            return {
                ...state,
                search: payload.results,
                searchRecords: payload.count,
            };
        case ACTION.ACCOUNT.RESET_SEARCH:
            return {
                ...state,
                search: [],
                searchRecords: 0,
            };
        case ACTION.ACCOUNT.GET_ITEM:
            return {
                ...state,
                item: payload
            };
        case ACTION.ACCOUNT.GET_CONTACT:
            return {
                ...state,
                item: {
                    ...state.item,
                    contacts: payload,
                }
            };
        case ACTION.ACCOUNT.RESET_ITEM:
            return {
                ...state,
                item: null,
            };
        default:
            return state;
    }
};