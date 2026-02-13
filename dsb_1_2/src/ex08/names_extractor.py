import sys

def cap(s): 
    return s[:1].upper() + s[1:].lower() if s else s

def main():
    if len(sys.argv) != 2:
        raise Exception("Wrong arguments")
    path = sys.argv[1]
    with open(path, 'r', encoding='utf-8') as f:
        emails = [line.strip() for line in f if line.strip()]

    with open('employees.tsv', 'w', encoding='utf-8') as out:
        out.write("Name\tSurname\tEmail\n")
        for e in emails:
            local = e.split('@', 1)[0]
            if '.' not in local:
                continue
            name, surname = local.split('.', 1)
            out.write(f"{cap(name)}\t{cap(surname)}\t{e}\n")

if __name__ == '__main__':
    main()
