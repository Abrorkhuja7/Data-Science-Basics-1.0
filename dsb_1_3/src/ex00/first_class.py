def main():
    class Must_Read:
        # Code inside the class body (no methods/constructors yet)
        with open("data.csv", "r", encoding="utf-8") as f:
            print(f.read(), end="")

if __name__ == "__main__":
    main()
