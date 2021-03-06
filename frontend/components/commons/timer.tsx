import * as React from 'react';
import { modulus, pad } from '../../utils/utils';
import { PauseIcon, PlayIcon } from '../icons/sudoku';
import { TimerInterface } from '../interfaces/interfaces';

const minute: number = 60; // 60 seconds
const hour: number = minute * 60;

function Timer({ playing, playControl, styleClass, totalSeconds, onClick, stopTimer }: TimerInterface) {
    function setClickFunction() {
        return stopTimer || !playControl ? () => {} : onClick;
    }

    function setStyleClass() {
        return stopTimer || !playControl ? `${styleClass}__svg__disabled` : `${styleClass}__svg`;
    }

    function loadIcon() {
        if (!stopTimer && playing) {
            return <PauseIcon onClick={setClickFunction()} width={'25'} styleClass={setStyleClass()} />;
        }

        return <PlayIcon onClick={setClickFunction()} width={'25'} styleClass={setStyleClass()} />;
    }

    function parseSeconds(totalSeconds: number) {
        const hours = Math.floor(totalSeconds / hour);
        const minutes = Math.floor(modulus(totalSeconds, hour) / minute);
        const seconds = modulus(modulus(totalSeconds, hour), minute);

        if (hours) {
            return `${pad(hours, (length = 2))}:${pad(minutes, (length = 2))}:${pad(seconds, (length = 2))}`;
        }

        if (minutes) {
            return `${pad(minutes, (length = 2))}:${pad(seconds, (length = 2))}`;
        }
        return `${pad(seconds, (length = 2))}`;
    }

    return (
        <div className={styleClass}>
            <span className={`${styleClass}__span`}>{parseSeconds(totalSeconds)}</span>
            {loadIcon()}
        </div>
    );
}

export { Timer };
