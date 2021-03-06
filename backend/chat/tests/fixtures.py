from django.contrib.auth import get_user_model
import faker
import pytest

from backend.chat.models import Message, ChatChannel

FAKE = faker.Faker()


@pytest.fixture(scope='module')
def user():
    return get_user_model()(
        name=FAKE.first_name(),
        preferred_name=FAKE.first_name(),
        email=FAKE.email()
    )


@pytest.fixture(scope='module')
def channel():
    return ChatChannel(
        room_id='djfhkf,mnskjnsllksfklnfdluns',
        name='testname',
        type='Private'
    )


@pytest.fixture(scope='module')
def message(user):
    return Message(
        user=user,
        message=FAKE.sentence()
    )


def create_direct_chat_mutation(user_id1, user_id2, name="channelTestName"):
    return (
        f'''
        mutation {{
                createOrGetDirectChat(name: "{name}", userIds: ["{user_id1}", "{user_id2}"]) {{
                    chatChannel {{
                        id
                        roomId
                        name
                        latestMessage {{
                            id
                            message
                        }}
                        users {{
                            id
                            name
                        }}
                        messages {{
                            createdAt
                            updatedAt
                            id
                            message
                            float
                            user {{
                                id
                                name
                            }}
                        }}
                    }}
                }}
            }}
        '''
    )


def create_multi_user_chat_mutation(name, chat_type, user_ids):
    return (
        f'''
        mutation {{
        createOrGetMultiUserChat(name: "{name}", chatType: "{chat_type}", userIds: ["{user_ids[0]}", "{user_ids[1]}"])
            {{
                chatChannel {{
                    id
                    roomId
                    name
                    users {{
                        id
                        name
                    }}
                    messages {{
                        createdAt
                        updatedAt
                        id
                        message
                        float
                        user {{
                            id
                            name
                        }}
                    }}
                }}
            }}
        }}
        '''
    )


def add_message_mutation(channel_id, message):
    return (
        f'''
        mutation {{
        addMessage(channelId: "{channel_id}", message: "{message}") {{
            chatMessage {{
                id
                createdAt
                updatedAt
                message
                float
                user {{
                    id
                    name
                    preferredName
                }}
            }}
        }}
    }}
    '''
    )


def edit_message_mutation(message_id, message):
    return (
        f'''
        mutation {{
        editMessage(messageId: "{message_id}", message: "{message}") {{
            chatMessage {{
                id
                createdAt
                updatedAt
                message
                float
                user {{
                    id
                    name
                    preferredName
                }}
            }}
        }}
    }}
    '''
    )
