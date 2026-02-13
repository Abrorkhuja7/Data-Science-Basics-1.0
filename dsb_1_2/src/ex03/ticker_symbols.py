import sys

def main():
    if len(sys.argv) != 2:
        return
    q = sys.argv[1].strip().upper()
    COMPANIES = {'Apple': 'AAPL', 'Microsoft': 'MSFT', 'Netflix': 'NFLX', 'Tesla': 'TSLA', 'Nokia': 'NOK'}
    STOCKS = {'AAPL': 287.73, 'MSFT': 173.79, 'NFLX': 416.90, 'TSLA': 724.88, 'NOK': 3.37}
    inv = {v: k for k, v in COMPANIES.items()}
    if q not in inv:
        print("Unknown ticker")
        return
    print(f"{inv[q]} {STOCKS[q]}")

if __name__ == '__main__':
    main()
