from typing import List


def filter_first_10_hashtags(hashtags: List[str]):
    return [x for x in hashtags if len(x) > 0][:10]
