import os, json, logging, requests
from random import randint
import config

logging.basicConfig(filename="analytics.log", level=logging.INFO,
                    format="%(asctime)s %(message)s")

class Research:
    def __init__(self, path: str):
        logging.info("Research.__init__ path=%s", path)
        self.path = path

    def file_reader(self, has_header: bool = True):
        logging.info("Research.file_reader has_header=%s", has_header)
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

    def send_telegram(self, text: str):
        logging.info("Research.send_telegram text=%s", text)
        if not config.telegram_webhook_url:
            return
        requests.post(config.telegram_webhook_url, json={"text": text}, timeout=10)

class Calculations:
    def __init__(self, data):
        logging.info("Calculations.__init__")
        self.data = data

    def counts(self):
        logging.info("Calculations.counts")
        return sum(x[0] for x in self.data), sum(x[1] for x in self.data)

    def fractions(self, heads: int, tails: int):
        logging.info("Calculations.fractions")
        total = heads + tails
        return (heads / total) * 100, (tails / total) * 100

class Analytics(Calculations):
    def predict_random(self, num_predictions: int):
        logging.info("Analytics.predict_random n=%s", num_predictions)
        res = []
        for _ in range(num_predictions):
            h = randint(0, 1)
            res.append([h, 1 - h])
        return res

    def predict_last(self):
        logging.info("Analytics.predict_last")
        return self.data[-1]

    def save_file(self, data, filename: str, ext: str):
        logging.info("Analytics.save_file %s.%s", filename, ext)
        with open(f"{filename}.{ext}", "w", encoding="utf-8") as f:
            f.write(str(data))
