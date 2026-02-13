def data_types():
    a = 1
    b = "a"
    c = 1.0
    d = True
    e = []
    f = {}
    g = ()
    h = set()

    types = [type(x).__name__ for x in (a, b, c, d, e, f, g, h)]
    print("[" + ", ".join(types) + "]")

if __name__ == '__main__':
    data_types()
