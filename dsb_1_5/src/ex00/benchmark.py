import timeit

emails = ['john@gmail.com','james@gmail.com','alice@yahoo.com','anna@live.com','philipp@gmail.com']* 5

def loop():
    out = []
    for e in emails:
        if e.endswith("@gmail.com"):
            out.append(e)
    return out

def list_comp():
    return [e for e in emails if e.endswith("@gmail.com")]

def main():
    t_loop = timeit.timeit(loop, number=90_000_000)
    t_lc = timeit.timeit(list_comp, number=90_000_000)

    if (t_loop > t_lc): print("It is better to use list comprehesion")
    else: print("It is better to use loop")

    a, b = sorted([t_lc, t_loop])
    print(f"{a} vs {b}")

if __name__ == "__main__":
    try: main()
    except Exception: pass
