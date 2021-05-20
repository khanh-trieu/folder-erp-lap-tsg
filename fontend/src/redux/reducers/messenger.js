import {ACTION} from "../action";

const initState = {
    type: null,
    message: '',
    title: '',
    action: null,
    id: null,
};

export default function (state = initState, {type, payload}) {
    switch (type) {
        case ACTION.MESSAGE.OK:
        case ACTION.MESSAGE.ERROR:
            return {
                type: type,
                message: payload?.message ?? '',
                title: payload?.title ?? '',
                action: payload?.action ?? null,
                id: payload?.id ?? null
            };
        case ACTION.MESSAGE.RESET:
            return initState;
        default:
            return state;
    }

}