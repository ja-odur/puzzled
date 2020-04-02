import * as React from 'react';

import { makeStyles } from '@material-ui/core/styles';
import ChatIcon from '@material-ui/icons/ChatOutlined';
import CloseIcon from '@material-ui/icons/CloseOutlined';

import { Draggable } from '../commons/draggable';
import { ChatBodyInterface, ChatInterface, DraggableChatInterface } from '../interfaces/chat';
import { DEFAULT_DRAGGABLE_CHAT_STYLE_CLASS, DEFAULT_DRAGGABLE_HANDLE } from "../../constants/draggable";
import { CHAT_PLACEHOLDER } from "../../constants/chat";

const useStyles = makeStyles({
    root: {
        fontSize: '32px',
    },
});

function Chat({ styleClass }: ChatInterface) {
    const classes = useStyles({});
    return (
        <div className={styleClass || DEFAULT_DRAGGABLE_CHAT_STYLE_CLASS}>
            <div className={DEFAULT_DRAGGABLE_HANDLE.CLASSNAME}>
                <span>
                    <ChatIcon className={classes.root} />
                    <span>chat</span>
                    <CloseIcon className={classes.root} />
                </span>
            </div>
            <ChatBody styleClass={`${DEFAULT_DRAGGABLE_CHAT_STYLE_CLASS}__chat_body`} />
        </div>
    );
}

function DraggableChat({  }: DraggableChatInterface) {
    return (
        <Draggable scale={1}>
            <Chat />
        </Draggable>
    );
}

export { Chat, DraggableChat };
