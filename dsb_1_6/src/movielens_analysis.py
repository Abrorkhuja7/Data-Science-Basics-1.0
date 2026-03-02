import os
import re
from collections import Counter, defaultdict
import pytest

def get_config():
    return {
        "LIMIT": 1000,
        "RATINGS_PATH": "ml_data/ratings.csv",
        "TAGS_PATH": "ml_data/tags.csv",
        "MOVIES_PATH": "ml_data/movies.csv",
        "LINKS_PATH": "ml_data/links.csv",
    }


def _load_file(path, required_fields, row_parser, limit=1000):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")
    rows = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            header = f.readline().rstrip("\n").split(",")
            fieldnames = [h.strip() for h in header]
            if not required_fields.issubset(set(fieldnames)):
                raise ValueError(f"Missing required columns: {required_fields - set(fieldnames)}")
            for i, line in enumerate(f):
                if i >= limit:
                    break
                values = line.rstrip("\n").split(",")
                r = dict(zip(fieldnames, values))
                parsed = row_parser(r, i)
                if parsed is not None:
                    rows.append(parsed)
    except UnicodeDecodeError:
        raise ValueError("File must be UTF-8")
    except OSError as e:
        raise OSError(f"Cannot read file: {e}")
    if not rows:
        raise ValueError("No data loaded")
    return rows


class Ratings:
    FIELDS = {"userId", "movieId", "rating", "timestamp"}

    def __init__(self, path=None, limit=None):
        cfg = get_config()
        self.rows = _load_file(
            path or cfg["RATINGS_PATH"],
            self.FIELDS,
            lambda r, _: (int(r["userId"]), int(r["movieId"]), float(r["rating"]), int(r["timestamp"])),
            limit or cfg["LIMIT"]
        )

    def avg_rating(self):
        return sum(rating for _, _, rating, _ in self.rows) / len(self.rows)

    def top_movies(self, n=10):
        sums, counts = defaultdict(float), Counter()
        for _, movie, rating, _ in self.rows:
            sums[movie] += rating
            counts[movie] += 1
        averages = {movie: sums[movie] / counts[movie] for movie in counts}
        return sorted(averages.items(), key=lambda x: x[1], reverse=True)[:int(n)]

    def top_active_users(self, n=10):
        counts = Counter(user for user, _, _, _ in self.rows)
        return counts.most_common(int(n))


class Tags:
    FIELDS = {"userId", "movieId", "tag", "timestamp"}

    def __init__(self, path=None, limit=None):
        cfg = get_config()

        def parse(r, i):
            tag = r["tag"].strip()
            if not tag:
                return None  # skip empty tags instead of raising
            return (int(r["userId"]), int(r["movieId"]), tag, int(r["timestamp"]))

        self.rows = _load_file(path or cfg["TAGS_PATH"], self.FIELDS, parse, limit or cfg["LIMIT"])

    def most_frequent_tags(self, n=10):
        n = int(n)
        if n <= 0:
            raise ValueError("n must be > 0")
        counts = Counter(tag.lower() for _, _, tag, _ in self.rows)
        return counts.most_common(n)

    def top_movies_by_tags(self, n=10):
        counts = Counter(movie for _, movie, _, _ in self.rows)
        return counts.most_common(int(n))

    def top_users_by_tags(self, n=10):
        counts = Counter(user for user, _, _, _ in self.rows)
        return counts.most_common(int(n))


