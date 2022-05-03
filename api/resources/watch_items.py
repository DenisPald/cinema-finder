from data._all_models import *
from resources.base import BaseListResource, BaseResource


class WatchListItemResource(BaseResource):

    def __init__(self):
        self.entity = WatchListItem
        self.columns_to_response = ("id", "user_id", "imdb_id", "title")


class WatchListResource(BaseListResource):

    def __init__(self):
        self.entity = WatchListItem
        self.columns_to_response = ("id", "user_id", "title")
        self.post_parser_args = ("user_id", "imdb_id", "title")
