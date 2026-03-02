from movielens_analysis import Ratings, Tags, Movies, Links

# ---------- Ratings ----------
def test_avg_rating_return_type():
    r = Ratings()
    x = r.avg_rating()
    assert isinstance(x, float)

def test_top_movies_types_and_sorted():
    r = Ratings()
    out = r.top_movies(10)
    assert isinstance(out, list)
    assert all(isinstance(t, tuple) and len(t) == 2 for t in out)
    assert all(isinstance(mid, int) and isinstance(avg, float) for mid, avg in out)
    assert out == sorted(out, key=lambda x: x[1], reverse=True)

def test_top_active_users_types_and_sorted():
    r = Ratings()
    out = r.top_active_users(10)
    assert isinstance(out, list)
    assert all(isinstance(t, tuple) and len(t) == 2 for t in out)
    assert all(isinstance(uid, int) and isinstance(cnt, int) for uid, cnt in out)
    assert out == sorted(out, key=lambda x: x[1], reverse=True)

# ---------- Tags ----------
def test_most_frequent_tags_types_and_sorted():
    t = Tags()
    out = t.most_frequent_tags(10)
    assert isinstance(out, list)
    assert all(isinstance(x, tuple) and len(x) == 2 for x in out)
    assert all(isinstance(tag, str) and isinstance(cnt, int) for tag, cnt in out)
    assert out == sorted(out, key=lambda x: x[1], reverse=True)

def test_top_movies_by_tags_types_and_sorted():
    t = Tags()
    out = t.top_movies_by_tags(10)
    assert isinstance(out, list)
    assert all(isinstance(x, tuple) and len(x) == 2 for x in out)
    assert all(isinstance(mid, int) and isinstance(cnt, int) for mid, cnt in out)
    assert out == sorted(out, key=lambda x: x[1], reverse=True)

def test_top_users_by_tags_types_and_sorted():
    t = Tags()
    out = t.top_users_by_tags(10)
    assert isinstance(out, list)
    assert all(isinstance(x, tuple) and len(x) == 2 for x in out)
    assert all(isinstance(uid, int) and isinstance(cnt, int) for uid, cnt in out)
    assert out == sorted(out, key=lambda x: x[1], reverse=True)

# ---------- Movies ----------
def test_top_years_by_movie_count_types_and_sorted():
    m = Movies()
    out = m.top_years_by_movie_count(5)
    assert isinstance(out, list)
    assert all(isinstance(x, tuple) and len(x) == 2 for x in out)
    assert all(isinstance(year, int) and isinstance(cnt, int) for year, cnt in out)
    assert out == sorted(out, key=lambda x: x[1], reverse=True)

def test_top_movies_by_genre_count_types_and_sorted():
    m = Movies()
    out = m.top_movies_by_genre_count(10)
    assert isinstance(out, list)
    assert all(isinstance(x, tuple) and len(x) == 3 for x in out)
    assert all(isinstance(mid, int) and isinstance(title, str) and isinstance(cnt, int)
               for mid, title, cnt in out)
    assert out == sorted(out, key=lambda x: x[2], reverse=True)

def test_top_genres_types_and_sorted():
    m = Movies()
    out = m.top_genres(10)
    assert isinstance(out, list)
    assert all(isinstance(x, tuple) and len(x) == 2 for x in out)
    assert all(isinstance(genre, str) and isinstance(cnt, int) for genre, cnt in out)
    assert out == sorted(out, key=lambda x: x[1], reverse=True)

# ---------- Links ----------
def test_links_urls_return_types():
    l = Links()
    u1 = l.imdb_url(1)
    u2 = l.tmdb_url(1)
    assert (u1 is None) or isinstance(u1, str)
    assert (u2 is None) or isinstance(u2, str)

def test_missing_ids_stats_types():
    l = Links()
    out = l.missing_ids_stats()
    assert isinstance(out, dict)
    assert set(out.keys()) == {"total_movies", "missing_imdb", "missing_tmdb"}
    assert all(isinstance(out[k], int) for k in out)

# ---------- Bonus 2: exact correctness tests (tiny CSVs) ----------
def test_avg_rating_exact(tmp_path):
    p = tmp_path / "ratings.csv"
    p.write_text(
        "userId,movieId,rating,timestamp\n"
        "1,10,4.0,100\n"
        "2,10,2.0,101\n"
        "3,11,5.0,102\n"
    )
    r = Ratings(path=str(p), limit=100)
    assert r.avg_rating() == (4.0 + 2.0 + 5.0) / 3

def test_top_movies_exact(tmp_path):
    p = tmp_path / "ratings.csv"
    p.write_text(
        "userId,movieId,rating,timestamp\n"
        "1,10,4.0,100\n"
        "2,10,2.0,101\n"
        "3,11,5.0,102\n"
    )
    r = Ratings(path=str(p), limit=100)
    # movie 11 avg=5.0, movie 10 avg=3.0
    assert r.top_movies(2) == [(11, 5.0), (10, 3.0)]

def test_top_active_users_exact(tmp_path):
    p = tmp_path / "ratings.csv"
    p.write_text(
        "userId,movieId,rating,timestamp\n"
        "1,10,4.0,100\n"
        "1,11,2.0,101\n"
        "2,11,5.0,102\n"
    )
    r = Ratings(path=str(p), limit=100)
    assert r.top_active_users(2) == [(1, 2), (2, 1)]

def test_most_frequent_tags_exact(tmp_path):
    p = tmp_path / "tags.csv"
    p.write_text(
        "userId,movieId,tag,timestamp\n"
        "1,10,Action,100\n"
        "2,10,action,101\n"
        "3,11,Drama,102\n"
    )
    t = Tags(path=str(p), limit=100)
    assert t.most_frequent_tags(2) == [("action", 2), ("drama", 1)]

def test_movies_top_genres_and_years_exact(tmp_path):
    p = tmp_path / "movies.csv"
    p.write_text(
        "movieId,title,genres\n"
        "10,Toy (1995),Adventure|Comedy\n"
        "11,Serious (1995),Drama\n"
        "12,NoYear,Comedy\n"
    )
    m = Movies(path=str(p), limit=100)
    assert m.top_years_by_movie_count(1) == [(1995, 2)]
    assert m.top_genres(2) == [("Comedy", 2), ("Adventure", 1)]

def test_links_urls_and_missing_stats_exact(tmp_path):
    p = tmp_path / "links.csv"
    p.write_text(
        "movieId,imdbId,tmdbId\n"
        "10,0114709,862\n"
        "11,,123\n"
        "12,9999999,\n"
    )
    l = Links(path=str(p), limit=100)
    assert l.imdb_url(10) == "https://www.imdb.com/title/tt0114709/"
    assert l.tmdb_url(10) == "https://www.themoviedb.org/movie/862"
    assert l.missing_ids_stats() == {"total_movies": 3, "missing_imdb": 1, "missing_tmdb": 1}
