import * as React from 'react';

import Input from '@material-ui/core/Input';
import { makeStyles } from '@material-ui/core/styles';
import ChatIcon from '@material-ui/icons/ChatOutlined';
import CloseIcon from '@material-ui/icons/CloseOutlined';
import SendIcon from '@material-ui/icons/SendOutlined';

import { CHAT_PLACEHOLDER } from '../../constants/chat';
import { DEFAULT_DRAGGABLE_CHAT_STYLE_CLASS, DEFAULT_DRAGGABLE_HANDLE } from '../../constants/draggable';
import { Draggable } from '../commons/draggable';
import { Flowable } from '../commons/flowable';
import { ChatBodyInterface, ChatInterface, DraggableChatInterface } from '../interfaces/chat';
import { MessageDialogue } from './messageDialogue';

const useStyles = makeStyles({
    root: {
        fontSize: '32px',
    },
});

function ChatBody({ styleClass }: ChatBodyInterface) {
    return (
        <div className={styleClass}>
            <div> chat side bar</div>
            <div>
                <Flowable>
                    <MessageDialogue round>
                        This one adds a right triangle on the left, flush at the top by using .tri-right and .left-top
                        to specify the location test.
                    </MessageDialogue>
                    <MessageDialogue round>
                        This one adds a right triangle on the left, flush at the top by using .tri-right and .left-top
                        to specify the location test.
                    </MessageDialogue>
                    <MessageDialogue round float={'right'}>
                        This one adds a right triangle on the left, flush at the top by using .tri-right and .left-top
                        to specify the location test.
                    </MessageDialogue>
                    <MessageDialogue round>Lol</MessageDialogue>

                    <MessageDialogue round>
                        This one adds a right triangle on the left, flush at the top by using .tri-right and .left-top
                        to specify the location test.
                    </MessageDialogue>
                    <MessageDialogue round>
                        This one adds a right triangle on the left, flush at the top by using .tri-right and .left-top
                        to specify the location test.
                    </MessageDialogue>
                    <MessageDialogue round>
                        This one adds a right triangle on the left, flush at the top by using .tri-right and .left-top
                        to specify the location test.
                    </MessageDialogue>
                    <MessageDialogue round>L</MessageDialogue>

                    <MessageDialogue round>
                        This one adds a right triangle on the left, flush at the top by using .tri-right and .left-top
                        to specify the location test.
                    </MessageDialogue>
                    <MessageDialogue round>
                        This one adds a right triangle on the left, flush at the top by using .tri-right and .left-top
                        to specify the location test.
                    </MessageDialogue>
                    <MessageDialogue round>
                        This one adds a right triangle on the left, flush at the top by using .tri-right and .left-top
                        to specify the location test.
                    </MessageDialogue>
                    <MessageDialogue round>Lol</MessageDialogue>

                    <MessageDialogue round>T</MessageDialogue>
                    <MessageDialogue round float={'right'}>
                        This one adds a right triangle on the left, flush at the top by using .tri-right and .left-top
                        to specify the location test.
                    </MessageDialogue>
                    <MessageDialogue round float={'right'}>
                        This one adds a right triangle on the left, flush at the top by using .tri-right and .left-top
                        to specify the location test.
                    </MessageDialogue>
                    <MessageDialogue round float={'right'}>
                        t
                    </MessageDialogue>
                </Flowable>
                <div className={`${styleClass}__message-send`}>
                    <Input autoFocus multiline disableUnderline placeholder={CHAT_PLACEHOLDER} />
                    <SendIcon />
                </div>
            </div>
        </div>
    );
}

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
