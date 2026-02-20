import sys
import httpx
from bs4 import BeautifulSoup


def get_financial_data(ticker: str, field: str) -> tuple[str, ...]:
    url = f"https://finance.yahoo.com/quote/{ticker}/financials"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
    }

    transport = httpx.HTTPTransport(retries=5)
    with httpx.Client(
        headers=headers,
        follow_redirects=True,
        timeout=20.0,
        transport=transport,
    ) as client:
        client.get("https://finance.yahoo.com")
        r = client.get(url)

    if r.status_code != 200:
        raise Exception(f"HTTP {r.status_code} for {url}")

    soup = BeautifulSoup(r.text, "html.parser")

    for row in soup.select("div.row"):
        cols = row.select("div.column")
        if not cols:
            continue

        name = cols[0].get_text(strip=True)
        if name == field:
            return tuple(c.get_text(strip=True) for c in cols)

    raise Exception("Requested field does not exist")


def main():
    if len(sys.argv) != 3:
        raise Exception("Usage: financial_enhanced.py <TICKER> <FIELD>")

    ticker = sys.argv[1]
    field = sys.argv[2]
    print(get_financial_data(ticker, field))


if __name__ == "__main__":
    main()
