import sys

def main():
    if len(sys.argv) != 2:
        return
    s = sys.argv[1]
    if ",," in s:
        return
    parts = [p.strip() for p in s.split(',')]
    if any(p == "" for p in parts):
        return

    COMPANIES = {'Apple': 'AAPL', 'Microsoft': 'MSFT', 'Netflix': 'NFLX', 'Tesla': 'TSLA', 'Nokia': 'NOK'}
    STOCKS = {'AAPL': 287.73, 'MSFT': 173.79, 'NFLX': 416.90, 'TSLA': 724.88, 'NOK': 3.37}

    comp_l = {k.lower(): v for k, v in COMPANIES.items()}
    tick_u = {v.upper(): k for k, v in COMPANIES.items()}

    for raw in parts:
        low = raw.lower()
        up = raw.upper()
        if low in comp_l:
            t = comp_l[low]
            print(f"{COMPANIES[[k for k in COMPANIES if k.lower()==low][0]]} stock price is {STOCKS[t]}")
        elif up in tick_u:
            print(f"{up} is a ticker symbol for {tick_u[up]}")
        else:
            print(f"{raw} is an unknown company or an unknown ticker symbol")

if __name__ == '__main__':
    main()
