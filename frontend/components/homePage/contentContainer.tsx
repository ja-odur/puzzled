import * as React from 'react';

import { GameCard, GameCards } from '../commons/cards';
import { links } from '../commons/linkUrls';
import { MainContent } from '../commons/mainContent';
import { ElementInterface } from '../interfaces/interfaces';

const sd = require('../../images/sudoku-dark.jpg');
const gif1 = 'https://media.giphy.com/media/10SvWCbt1ytWCc/giphy.gif';
const gif2 = 'https://media.giphy.com/media/LwIyvaNcnzsD6/giphy.gif';

function GamesIntro({ className }: ElementInterface) {
    return (
        <div className={className || ''}>
            <h1>let&apos;s play.</h1>
            <div>play your favourite games right here at Puzzled</div>
        </div>
    );
}

function ContentContainer() {
    return (
        <React.Fragment>
            <GamesIntro className={'game-intro'} />
            <MainContent>
                <GameCards>
                    <GameCard name={'sudoku'} desc={''} src={sd} link={links.SUDOKU.HOME} />
                    <GameCard name={'sudoku'} desc={''} src={sd} link={links.SUDOKU.HOME} />
                    <GameCard name={'sudoku'} desc={''} src={sd} link={links.SUDOKU.HOME} />
                    <GameCard name={'sudoku'} desc={''} src={sd} link={links.SUDOKU.HOME} />
                    <GameCard name={'sudoku'} desc={''} src={sd} link={links.SUDOKU.HOME} />
                    <GameCard name={'sudoku'} desc={''} src={sd} link={links.SUDOKU.HOME} />
                    <GameCard name={'sudoku'} desc={''} src={sd} link={links.SUDOKU.HOME} />
                    <GameCard name={'sudoku'} desc={''} src={sd} link={links.SUDOKU.HOME} />
                    <GameCard name={'sudoku'} desc={''} src={gif1} link={links.SUDOKU.HOME} />
                    <GameCard name={'sudoku'} desc={''} src={gif2} link={links.SUDOKU.HOME} />
                    <GameCard name={'sudoku'} desc={''} src={gif1} link={links.SUDOKU.HOME} />
                    <GameCard name={'sudoku'} desc={''} src={gif2} link={links.SUDOKU.HOME} />
                    <GameCard name={'sudoku'} desc={''} src={sd} link={links.SUDOKU.HOME} />
                    <GameCard name={'sudoku'} desc={''} src={sd} link={links.SUDOKU.HOME} />
                    <GameCard name={'sudoku'} desc={''} src={sd} link={links.SUDOKU.HOME} />
                    <GameCard name={'sudoku'} desc={''} src={gif1} link={links.SUDOKU.HOME} />
                    <GameCard name={'sudoku'} desc={''} src={gif2} link={links.SUDOKU.HOME} />
                    <GameCard name={'sudoku'} desc={''} src={gif1} link={links.SUDOKU.HOME} />
                    <GameCard name={'sudoku'} desc={''} src={gif2} link={links.SUDOKU.HOME} />
                </GameCards>
            </MainContent>
        </React.Fragment>
    );
}

export { ContentContainer };
