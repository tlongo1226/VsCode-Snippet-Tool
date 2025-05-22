import sys

def escape_line(line):
    return '"' + line.replace('\\', '\\\\').replace('"', '\\"') + '",'

def main():
    for line in sys.stdin:
        print(escape_line(line.rstrip()))

if __name__ == "__main__":
    main()
