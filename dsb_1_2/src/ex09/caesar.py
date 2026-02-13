import sys

def has_cyrillic(s):
    return any('\u0400' <= ch <= '\u04FF' or '\u0500' <= ch <= '\u052F' for ch in s)

def shift_char(ch, k):
    if 'a' <= ch <= 'z':
        return chr((ord(ch) - 97 + k) % 26 + 97)
    if 'A' <= ch <= 'Z':
        return chr((ord(ch) - 65 + k) % 26 + 65)
    return ch

def caesar(text, k):
    return ''.join(shift_char(ch, k) for ch in text)

def main():
    if len(sys.argv) != 4:
        raise Exception("Wrong arguments")
    mode, text, k_str = sys.argv[1], sys.argv[2], sys.argv[3]
    if has_cyrillic(text):
        raise Exception("The script does not support your language yet.")
    k = int(k_str)
    if mode == "encode":
        print(caesar(text, k))
    elif mode == "decode":
        print(caesar(text, -k))
    else:
        raise Exception("Wrong arguments")

if __name__ == '__main__':
    main()
