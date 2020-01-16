import { useSnackbar, withSnackbar } from 'notistack';
import { useState } from 'react';
import * as React from 'react';
import { useMutation } from 'react-apollo-hooks';
import { Redirect, Route, Switch } from 'react-router-dom';
import { validate } from 'validate.js';
import { CREATE_USER_MUTATION, LOGIN_USER_MUTATION } from '../../graphql/mutations/authentication';
import { deepCopy, renderElement } from '../../utils/utils';
import { Footer } from '../commons/footer';
import { NavBarContainer } from '../commons/navbarContainer';
import { closeAction } from '../commons/snackBarActions';
import { EventInterface } from '../interfaces/interfaces';
import { createUserConstraints, userLogInConstraints } from '../validators/authentication';
import SignIn from './signin';
import SignUp from './signup';

const footerClass: string = 'main-footer';

function SignInSignUpContainer() {
    const preventDefault = (event: any) => event.preventDefault();
    const { enqueueSnackbar, closeSnackbar } = useSnackbar();
    // eslint-disable-next-line
    const [logInUserFunction, setLogInUserFunction] = useMutation(LOGIN_USER_MUTATION);
    // eslint-disable-next-line
    const [createUserFunction, setCreateUserFunction] = useMutation(CREATE_USER_MUTATION);
    const [userInfo, setUserInfo] = useState(userInfoInitialState);
    const [userErrors, setUserErrors] = useState({});

    function userInfoInitialState() {
        return {
            email: '',
            firstName: '',
            lastName: '',
            password: '',
            pictureUrl: '',
            preferredName: '',
            telephone: '',
        };
    }

    function validateUserInputs(userInputs: object, constraints: object, fullMessages: boolean = false) {
        return validate(userInputs, constraints, { fullMessages });
    }

    function onTextFieldChange(constraints: object) {
        return function(key: string) {
            return function(event: EventInterface) {
                preventDefault(event);

                const updatedUserInfo = deepCopy(userInfo);
                updatedUserInfo[key] = event.target.value;
                const errors = validateUserInputs(updatedUserInfo, constraints);
                setUserErrors(errors || {});
                setUserInfo(updatedUserInfo);
            };
        };
    }

    async function logInUser(event: EventInterface) {
        preventDefault(event);

        const errors = validateUserInputs(userInfo, userLogInConstraints);

        if (!!errors) {
            setUserErrors(errors || {});
            return;
        }

        await logInUserFunction({
            variables: {
                email: userInfo.email,
                password: userInfo.password,
            },
        })
            .then(() => {
                enqueueSnackbar('successful', { variant: 'success' });
            })
            .catch((response: any) => {
                enqueueSnackbar(response.graphQLErrors[0].message, {
                    variant: 'error',
                    persist: true,
                    action: closeAction(closeSnackbar),
                });
            });
    }

    async function createUser(event: EventInterface) {
        preventDefault(event);

        const errors = validateUserInputs(userInfo, createUserConstraints);

        if (!!errors) {
            setUserErrors(errors || {});
            return;
        }

        await createUserFunction({
            variables: {
                firstName: userInfo.firstName,
                lastName: userInfo.lastName,
                email: userInfo.email,
                password: userInfo.password,
            },
        })
            .then(() => {
                enqueueSnackbar('successful signup', { variant: 'success' });
            })
            .catch((response: any) => {
                enqueueSnackbar(response.graphQLErrors[0].message, {
                    variant: 'error',
                    persist: true,
                    action: closeAction(closeSnackbar),
                });
            });
    }

    return (
        <React.Fragment>
            <NavBarContainer styleClass={'default-navbar-container'} />
            <div className={'default-nav-strip'} />
            <div className={'content'}>
                <Switch>
                    <Route
                        exact
                        path="/u/signin/"
                        render={renderElement(
                            <SignIn
                                loginUser={logInUser}
                                userInfo={userInfo}
                                onTextFieldChange={onTextFieldChange(userLogInConstraints)}
                                userErrors={userErrors}
                            />
                        )}
                    />
                    <Route
                        exact
                        path="/u/signup/"
                        render={renderElement(
                            <SignUp
                                createUser={createUser}
                                userInfo={userInfo}
                                onTextFieldChange={onTextFieldChange(createUserConstraints)}
                                userErrors={userErrors}
                            />
                        )}
                    />
                    <Redirect to="/u/signin/" />
                </Switch>
            </div>
            <Footer footerClass={footerClass} key={'sudoku-footer'} />
        </React.Fragment>
    );
}

export default withSnackbar(SignInSignUpContainer);
