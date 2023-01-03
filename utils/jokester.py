"""
This Module is responsible for all the actions that occur in the /insults endpoint, and the functions that are called by the /insults routes.
"""

import random

from database.models import Insult


class Jokester:
    @staticmethod
    def get_random_joke():
        randomized_pipeline = [{"$sample": {"size": 1}}]
        randomized_joke = str()
        insult = Insult.objects().aggregate(randomized_pipeline)
        for doc in insult:
            randomized_joke = doc['content']
        return randomized_joke

    @staticmethod
    def get_censored_joke():
        censored_pipeline = [{"$match": {"explicit": False}}, {"$sample": {"size": 1}}]
        censored_joke = str()
        insult = Insult.objects().aggregate(censored_pipeline)
        for doc in insult:
            if doc["status"] == "Active":
                censored_joke = doc['content']

            else:
                Jokester.get_censored_joke()
        return censored_joke

    @staticmethod
    def get_categorized_joke(catagory_selection, explicit_settings):
        pipeline_step1 = {"$match": {"explicit": explicit_settings}}
        pipeline_step2 = {"$match": {"catagory": catagory_selection}}
        catagorized_pipeline = [pipeline_step1, pipeline_step2]
        catagorized_joke = str()
        insult = Insult.objects().aggregate(catagorized_pipeline)
        randomizer = random.randint(0, len(insult))
        for doc in insult:
            if doc[randomizer]["status"] == "Active":
                catagorized_joke = doc[randomizer]["content"]
            else:
                Jokester.get_categorized_joke()
        return catagorized_joke

    @staticmethod
    def get_catagories():
        catagories = Insult.objects()
        # print(dir(catagories))
        # catagories.distinct("catagory")
        catagory_list = list()

        for cat in catagories:
            if cat['category'] not in catagory_list:
                catagory_list.append(cat['category'])

        return catagory_list

