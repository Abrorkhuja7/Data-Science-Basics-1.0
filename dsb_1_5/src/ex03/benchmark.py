import sys
import timeit
from functools import reduce

def loop(n: int) -> int:
    s = 0
    for i in range(1, n + 1):
        s += i * i
    return s

def reduce_func(n: int) -> int:
    return reduce(lambda acc, i: acc + i * i, range(1, n + 1), 0)

func_calls = {
    "loop": loop,
    "reduce": reduce_func,
}


def main():
    try:
        if len(sys.argv) != 4:
            return
        name = sys.argv[1]
        calls = int(sys.argv[2])
        n = int(sys.argv[3])
        if name not in func_calls or calls < 1 or n < 1:
            return

        f = func_calls[name]
        print(timeit.timeit(lambda: f(n), number=calls))
    except Exception:
        return


if __name__ == "__main__":
    try: main()
    except Exception: pass
