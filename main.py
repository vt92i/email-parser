import argparse, sys, os, re

parser = argparse.ArgumentParser(description='Extract all email from combos', add_help=False)
totalLines, totalExtracted = 0, 0


def getInputFile():
    parser.add_argument('-i', metavar="input_file", type=str, dest="inputfile", required=True)
    args = parser.parse_args().inputfile
    if (os.path.exists(args) and os.path.isfile(args) and (os.path.splitext(args)[len(os.path.splitext(args)) - 1] == ".txt")):
        return args
    else:
        sys.exit("Please, check your input file.")


def extractAllEmail(i):
    global totalLines, totalExtracted
    with open(file=i, mode="r", encoding="utf-8", errors="ignore") as f:
        extracted = []
        for email in f.readlines():
            totalLines += 1
            j = re.search(r"([a-z0-9_.+-]+[@]+[a-z0-9-]+[.]+[a-z.]+)", email, re.I)
            if j:
                extracted.append(j.group())
                totalExtracted += 1
    return extracted


def saveFile(o):
    with open(file="out.txt", mode="w", encoding="utf-8") as f:
        for item in o:
            f.write(f"{item}\n")
            print(item)
        f.close()
    print(f"\nTotal lines: {totalLines}")
    print(f"Total extracted: {totalExtracted}\n")


if __name__ == "__main__":
    try:
        saveFile(extractAllEmail(getInputFile()))
    except KeyboardInterrupt:
        sys.exit()
