import sys, config
from analytics import Research, Analytics

def main():
    if len(sys.argv) != 2:
        raise Exception("Usage: python3 make_report.py <path>")

    r = Research(sys.argv[1])
    try:
        data = r.file_reader()
        a = Analytics(data)
        heads, tails = a.counts()
        ph, pt = a.fractions(heads, tails)

        preds = a.predict_random(config.num_of_steps)
        fh = sum(x[0] for x in preds)
        ft = sum(x[1] for x in preds)

        report = config.report_template.format(
            n=len(data), tails=tails, heads=heads,
            pt=pt, ph=ph, steps=config.num_of_steps, ft=ft, fh=fh
        )
        a.save_file(report, "report", "txt")
        r.send_telegram("The report has been successfully created")
        print(report)
    except Exception:
        r.send_telegram("The report hasn't been created due to an error")
        raise

if __name__ == "__main__":
    main()
