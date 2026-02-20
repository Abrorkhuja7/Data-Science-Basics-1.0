import sys
import time
import requests
from bs4 import BeautifulSoup


def get_financial_data(ticker, field):
    url = f"https://finance.yahoo.com/quote/{ticker}/financials"
    session = requests.Session()
    headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "gzip, deflate, br",  "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8","Connection": "keep-alive", }
    session.headers.update(headers)

    session.get("https://finance.yahoo.com")
    time.sleep(5)
    response = session.get(url, allow_redirects=True)
    if response.status_code != 200:
        raise Exception("URL does not exist")

    soup = BeautifulSoup(response.text, "html.parser")

    rows = soup.find_all("div",{"class":"row"})
    for row in rows:
        cells = row.find_all("div",{"class":"column"})
        if not cells:
            continue

        field_name = cells[0].get_text(strip=True)
        if field_name == field:
            values = [cell.get_text(strip=True) for cell in cells]
            return tuple(values)

    raise Exception("Requested field does not exist")


def main():
    if len(sys.argv) != 3:
        raise Exception("Usage: financial.py <TICKER> <FIELD>")

    ticker = sys.argv[1]
    field = sys.argv[2]

    result = get_financial_data(ticker, field)

    #time.sleep(5)

    print(result)


if __name__ == "__main__":
    main()
