import {combineReducers} from "redux";
import account from './account';
import blocker from './blocker';
import contact from './contact';
import initial from './initial';
import messenger from './messenger';
import user from './user';
import storage from 'redux-persist/lib/storage';
import {persistReducer} from "redux-persist";

const rootPersistConfig = {
    key: 'root',
    storage: storage,
};

export default persistReducer(rootPersistConfig, combineReducers({
    account,
    blocker,
    contact,
    initial,
    messenger,
    user,
}));