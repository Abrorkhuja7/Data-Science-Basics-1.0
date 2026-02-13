import sys
from analytics import Research, Analytics
import config


def main():
    if len(sys.argv) != 2:
        raise Exception("Usage: python3 make_report.py <path>")

    data = Research(sys.argv[1]).file_reader()
    a = Analytics(data)

    heads, tails = a.counts()
    ph, pt = a.fractions(heads, tails)

    preds = a.predict_random(config.num_of_steps)
    f_heads = sum(x[0] for x in preds)
    f_tails = sum(x[1] for x in preds)

    report = config.report_template.format(
        n=len(data), tails=tails, heads=heads,
        pt=pt, ph=ph, steps=config.num_of_steps,
        ft=f_tails, fh=f_heads
    )

    a.save_file(report, "report", "txt")
    print(report)


if __name__ == "__main__":
    main()
