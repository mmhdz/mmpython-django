import re


class Helper:

    @staticmethod
    def modify_hashtag_raw_string(hashtags_string: str):
        hashtags = hashtags_string.replace(" ", ",").split(",")

        return [x for x in hashtags if len(x) > 0]
