from backend.services.redis import RedisStream
from backend.poker.persister import PokerGamePersist
from backend.poker.game_logic.poker_room import PokerRoom

poker_room_streams = RedisStream(name_prefix='poker:room:')


class PokerGame:
    def __init__(self, *args, room_id=None, **kwargs):
        """
        Args:
            *args (tuple): a tuple with the following positional values;
                poker_type (str): string representing the type of hand --such as Omaha, being played in the room.
                small_blind (int): forced bet placed by the player to the immediate left of the dealer
                big_blind (int): forced bet placed by the player to the immediate left of the small blind
                players (tuple): a tuple of poker players on the room
                name (str): name of the room
                from_deck (list): a nested list of cards and banned cards that can be used to recreate a card deck
                deck_size (int): an integer representing the size of deck e.g 1 = single deck, 2 = double deck, etc.
                dealer (int): if set, represents the position of the dealer
            **kwargs (dict): dict with the following key/values;
                players (tuple): a tuple of poker players on the room
                name (str): name of the room
                from_deck (list): a nested list of cards and banned cards that can be used to recreate a card deck
                deck_size (int): an integer representing the size of deck e.g 1 = single deck, 2 = double deck, etc.
                dealer (int): if set, represents the position of the dealer
        """

        if room_id:
            room = poker_room_streams.latest(room_id)
            if not room:
                raise Exception('Poker room not found')
            self.room = room[0].get('room')
        else:
            self.room = self.new_room(*args, **kwargs)

    def redis_stream_push(self):
        """Push game to redis stream"""
        poker_room_streams.add(self.room.poker_room, {'room': self.room})

    @classmethod
    def new_room(cls, poker_type, small_blind, big_blind, players=(),
                 name=None, from_deck=None, deck_size=1, dealer=None):
        """constructor for creating new room
        Args:
            poker_type (str): string representing the type of hand --such as Omaha, being played in the room.
            small_blind (int): forced bet placed by the player to the immediate left of the dealer
            big_blind (int): forced bet placed by the player to the immediate left of the small blind
            players (tuple): a tuple of poker players on the room
            name (str): name of the room
            from_deck (list): a nested list of cards and banned cards that can be used to recreate a card deck
            deck_size (int): an integer representing the size of deck e.g 1 = single deck, 2 = double deck, etc.
            dealer (int): if set, represents the position of the dealer
        """
        new_room = PokerGamePersist.new_room(poker_type, small_blind, big_blind, players=players, name=name)
        return PokerRoom(new_room.id, poker_type, small_blind, big_blind, players, name, from_deck, deck_size, dealer)

    def join_room(self):
        pass

    def leave_room(self):
        pass

    def invite(self):
        pass

    @classmethod
    def add_player(cls, room_id, user_id):
        return PokerGamePersist.add_player(room_id=room_id, user_id=user_id)
