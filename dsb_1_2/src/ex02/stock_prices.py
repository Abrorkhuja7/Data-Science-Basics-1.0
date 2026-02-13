import sys

def main():
    if len(sys.argv) != 2:
        return
    q = sys.argv[1].strip()
    COMPANIES = {'Apple': 'AAPL', 'Microsoft': 'MSFT', 'Netflix': 'NFLX', 'Tesla': 'TSLA', 'Nokia': 'NOK'}
    STOCKS = {'AAPL': 287.73, 'MSFT': 173.79, 'NFLX': 416.90, 'TSLA': 724.88, 'NOK': 3.37}
    name_map = {k.lower(): v for k, v in COMPANIES.items()}
    t = name_map.get(q.lower())
    if not t:
        print("Unknown company.")
        return
    print(STOCKS[t])

if __name__ == '__main__':
    main()
