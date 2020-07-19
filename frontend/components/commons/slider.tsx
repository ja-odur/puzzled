import * as React from 'react';

import Input from '@material-ui/core/Input';
import Slider from '@material-ui/core/Slider';
import { makeStyles, withStyles } from '@material-ui/core/styles';
import Tooltip from '@material-ui/core/Tooltip';

import { SliderInterface } from '../interfaces/slider';

const useStyles = makeStyles({
    root: {
        width: 250,
    },
    input: {
        width: '20%',
    },
    slider: {
        width: '70%',
    },
});

interface Props {
    children: React.ReactElement;
    open: boolean;
    value: number;
}

function ValueLabelComponent(props: Props) {
    const { children, open, value } = props;

    return (
        <Tooltip open={open} enterTouchDelay={0} placement="top" title={value}>
            {children}
        </Tooltip>
    );
}

const iOSBoxShadow = '0 3px 1px rgba(0,0,0,0.1),0 4px 8px rgba(0,0,0,0.13),0 0 0 1px rgba(0,0,0,0.02)';

const IOSSlider = withStyles({
    root: {
        color: '#3880ff',
        height: 2,
        padding: '15px 0',
    },
    thumb: {
        height: 28,
        width: 28,
        backgroundColor: '#fff',
        boxShadow: iOSBoxShadow,
        marginTop: -14,
        marginLeft: -14,
        '&:focus, &:hover, &$active': {
            boxShadow: '0 3px 1px rgba(0,0,0,0.1),0 4px 8px rgba(0,0,0,0.3),0 0 0 1px rgba(0,0,0,0.02)',
            // Reset on touch devices, it doesn't add specificity
            '@media (hover: none)': {
                boxShadow: iOSBoxShadow,
            },
        },
    },
    active: {},
    valueLabel: {
        left: 'calc(-50% + 12px)',
        top: -22,
        '& *': {
            background: 'transparent',
            color: '#000',
        },
    },
    track: {
        height: 2,
    },
    rail: {
        height: 2,
        opacity: 0.5,
        backgroundColor: '#bfbfbf',
    },
    mark: {
        backgroundColor: '#bfbfbf',
        height: 8,
        width: 1,
        marginTop: -3,
    },
    markActive: {
        opacity: 1,
        backgroundColor: 'currentColor',
    },
})(Slider);

const PrettoSlider = withStyles({
    root: {
        color: '#52af77',
        height: 8,
    },
    thumb: {
        height: 24,
        width: 24,
        backgroundColor: '#fff',
        border: '2px solid currentColor',
        marginTop: -8,
        marginLeft: -12,
        '&:focus, &:hover, &$active': {
            boxShadow: 'inherit',
        },
    },
    active: {},
    valueLabel: {
        left: 'calc(-50% + 4px)',
    },
    track: {
        height: 8,
        borderRadius: 4,
    },
    rail: {
        height: 8,
        borderRadius: 4,
    },
})(Slider);

const AirbnbSlider = withStyles({
    root: {
        color: '#3a8589',
        height: 3,
        padding: '13px 0',
    },
    thumb: {
        height: 27,
        width: 27,
        backgroundColor: '#fff',
        border: '1px solid currentColor',
        marginTop: -12,
        marginLeft: -13,
        boxShadow: '#ebebeb 0 2px 2px',
        '&:focus, &:hover, &$active': {
            boxShadow: '#ccc 0 2px 3px 1px',
        },
        '& .bar': {
            // display: inline-block !important;
            height: 9,
            width: 1,
            backgroundColor: 'currentColor',
            marginLeft: 1,
            marginRight: 1,
        },
    },
    active: {},
    track: {
        height: 3,
    },
    rail: {
        color: '#d8d8d8',
        opacity: 1,
        height: 3,
    },
})(Slider);

function AirbnbThumbComponent(props: any) {
    return (
        <span {...props}>
            <span className="bar" />
            <span className="bar" />
            <span className="bar" />
        </span>
    );
}

function PrettoInputSlider({ value, min, max, step = 1, marks = [] }: SliderInterface) {
    const classes = useStyles();
    const [internalVal, setInternalVal] = React.useState(value);

    const handleSliderChange = (event: any, newValue: number) => {
        setInternalVal(newValue);
    };

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        let value: number = event.target.value === '' ? min : Number(event.target.value);
        if (value < min) {
            value = min;
        } else if (value > max) {
            value = max;
        }
        setInternalVal(value);
    };

    return (
        <div className={'pretto-slider'}>
            <PrettoSlider
                className={classes.slider}
                value={internalVal}
                valueLabelDisplay="auto"
                aria-label="pretto slider"
                min={min}
                max={max}
                step={step}
                marks={marks}
                onChange={handleSliderChange}
            />
            <Input
                className={classes.input}
                value={internalVal}
                margin="dense"
                onChange={handleInputChange}
                inputProps={{
                    step,
                    min,
                    max,
                    type: 'number',
                    'aria-labelledby': 'input-slider',
                    style: { textAlign: 'center' },
                }}
            />
        </div>
    );
}

export { IOSSlider, AirbnbSlider, PrettoSlider, PrettoInputSlider, ValueLabelComponent, AirbnbThumbComponent };
