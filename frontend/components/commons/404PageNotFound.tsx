import * as React from 'react';
import { Footer } from './footer';
import { TextLink } from './links';
import { NavBarContainer } from './navbarContainer';

const pageNotFoundContentClass: string = 'content-container-404';
const footerClass: string = 'footer-404';

function PageNotFound() {
    return (
        <React.Fragment>
            <NavBarContainer style={{ backgroundColor: 'black' }}/>
            <div className={pageNotFoundContentClass}>
                <div className={`${pageNotFoundContentClass}__main`}>404</div>
                <div className={`${pageNotFoundContentClass}__sub`}>You have reached the end of the universe...</div>
                <div className={`${pageNotFoundContentClass}__sub`}>
                    though you can still revisit planet{' '}
                    <TextLink text={'Puzzled'} link={'/'} styleClass={'link__emphasized'} />
                </div>
            </div>
            <Footer className={footerClass} />
        </React.Fragment>
    );
}

export { PageNotFound };
