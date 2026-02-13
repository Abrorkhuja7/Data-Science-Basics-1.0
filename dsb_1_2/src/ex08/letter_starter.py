import sys

def main():
    if len(sys.argv) != 2:
        raise Exception("Wrong arguments")
    email = sys.argv[1].strip()
    with open('employees.tsv', 'r', encoding='utf-8') as f:
        next(f, None)  # header
        for line in f:
            name, surname, e = line.rstrip('\n').split('\t')
            if e == email:
                print(f"Dear {name}, welcome to our team! We are sure that it will be a pleasure to work with you. "
                      f"That’s a precondition for the professionals that our company hires.")
                return

if __name__ == '__main__':
    main()
