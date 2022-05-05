class Urls():
    search_by_title = "https://imdb-api.com/ru/API/Search/{imdb_token}/{title}"
    get_by_id = "https://imdb-api.com/ru/API/Title/{imdb_token}/{id}"
    get_trailer = "https://imdb-api.com/ru/API/Trailer/{imdb_token}/{id}"
    get_posters = "https://imdb-api.com/ru/API/Posters/{imdb_token}/{id}"

    get_full_data = "https://imdb-api.com/ru/API/Title/{imdb_token}/{id}/Posters,Trailer,Ratings,"

    register = "{api_uri}/users/?id={telegram_id}"
    new_watch_item = "{api_uri}/watch_items/?imdb_id={imdb_id}&user_id={user_id}&title={title}"
    delete_watch_item="{api_uri}/watch_items/{id}"
    get_user_info = "{api_uri}/users/{id}"
