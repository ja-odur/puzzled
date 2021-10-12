import * as React from 'react';
import { useMutation } from 'react-apollo-hooks';
import { useDispatch } from 'react-redux';
import { Link, useHistory } from 'react-router-dom';

import Collapse from '@material-ui/core/Collapse';
import SigninIcon from '@material-ui/icons/AccountCircle';
import LogoutIcon from '@material-ui/icons/ExitToApp';
import MenuIcon from '@material-ui/icons/Menu';
import ProfileIcon from '@material-ui/icons/PersonOutline';

import { LOGOUT_MUTATION } from '../../graphql/mutations/authentication';
import { loadCurrentUser } from '../../state/userProfile';
import { ElementInterface, EventInterface, LinksInterface } from '../interfaces/interfaces';
import { DropdownInterface } from '../interfaces/navbar';
import { NavBarProfileAvatar } from './avatar';
import { ULItems } from './links';
import { links } from './linkUrls';
import { useCheckLoginContext } from './puzzleContext';

const ProfileDropdown = ({ toggleDropdown }: DropdownInterface) => {
    const history = useHistory();
    // eslint-disable-next-line
    const [logoutUserFunc, setLogoutUserFunc] = useMutation(LOGOUT_MUTATION);
    const { asyncUpdateLoginInfo } = useCheckLoginContext();
    const dispatch = useDispatch();

    function gotoProfile() {
        toggleDropdown();
        history.push(links.USER.PROFILE.HOME);
    }

    async function logout(event: EventInterface) {
        event.preventDefault();

        await logoutUserFunc().then(async () => {
            await dispatch(loadCurrentUser());
            await asyncUpdateLoginInfo(() => {});
        });

        history.push(links.HOME);
    }
    return (
        <div>
            <span onClick={gotoProfile}>
                <ProfileIcon /> profile
            </span>
            <span onClick={logout}>
                <LogoutIcon /> logout
            </span>
        </div>
    );
};

const AnonymousUserDropdown = ({ toggleDropdown }: DropdownInterface) => {
    return (
        <div>
            <Link to={links.USER.SIGN_IN} onClick={toggleDropdown}>
                <span>
                    <SigninIcon /> Sign In
                </span>
            </Link>
            <Link to={links.USER.SIGN_UP} onClick={toggleDropdown}>
                <span>
                    <SigninIcon /> Sign Up
                </span>
            </Link>
        </div>
    );
};

function NavDropDownMin({ className }: ElementInterface) {
    const { checkLogin } = useCheckLoginContext();
    const [showDropdown, setShowDropdown] = React.useState(false);

    function toggleDropdown() {
        setShowDropdown(!showDropdown);
    }

    return (
        <div className={className}>
            <MenuIcon onClick={toggleDropdown} />
            <Collapse className={'c-dropdown dropdown'} in={showDropdown} timeout="auto" unmountOnExit>
                {checkLogin._loginInfo.loggedIn ? (
                    <ProfileDropdown toggleDropdown={toggleDropdown} />
                ) : (
                    <AnonymousUserDropdown toggleDropdown={toggleDropdown} />
                )}
            </Collapse>
        </div>
    );
}

function NavBarDropDown({ activeClass, onTabClick, links, className }: LinksInterface) {
    const { checkLogin } = useCheckLoginContext();
    return (
        <div className={className}>
            {checkLogin._loginInfo.loggedIn ? (
                <NavBarProfileAvatar profileName={checkLogin._loginInfo.user.name} />
            ) : (
                <ULItems activeClass={activeClass} links={links} onTabClick={onTabClick} />
            )}
        </div>
    );
}

export { NavDropDownMin, NavBarDropDown };
