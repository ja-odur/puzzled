import * as React from 'react';

import { LinkInterface, LinksInterface } from '../interfaces/interfaces';
import { NavBarDropDown, NavDropDownMin } from './Dropdown';
import { ULItems } from './links';
import { links as urlLinks } from './linkUrls';
import { Logo } from './logo';

const sudokuImage = require('../../images/sudoku-dark.jpg');

function NavUL() {
    return (
        <div className={'nav-ul'}>
            <img className={'nav-img'} src={sudokuImage} alt={'sudoku-nav-image'} />
            <img className={'nav-img'} src={sudokuImage} alt={'sudoku-nav-image'} />
            <img className={'nav-img'} src={sudokuImage} alt={'sudoku-nav-image'} />
            <img className={'nav-img'} src={sudokuImage} alt={'sudoku-nav-image'} />
            <img className={'nav-img'} src={sudokuImage} alt={'sudoku-nav-image'} />
        </div>
    );
}

function NavMenu({ className, activeClass, links }: LinksInterface) {
    return (
        <div className={'nav-ul'}>
            <ULItems className={className || 'nav-menu-li'} activeClass={activeClass || 'nav-active'} links={links} />
        </div>
    );
}

function NavBar({ className, activeClass, links, style }: LinksInterface) {
    const signUpSignInLinks: LinkInterface[] = [
        { name: 'Sign In', href: urlLinks.USER.SIGN_IN },
        { name: 'Sign Up', href: urlLinks.USER.SIGN_UP },
    ];

    return (
        <nav style={style || {}}>
            <Logo />
            {!!links ? <NavMenu className={className} activeClass={activeClass} links={links} /> : <NavUL />}
            <NavDropDownMin className={'min-dropdown h-dropdown'} />
            <NavBarDropDown
                activeClass={''}
                links={signUpSignInLinks}
                className={'h-dropdown nav-profile full-dropdown'}
            />
        </nav>
    );
}

export { NavBar };
