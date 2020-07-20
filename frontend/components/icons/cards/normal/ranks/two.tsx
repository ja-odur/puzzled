import * as React from 'react';

import { CardInterface } from '../../../../interfaces/card';

function Two({ value }: CardInterface) {
    return (
        <>
            <use xlinkHref={`#V${value}`} height="32" x="-112.4" y="-154" />
            <use xlinkHref={`#S${value}`} height="26.769" x="-109.784" y="-117" />
            <use xlinkHref={`#S${value}`} height="65" x="-32.5" y="-133.084" />
            <g transform="rotate(180)">
                <use xlinkHref={`#V${value}`} height="32" x="-112.4" y="-154" />
                <use xlinkHref={`#S${value}`} height="26.769" x="-109.784" y="-117" />
                <use xlinkHref={`#S${value}`} height="65" x="-32.5" y="-133.084" />
            </g>
        </>
    );
}

export { Two };
