def parse_csv_line(line):
    fields, cur, in_q, i = [], [], False, 0
    while i < len(line):
        ch = line[i]
        if ch == '"':
            if in_q and i + 1 < len(line) and line[i + 1] == '"':
                cur.append('"'); i += 2; continue
            in_q = not in_q
        elif ch == ',' and not in_q:
            fields.append(''.join(cur)); cur = []
        else:
            cur.append(ch)
        i += 1
    fields.append(''.join(cur))
    return fields

def main():
    with open('ds.csv', 'r', encoding='utf-8') as f_in, open('ds.tsv', 'w', encoding='utf-8') as f_out:
        for line in f_in:
            line = line.rstrip('\n')
            f_out.write('\t'.join(parse_csv_line(line)) + '\n')

if __name__ == '__main__':
    main()
