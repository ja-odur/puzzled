import * as React from 'react';
import { EraseIcon } from '../icons/sudoku';
import { NumPadInterface, NumPadRowInterface } from '../interfaces';
import {Timer} from "../commons/timer";

function NumPadRow({ gridClass, type, startNum, onPadClick }: NumPadRowInterface) {
    function CreateNumPadData(num: number, fillValue: number) {
        const cells = [];
        for (let i = 0; i < num; i++) {
            cells.push(
                <td onClick={onPadClick} data-value={fillValue} key={`sudoku-numpad-td-${fillValue}`}>
                    {fillValue}
                </td>
            );
            fillValue += 1;
        }

        return cells.map(cell => cell);
    }

    return <tr className={`${gridClass}__grid_wrapper__numpad_row`}>{CreateNumPadData(type, startNum)}</tr>;
}

function NumberPad({ gridClass, type, onPadClick, onTimerClick, playing, stopTimer, timerStyleClass, totalSeconds }: NumPadInterface) {
    function CreateNumPadRow(type: number, startNum: number) {
        const cells = [];
        for (let i = 0; i < type; i++) {
            cells.push(
                <NumPadRow
                    onPadClick={onPadClick}
                    gridClass={gridClass}
                    type={type}
                    startNum={startNum}
                    key={`sudoku-numpad-row-${startNum}`}
                />
            );
            startNum += type;
        }

        return cells.map(cell => cell);
    }

    return (
        <table className={`${gridClass}__grid_wrapper__numpad`}>
            <tbody>
                <tr className={`${gridClass}__grid_wrapper__numpad_row`}>
                    <div>
                        <Timer
                            stopTimer={stopTimer}
                            onClick={onTimerClick}
                            playing={playing}
                            styleClass={timerStyleClass}
                            totalSeconds={totalSeconds}
                        />
                    </div>
                </tr>
                {CreateNumPadRow(type, 1)}
                <tr className={`${gridClass}__grid_wrapper__numpad_row`}>
                    <td onClick={onPadClick} data-value={0}>
                        <EraseIcon width={'30'} />
                        &nbsp;erase
                    </td>
                </tr>
            </tbody>
        </table>
    );
}

export { NumberPad };
