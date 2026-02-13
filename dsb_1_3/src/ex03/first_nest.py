import sys
import os


class Research:
    def __init__(self, path: str):
        self.path = path

    def file_reader(self, has_header: bool = True):
        if not os.path.isfile(self.path):
            raise Exception("File not found")

        with open(self.path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        if len(lines) < 1:
            raise Exception("Bad file")

        start = 1 if has_header else 0
        if has_header:
            header = lines[0].split(",")
            if len(header) != 2 or not header[0] or not header[1]:
                raise Exception("Bad header")

        data = []
        for line in lines[start:]:
            parts = line.split(",")
            if len(parts) != 2 or parts not in (["0", "1"], ["1", "0"]):
                raise Exception("Bad value")
            data.append([int(parts[0]), int(parts[1])])

        return data

    class Calculations:
        def counts(self, data):
            heads = sum(x[0] for x in data)
            tails = sum(x[1] for x in data)
            return heads, tails

        def fractions(self, heads: int, tails: int):
            total = heads + tails
            if total == 0:
                return 0.0, 0.0
            return heads / total, tails / total


def main():
    if len(sys.argv) != 2:
        raise Exception("Usage: python3 first_nest.py <path>")

    r = Research(sys.argv[1])
    data = r.file_reader()

    calc = Research.Calculations()
    heads, tails = calc.counts(data)
    fh, ft = calc.fractions(heads, tails)

    print(data)
    print(heads, tails)
    print(f"{fh:.4f} {ft:.4f}")


if __name__ == "__main__":
    main()
