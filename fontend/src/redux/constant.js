import {ACTION} from "./action";

export function render_message_ok(action, message = 'Successful!', title = 'Success') {
    return {
        type: ACTION.MESSAGE.OK,
        payload: {
            title: title,
            message: message,
            action: action,
        }
    };
}

export function render_message_err(action, message = 'Something went wrong. Please try again later!', title = 'Error') {
    return {
        type: ACTION.MESSAGE.ERROR,
        payload: {
            title: title,
            message: message,
            action: action,
        }
    };
}