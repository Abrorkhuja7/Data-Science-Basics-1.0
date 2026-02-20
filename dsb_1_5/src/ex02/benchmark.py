import sys
import timeit

emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
          'anna@live.com', 'philipp@gmail.com'] * 5

def loop():
    out = []
    for e in emails:
        if e.endswith("@gmail.com"):
            out.append(e)
    return out

def list_comprehension():
    return [e for e in emails if e.endswith("@gmail.com")]

def map_func():
    return list(map(lambda e: e if e.endswith("@gmail.com") else None, emails))

def filter_func():
    return list(filter(lambda e: e.endswith("@gmail.com"), emails))

func_calls = {
    "loop": loop,
    "list_comprehension": list_comprehension,
    "map": map_func,
    "filter": filter_func,
}

def main():
    try:
        if len(sys.argv) != 3:
            return
        name = sys.argv[1]
        number = int(sys.argv[2])
        if name not in func_calls or number < 1:
            return
        print(timeit.timeit(func_calls[name], number=number))
    except Exception:
        return


if __name__ == "__main__":
    try: main()
    except Exception: pass
