// ACCOUNT TYPE
const ACCOUNT = {
    GET_ALL: 'ACCOUNT_GET_ALL',
    GET_ITEM: 'ACCOUNT_GET_ITEM',
    RESET_ITEM: 'ACCOUNT_RESET_ITEM',
    SEARCH_ITEM: 'ACCOUNT_SEARCH_ITEM',
    RESET_SEARCH: 'ACCOUNT_RESET_SEARCH',
    GET_CONTACT: 'ACCOUNT_GET_CONTACT',
};

const CONTACT = {
    GET_ALL: 'CONTACT_GET_ALL',
    GET_ITEM: 'CONTACT_GET_ITEM',
    GET_POSITION: 'GET_POSITION',
    RESET_ITEM: 'CONTACT_RESET_ITEM',
    REMOVE_ITEM: 'CONTACT_REMOVE_ITEM',
    SEARCH_ITEM: 'CONTACT_SEARCH_ITEM',
    RESET_SEARCH: 'CONTACT_RESET_SEARCH'
};

const BLOCKER = {
    BLOCK: 'BLOCK',
    UNBLOCK: 'UNBLOCK',
};

const INITIAL = {
    GET_CONTACT_ADDRESS_TYPE: 'GET_CONTACT_ADDRESS_TYPE',
    GET_CONTACT_INITIAL_DATA: 'GET_CONTACT_INITIAL_DATA'
};

const MESSAGE = {
    OK: 'OK',
    ERROR: 'ERROR',
    RESET: 'RESET',
};

const AUTH = {
    LOGIN_SUCCESS: 'LOGIN_SUCCESS',
    LOGOUT: 'LOGOUT',
};

const USER = {
    USER_GET_ALL: 'USER_GET_ALL',
};

export const ACTION = {
    ACCOUNT: ACCOUNT,
    CONTACT: CONTACT,
    BLOCKER: BLOCKER,
    INITIAL: INITIAL,
    MESSAGE: MESSAGE,
    AUTH: AUTH,
    USER: USER,
};