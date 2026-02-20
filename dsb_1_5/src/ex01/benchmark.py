import timeit

emails = ['john@gmail.com','james@gmail.com','alice@yahoo.com','anna@live.com','philipp@gmail.com'] * 5

def loop():
    out=[]
    for e in emails:
        if e.endswith("@gmail.com"):
            out.append(e)
    return out

def list_comp():
    return [e for e in emails if e.endswith("@gmail.com")]


def map_func():
    return list(map(lambda e: e if e.endswith("@gmail.com") else None, emails))


def main():
    t_loop = timeit.timeit(loop, number=90_000_000)
    t_lc = timeit.timeit(list_comp, number=90_000_000)
    t_map = timeit.timeit(map_func, number=90_000_000)
    best = min((t_loop,"it is better to use a loop"),
               (t_lc,"it is better to use a list comprehension"),
               (t_map,"it is better to use a map"))[1]
    print(best)
    a,b,c = sorted([t_map,t_lc,t_loop])
    print(f"{a} vs {b} vs {c}")

if __name__ == "__main__":
    try: main()
    except Exception: pass
