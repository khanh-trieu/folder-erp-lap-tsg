import {DOMAIN} from "./config/config";


const ACCOUNT_API = `${DOMAIN}/accounts`;
const ACCOUNT_PAGE_API = `${DOMAIN}/accounts?page=`;
const ACCOUNT_SEARCH_API = `${DOMAIN}/accounts?search=`;
const CHECK_TAX_NUMBER_API = `${ACCOUNT_API}/check-tax-code?tax_code=`;

const CONTACT_API = `${DOMAIN}/contacts`;
const CONTACT_SUBLIST_API = `${DOMAIN}/contacts/list?id=`;
const CONTACT_SEARCH_API = `${DOMAIN}/contacts?search=`;

const CONTACT_POSITION_API = `${CONTACT_API}/list?type=positions`;
const CONTACT_ADDRESS_TYPE_API = `${CONTACT_API}/list?type=address`;
const CONTACT_POSITION_TYPE_API = `${CONTACT_API}/list?type=positions`;
const CONTACT_INITIAL_API = `${CONTACT_API}/list?type=all`;

const USER_API = `${DOMAIN}/users`;

export const API = {
    INITIAL: {
        CONTACT_POSITION_API: CONTACT_POSITION_API,
        CONTACT_ADDRESS_TYPE_API: CONTACT_ADDRESS_TYPE_API,
        CONTACT_POSITION_TYPE_API: CONTACT_POSITION_TYPE_API,
        CONTACT_INITIAL_API: CONTACT_INITIAL_API,
    },
    ACCOUNT: {
        API: ACCOUNT_API,
        SEARCH: ACCOUNT_SEARCH_API,
        PAGE: ACCOUNT_PAGE_API,
        CHECK_TAX_NUMBER: CHECK_TAX_NUMBER_API,
    },
    CONTACT: {
        API: CONTACT_API,
        SUBLIST: CONTACT_SUBLIST_API,
        SEARCH: CONTACT_SEARCH_API,
    },
    USER: {
        API: USER_API,
    }

};