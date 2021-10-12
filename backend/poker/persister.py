from .models import PokerHand, PokerRoom


class PokerGamePersist:

    def __init__(self, poker_type, small_blind, big_blind, players=(), dealer=0, name=None, current_hand=None, id=None):
        self.id = id
        self.type = poker_type
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.players = players
        self.name = name
        self.dealer = dealer
        self.current_hand = current_hand

    @classmethod
    def new_room(cls, poker_type, small_blind, big_blind, players=(), name=None, current_hand=None):

        """constructor for creating new room
         Args:
            poker_type (str): string representing the type of hand --such as Omaha, being played in the room.
            small_blind (int): forced bet placed by the player to the immediate left of the dealer
            big_blind (int): forced bet placed by the player to the immediate left of the small blind
            players (tuple): a tuple of poker players on the room
            name (str): name of the room
        """
        player_ids = [player.user for player in players]
        room = PokerRoom(name=name, type=poker_type, small_blind=small_blind, big_blind=big_blind)
        room.save()
        room.players.set(player_ids)
        return cls(
            poker_type,
            small_blind,
            big_blind,
            players=players,
            name=name,
            current_hand=current_hand,
            id=room.id
        )

    def save(self):
        room = PokerRoom.objects.get(id=self.id)
        if self.current_hand:
            hand = PokerHand(
                poker_room=room,
                deck=self._stringify_cards(self.current_hand.deck),
                deck_size=self.current_hand.deck_size,
                last_round=self.current_hand.state.round.value,
                pot_size=self.current_hand.pot.size,
                community_cards=self._stringify_cards(self.current_hand.community_cards),
                banned_cards=self._stringify_cards(self.current_hand.banned_cards),

                dealer=self.dealer
            )
            hand.save()
            hand.players.set(self.current_hand.players)

    @classmethod
    def add_player(cls, room_id, user_id):
        return PokerRoom.objects.add_player(room_id=room_id, user_id=user_id)

    @staticmethod
    def _stringify_cards(cards):
        return ' '.join(card.raw_value for card in cards)
