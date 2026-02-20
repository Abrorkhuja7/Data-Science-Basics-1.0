#!/usr/bin/env python3
import os
import subprocess

def main():
    if os.environ.get("VIRTUAL_ENV") is None:
        raise Exception("Wrong environment")

    # install both in ONE command
    subprocess.run(
        ["python", "-m", "pip", "install", "beautifulsoup4", "pytest"],
        check=True
    )

    freeze = subprocess.check_output(
        ["python", "-m", "pip", "freeze"],
        text=True
    )

    print(freeze, end="")

    with open("requirements.txt", "w", encoding="utf-8") as f:
        f.write(freeze)

if __name__ == "__main__":
    main()