class Movies:
    FIELDS = {"movieId", "title", "genres"}
    _YEAR_RE = re.compile(r"\((\d{4})\)")

    def __init__(self, path=None, limit=None):
        cfg = get_config()

        def parse(r, i):
            title = r["title"].strip()
            if not title:
                return None  # skip empty titles instead of raising
            return (int(r["movieId"]), title, r["genres"].strip())

        self.rows = _load_file(path or cfg["MOVIES_PATH"], self.FIELDS, parse, limit or cfg["LIMIT"])

    def top_years_by_movie_count(self, n=5):
        counts = Counter()
        for _, title, _ in self.rows:
            if m := self._YEAR_RE.search(title):
                counts[int(m.group(1))] += 1
        return counts.most_common(int(n))

    def top_movies_by_genre_count(self, n=10):
        def genre_count(genres):
            return 0 if genres == "(no genres listed)" else genres.count("|") + 1

        result = [(mid, title, genre_count(genres)) for mid, title, genres in self.rows]
        return sorted(result, key=lambda x: x[2], reverse=True)[:int(n)]

    def top_genres(self, n=10):
        counts = Counter(
            genre
            for _, _, genres in self.rows
            if genres != "(no genres listed)"
            for genre in genres.split("|")
        )
        return counts.most_common(int(n))


class Links:
    FIELDS = {"movieId", "imdbId", "tmdbId"}

    def __init__(self, path=None, limit=None):
        cfg = get_config()
        self.rows = _load_file(
            path or cfg["LINKS_PATH"],
            self.FIELDS,
            lambda r, _: (int(r["movieId"]), r["imdbId"].strip(), r["tmdbId"].strip()),
            limit or cfg["LIMIT"]
        )
        self._index = {movie: (imdb, tmdb) for movie, imdb, tmdb in self.rows}

    def imdb_url(self, movie_id: int):
        ids = self._index.get(int(movie_id))
        return f"https://www.imdb.com/title/tt{ids[0]}/" if ids and ids[0] else None

    def tmdb_url(self, movie_id: int):
        ids = self._index.get(int(movie_id))
        return f"https://www.themoviedb.org/movie/{ids[1]}" if ids and ids[1] else None

    def movielens_url(self, movie_id: int):
        return f"https://movielens.org/movies/{int(movie_id)}"

    def missing_ids_stats(self):
        missing_imdb = sum(1 for _, imdb, _ in self.rows if not imdb)
        missing_tmdb = sum(1 for _, _, tmdb in self.rows if not tmdb)
        return {
            "total_movies": len(self.rows),
            "missing_imdb": missing_imdb,
            "missing_tmdb": missing_tmdb,
        }

