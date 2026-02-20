import sys
import resource
import time

def read_gen(path):
    with open(path, "r") as f:
        for line in f:
            yield line

def main():
    try:
        if len(sys.argv) != 2:
            return

        start = time.time()
        for _ in read_gen(sys.argv[1]):
            pass

        usage = resource.getrusage(resource.RUSAGE_SELF)
        peak = usage.ru_maxrss / (1024 * 1024)
        total_time = usage.ru_utime + usage.ru_stime

        print(f"Peak Memory Usage = {peak:.3f} GB")
        print(f"User Mode Time + System Mode Time = {total_time:.2f}s")

    except Exception:
        return

if __name__ == "__main__":
    try: main()
    except Exception: pass
