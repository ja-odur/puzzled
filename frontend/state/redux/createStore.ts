import { applyMiddleware, createStore } from 'redux';
import { composeWithDevTools } from 'redux-devtools-extension';
import reduxImmutableStateInvariant from 'redux-immutable-state-invariant';
import thunk from 'redux-thunk';

import rootReducer from './reducers';

const initialState = {};

export default function configureReduxStore() {
    const middleware: any[] = [thunk];

    // Be sure to ONLY add these middlewares in development!
    if (process.env.NODE_ENV !== 'production') {
        middleware.unshift(reduxImmutableStateInvariant());
    }

    const middlewareEnhancer = applyMiddleware(...middleware);
    const storeEnhancer = composeWithDevTools(middlewareEnhancer);
    const store = createStore(rootReducer, initialState, storeEnhancer);

    return store;
}
