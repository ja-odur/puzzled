import * as React from 'react';

import { Footer } from '../commons/footer';
import { links } from '../commons/linkUrls';
import { NavBarContainer } from '../commons/navbarContainer';
import { SudokuGrid } from './sudokuGrid';

const sudokuLinks = [
    { name: 'Play', href: links.SUDOKU.PLAY },
    { name: 'Solve', href: links.SUDOKU.SOLVE },
    { name: 'Trainer', href: links.SUDOKU.TRAINER },
    { name: 'Help', href: '#' },
];

function SudokuHome() {
    return (
        <React.Fragment>
            <NavBarContainer links={sudokuLinks} />
            <div className={'main-content'}>
                <SudokuGrid key={'sudokuGrid'} />
            </div>
            <Footer key={'sudoku-footer'} />
        </React.Fragment>
    );
}

export { SudokuHome };
