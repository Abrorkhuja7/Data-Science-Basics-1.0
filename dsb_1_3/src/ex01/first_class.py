def main():
    class Research:
        def file_reader(self):
            with open("data.csv", "r", encoding="utf-8") as f:
                return f.read()

    r = Research()
    print(r.file_reader(), end="")

if __name__ == "__main__":
    main()

