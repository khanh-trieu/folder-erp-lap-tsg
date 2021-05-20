import {applyMiddleware, createStore} from "redux";
import rootReducer from './redux/reducers';
import {composeWithDevTools} from "redux-devtools-extension";
import reduxMiddleware from 'react-block-ui/lib/reduxMiddleware';
import thunk from "redux-thunk";
import {persistStore} from "redux-persist";

const middleware = [thunk, reduxMiddleware];

export const store = createStore(rootReducer, {}, composeWithDevTools(applyMiddleware(...middleware)));
export const persistor = persistStore(store);
