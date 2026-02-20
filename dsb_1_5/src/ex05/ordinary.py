import sys
import resource
import time

def read_all(path):
    with open(path, "r") as f:
        return f.readlines()

def main():
    try:
        if len(sys.argv) != 2:
            return

        start = time.time()
        data = read_all(sys.argv[1])

        for _ in data:
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
