import timeit
import random
from collections import Counter

def gen_list():
    return [random.randint(0, 100) for _ in range(1_000_000)]

def my_counts(lst):
    d = dict.fromkeys(range(101), 0)
    for x in lst:
        d[x] += 1
    return d

def my_top10(lst):
    d = my_counts(lst)
    return dict(sorted(d.items(), key=lambda kv: kv[1], reverse=True)[:10])

def counter_counts(lst):
    return Counter(lst)

def counter_top10(lst):
    return dict(Counter(lst).most_common(10))

def main():
    try:
        lst = gen_list()

        print(f"my function: {timeit.timeit(lambda: my_counts(lst), number=1)}")
        print(f"Counter: {timeit.timeit(lambda: counter_counts(lst), number=1)}")
        print(f"my top: {timeit.timeit(lambda: my_top10(lst), number=1)}")
        print(f"Counter's top: {timeit.timeit(lambda: counter_top10(lst), number=1)}")
    except Exception:
        return

if __name__ == "__main__":
    try: main()
    except Exception: pass