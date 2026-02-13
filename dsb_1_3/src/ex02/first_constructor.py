import sys
import os


class Research:
    def __init__(self, path: str):
        self.path = path

    def file_reader(self):
        if not os.path.isfile(self.path):
            raise Exception("File not found")

        with open(self.path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        if len(lines) < 2:
            raise Exception("Bad file")

        header = lines[0].split(",")
        if len(header) != 2 or not header[0] or not header[1]:
            raise Exception("Bad header")

        for line in lines[1:]:
            parts = line.split(",")
            if len(parts) != 2:
                raise Exception("Bad line")
            if parts not in (["0", "1"], ["1", "0"]):
                raise Exception("Bad value")

        return "\n".join(lines)


def main():
    if len(sys.argv) != 2:
        raise Exception("Usage: python3 first_constructor.py <path>")

    r = Research(sys.argv[1])
    print(r.file_reader())


if __name__ == "__main__":
    main()
