from data._all_models import *
from resources.base import BaseListResource, BaseResource


class UserResource(BaseResource):

    def __init__(self):
        self.entity = User
        self.columns_to_response = ("id", "watch_item.id",
                                    "watch_item.imdb_id", "watch_item.title")


class UserListResource(BaseListResource):

    def __init__(self):
        self.entity = User
        self.columns_to_response = ("id", "watch_item.title")
        self.post_parser_args = ("id", )
