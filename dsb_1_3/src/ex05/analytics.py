import os
from random import randint


class Research:
    def __init__(self, path: str):
        self.path = path

    def file_reader(self, has_header: bool = True):
        if not os.path.isfile(self.path):
            raise Exception("File not found")
        with open(self.path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        start = 1 if has_header else 0
        if has_header:
            header = lines[0].split(",")
            if len(header) != 2:
                raise Exception("Bad header")

        data = []
        for line in lines[start:]:
            parts = line.split(",")
            if parts not in (["0", "1"], ["1", "0"]):
                raise Exception("Bad value")
            data.append([int(parts[0]), int(parts[1])])
        return data


class Calculations:
    def __init__(self, data):
        self.data = data

    def counts(self):
        heads = sum(x[0] for x in self.data)
        tails = sum(x[1] for x in self.data)
        return heads, tails

    def fractions(self, heads: int, tails: int):
        total = heads + tails
        return (heads / total) * 100, (tails / total) * 100


class Analytics(Calculations):
    def predict_random(self, num_predictions: int):
        res = []
        for _ in range(num_predictions):
            head = randint(0, 1)
            res.append([head, 1 - head])
        return res

    def predict_last(self):
        return self.data[-1]

    def save_file(self, data, filename: str, ext: str):
        with open(f"{filename}.{ext}", "w", encoding="utf-8") as f:
            f.write(str(data))
