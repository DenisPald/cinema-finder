from data._all_models import *
from resources.base import BaseListResource, BaseResource


class UserResource(BaseResource):

    def __init__(self):
        self.entity = User
        self.columns_to_response = ("id", "watch_item.id",
                                    "watch_item.imdb_id", "telegram_id")


class UserListResource(BaseListResource):

    def __init__(self):
        self.entity = User
        self.columns_to_response = ("id", "watch_item.id",
                                    "watch_item.imdb_id")
        self.post_parser_args = ("telegram_id", )
