import graphene
from backend.authentication.schema import UserMutation, UserQuery
from backend.chat.schema import ChatMutations, ChatSubscriptions
from backend.gem.schema import GemQuery
from backend.poker.schema import PokerMutations, PokerSubscriptions
from backend.sudoku.schema import SudokuMutation, SudokuQuery


class Mutation(UserMutation, SudokuMutation, PokerMutations, ChatMutations, graphene.ObjectType):
    pass


class Query(UserQuery, SudokuQuery, GemQuery, graphene.ObjectType):
    pass


class Subscription(PokerSubscriptions, ChatSubscriptions, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
