from database.models import Insult

class Jokester():
    @staticmethod
    def get_random_joke():
            randomized_pipeline = [{"$sample": {"size": 1}}]
            randomized_joke = str()
            insult = Insult.objects().aggregate(randomized_pipeline)
            for doc in insult:
                if doc["status"] == "Active":
                    randomized_joke = doc["content"]
                else:
                    get_random_joke()
            return randomized_joke
    
    @staticmethod
    def get_censored_joke():
        censored_pipeline = [{'$match':{"nsfw":False}},]
        censored_joke = str()
        insult = Insult.objects().aggregate(censored_pipeline)
        for doc in insult:
                if doc["status"] == "Active":
                    censored_joke = doc["content"]
                else:
                    get_censored_joke()
        return censored_joke
    
    @staticmethod
    def get_categorized_joke(catagory):
        pass