class Tests:

    # ---------- Ratings ----------
    def test_avg_rating_return_type(self):
        r = Ratings()
        x = r.avg_rating()
        assert isinstance(x, float), "avg_rating() should return a float value"

    def test_top_movies_types_and_sorted(self):
        r = Ratings()
        out = r.top_movies(10)
        assert isinstance(out, list), "top_movies() must return a list"
        assert all(isinstance(t, tuple) and len(t) == 2 for t in out), "Each item must be a tuple (movieId, average)"
        assert all(isinstance(mid, int) and isinstance(avg, float) for mid, avg in out), "movieId must be int and average must be float"
        assert out == sorted(out, key=lambda x: x[1], reverse=True), "Movies must be sorted by average rating descending"

    def test_top_active_users_types_and_sorted(self):
        r = Ratings()
        out = r.top_active_users(10)
        assert isinstance(out, list), "top_active_users() must return a list"
        assert all(isinstance(t, tuple) and len(t) == 2 for t in out), "Each item must be a tuple (userId, count)"
        assert all(isinstance(uid, int) and isinstance(cnt, int) for uid, cnt in out), "userId and count must both be integers"
        assert out == sorted(out, key=lambda x: x[1], reverse=True), "Users must be sorted by activity descending"

    # ---------- Tags ----------
    def test_most_frequent_tags_types_and_sorted(self):
        t = Tags()
        out = t.most_frequent_tags(10)
        assert isinstance(out, list), "most_frequent_tags() must return a list"
        assert all(isinstance(x, tuple) and len(x) == 2 for x in out), "Each item must be a tuple (tag, count)"
        assert all(isinstance(tag, str) and isinstance(cnt, int) for tag, cnt in out), "tag must be str and count must be int"
        assert out == sorted(out, key=lambda x: x[1], reverse=True), "Tags must be sorted by frequency descending"

    def test_top_movies_by_tags_types_and_sorted(self):
        t = Tags()
        out = t.top_movies_by_tags(10)
        assert isinstance(out, list), "top_movies_by_tags() must return a list"
        assert all(isinstance(x, tuple) and len(x) == 2 for x in out), "Each item must be a tuple (movieId, count)"
        assert all(isinstance(mid, int) and isinstance(cnt, int) for mid, cnt in out), "movieId and count must both be integers"
        assert out == sorted(out, key=lambda x: x[1], reverse=True), "Movies must be sorted by tag count descending"

    def test_top_users_by_tags_types_and_sorted(self):
        t = Tags()
        out = t.top_users_by_tags(10)
        assert isinstance(out, list), "top_users_by_tags() must return a list"
        assert all(isinstance(x, tuple) and len(x) == 2 for x in out), "Each item must be a tuple (userId, count)"
        assert all(isinstance(uid, int) and isinstance(cnt, int) for uid, cnt in out), "userId and count must both be integers"
        assert out == sorted(out, key=lambda x: x[1], reverse=True), "Users must be sorted by tag activity descending"

    # ---------- Movies ----------
    def test_top_years_by_movie_count_types_and_sorted(self):
        m = Movies()
        out = m.top_years_by_movie_count(5)
        assert isinstance(out, list), "top_years_by_movie_count() must return a list"
        assert all(isinstance(x, tuple) and len(x) == 2 for x in out), "Each item must be a tuple (year, count)"
        assert all(isinstance(year, int) and isinstance(cnt, int) for year, cnt in out), "year and count must both be integers"
        assert out == sorted(out, key=lambda x: x[1], reverse=True), "Years must be sorted by movie count descending"

    def test_top_movies_by_genre_count_types_and_sorted(self):
        m = Movies()
        out = m.top_movies_by_genre_count(10)
        assert isinstance(out, list), "top_movies_by_genre_count() must return a list"
        assert all(isinstance(x, tuple) and len(x) == 3 for x in out), "Each item must be a tuple (movieId, title, genre_count)"
        assert all(isinstance(mid, int) and isinstance(title, str) and isinstance(cnt, int)
                   for mid, title, cnt in out), "movieId must be int, title must be str, genre_count must be int"
        assert out == sorted(out, key=lambda x: x[2], reverse=True), "Movies must be sorted by number of genres descending"

    def test_top_genres_types_and_sorted(self):
        m = Movies()
        out = m.top_genres(10)
        assert isinstance(out, list), "top_genres() must return a list"
        assert all(isinstance(x, tuple) and len(x) == 2 for x in out), "Each item must be a tuple (genre, count)"
        assert all(isinstance(genre, str) and isinstance(cnt, int) for genre, cnt in out), "genre must be str and count must be int"
        assert out == sorted(out, key=lambda x: x[1], reverse=True), "Genres must be sorted by frequency descending"

    # ---------- Links ----------
    def test_links_urls_return_types(self):
        l = Links()
        u1 = l.imdb_url(1)
        u2 = l.tmdb_url(1)
        assert (u1 is None) or isinstance(u1, str), "imdb_url() must return either None or a string"
        assert (u2 is None) or isinstance(u2, str), "tmdb_url() must return either None or a string"

    def test_missing_ids_stats_types(self):
        l = Links()
        out = l.missing_ids_stats()
        assert isinstance(out, dict), "missing_ids_stats() must return a dictionary"
        assert set(out.keys()) == {"total_movies", "missing_imdb", "missing_tmdb"}, "Dictionary must contain exact required keys"
        assert all(isinstance(out[k], int) for k in out), "All dictionary values must be integers"

    # ---------- Bonus part ----------
    def test_avg_rating_exact(self, tmp_path):
        p = tmp_path / "ratings.csv"
        p.write_text(
            "userId,movieId,rating,timestamp\n"
            "1,10,4.0,100\n"
            "2,10,2.0,101\n"
            "3,11,5.0,102\n"
        )
        r = Ratings(path=str(p), limit=100)
        expected = (4.0 + 2.0 + 5.0) / 3
        got = r.avg_rating()
        assert got == expected, f"avg_rating() is wrong: expected {expected}, got {got}"

    def test_top_movies_exact(self, tmp_path):
        p = tmp_path / "ratings.csv"
        p.write_text(
            "userId,movieId,rating,timestamp\n"
            "1,10,4.0,100\n"
            "2,10,2.0,101\n"
            "3,11,5.0,102\n"
        )
        r = Ratings(path=str(p), limit=100)
        expected = [(11, 5.0), (10, 3.0)]
        got = r.top_movies(2)
        assert got == expected, f"top_movies(2) is wrong: expected {expected}, got {got}"

    def test_top_active_users_exact(self, tmp_path):
        p = tmp_path / "ratings.csv"
        p.write_text(
            "userId,movieId,rating,timestamp\n"
            "1,10,4.0,100\n"
            "1,11,2.0,101\n"
            "2,11,5.0,102\n"
        )
        r = Ratings(path=str(p), limit=100)
        expected = [(1, 2), (2, 1)]
        got = r.top_active_users(2)
        assert got == expected, f"top_active_users(2) is wrong: expected {expected}, got {got}"

    def test_most_frequent_tags_exact(self, tmp_path):
        p = tmp_path / "tags.csv"
        p.write_text(
            "userId,movieId,tag,timestamp\n"
            "1,10,Action,100\n"
            "2,10,action,101\n"
            "3,11,Drama,102\n"
        )
        t = Tags(path=str(p), limit=100)
        expected = [("action", 2), ("drama", 1)]
        got = t.most_frequent_tags(2)
        assert got == expected, f"most_frequent_tags(2) is wrong: expected {expected}, got {got}"

    def test_movies_top_genres_and_years_exact(self, tmp_path):
        p = tmp_path / "movies.csv"
        p.write_text(
            "movieId,title,genres\n"
            "10,Toy (1995),Adventure|Comedy\n"
            "11,Serious (1995),Drama\n"
            "12,NoYear,Comedy\n"
        )
        m = Movies(path=str(p), limit=100)

        expected_years = [(1995, 2)]
        got_years = m.top_years_by_movie_count(1)
        assert got_years == expected_years, \
            f"top_years_by_movie_count(1) is wrong: expected {expected_years}, got {got_years}"

        expected_genres = [("Comedy", 2), ("Adventure", 1)]
        got_genres = m.top_genres(2)
        assert got_genres == expected_genres, \
            f"top_genres(2) is wrong: expected {expected_genres}, got {got_genres}"

    def test_links_urls_and_missing_stats_exact(self, tmp_path):
        p = tmp_path / "links.csv"
        p.write_text(
            "movieId,imdbId,tmdbId\n"
            "10,0114709,862\n"
            "11,,123\n"
            "12,9999999,\n"
        )
        l = Links(path=str(p), limit=100)

        expected_imdb = "https://www.imdb.com/title/tt0114709/"
        got_imdb = l.imdb_url(10)
        assert got_imdb == expected_imdb, f"imdb_url(10) is wrong: expected {expected_imdb}, got {got_imdb}"

        expected_tmdb = "https://www.themoviedb.org/movie/862"
        got_tmdb = l.tmdb_url(10)
        assert got_tmdb == expected_tmdb, f"tmdb_url(10) is wrong: expected {expected_tmdb}, got {got_tmdb}"

        expected_stats = {"total_movies": 3, "missing_imdb": 1, "missing_tmdb": 1}
        got_stats = l.missing_ids_stats()
        assert got_stats == expected_stats, \
            f"missing_ids_stats() is wrong: expected {expected_stats}, got {got_stats}"

if __name__ == "__main__":
    pass
