class Urls():
    search_by_title = "https://imdb-api.com/ru/API/Search/{imdb_token}/{title}"
    get_by_id = "https://imdb-api.com/ru/API/Title/{imdb_token}/{id}"
    get_trailer = "https://imdb-api.com/ru/API/Trailer/{imdb_token}/{id}"
    get_posters = "https://imdb-api.com/ru/API/Posters/{imdb_token}/{id}"

    get_full_data = "https://imdb-api.com/ru/API/Title/{imdb_token}/{id}/Posters,Trailer,Ratings,"
