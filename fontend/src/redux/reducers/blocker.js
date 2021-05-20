import {ACTION} from "../action";

const initState = {block: 0};

export default function (state = initState, {type}) {
    switch (type) {
        case ACTION.BLOCKER.BLOCK:
            return {
                ...state,
                block: 1
            };
        case ACTION.BLOCKER.UNBLOCK:
            return {
                ...state,
                block: 0,
            };
        default:
            return state;
    }
}