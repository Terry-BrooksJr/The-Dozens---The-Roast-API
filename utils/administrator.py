
from database.models import Insult, User


class Administrator:
    @staticmethod
    def count_user_and_jokes():
        return tuple(Insult.objects().count(), User.objects().count())