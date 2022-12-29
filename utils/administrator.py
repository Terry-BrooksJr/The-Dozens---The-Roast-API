from database.models import Insult, User





class Administrator:
    @staticmethod
    def count_insults():
        return Insult.objects().count()

