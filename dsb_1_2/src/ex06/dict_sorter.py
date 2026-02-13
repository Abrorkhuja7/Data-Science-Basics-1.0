def main():
    list_of_tuples = [
        ('Russia', '25'), ('France', '132'), ('Germany', '132'), ('Spain', '178'),
        ('Italy', '162'), ('Portugal', '17'), ('Finland', '3'), ('Hungary', '2'),
        ('The Netherlands', '28'), ('The USA', '610'), ('The United Kingdom', '95'),
        ('China', '83'), ('Iran', '76'), ('Turkey', '65'), ('Belgium', '34'),
        ('Canada', '28'), ('Switzerland', '26'), ('Brazil', '25'), ('Austria', '14'),
        ('Israel', '12')
    ]
    d = {country: int(num) for country, num in list_of_tuples}
    for country, _ in sorted(d.items(), key=lambda kv: (-kv[1], kv[0])):
        print(country)

if __name__ == '__main__':
    main()
