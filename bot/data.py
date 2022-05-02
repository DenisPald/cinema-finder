from dataclasses import asdict, dataclass


@dataclass
class MovieInfo:
    id: str
    trailer_link: str
    posters: list[dict]
    plot: str
    rewards: str
    ratings: dict
    stars: str
    similars: list[dict]
    plotLocal: str = ""

    def as_dict(self):
        return asdict(self)

    def get_poster_link(self, number):
        return self.posters[number]['link']

    def get_ratings(self):
        res = ""
        res += f"IMDB: {self.ratings['imDb']}\n"
        res += f"Metacritic: {self.ratings['metacritic']}\n"
        res += f"Rotten tomatoes: {self.ratings['rottenTomatoes']}\n"
        return res

    def similars_get_poster_link(self, number):
        return self.similars[number]['image']
