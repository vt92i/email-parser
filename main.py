from datetime import datetime
import argparse, time, sys, os, re


class App():
    class ArgParser(argparse.ArgumentParser):
        def error(self, message):
            self.print_help()
            sys.exit()

    def __init__(self):
        self.totalLines = 0
        self.totalExtracted = 0
        self.extractedEmail = []
        self.outputDir = os.path.join("output")

    def run(self):
        parser = self.ArgParser(description='Extract all valid email from given data', add_help=True, exit_on_error=False)
        parser.add_argument("-i", "--input", dest="inputfile", metavar="\b", type=str, help="a .txt input file", required=True)
        try:
            if len(sys.argv) == 1:
                parser.print_help()
                sys.exit()
            file = parser.parse_args().inputfile
            if (os.path.exists(file) and os.path.isfile(file) and (os.path.splitext(file)[len(os.path.splitext(file)) - 1] == ".txt")):
                time_start = time.perf_counter()
                with open(file=file, mode="r", encoding="utf-8", errors="ignore") as f:
                    for email in f.readlines():
                        self.totalLines += 1
                        j = re.search(r"([a-z0-9_.+-]+[@]+[a-z0-9-]+[.]+[a-z.]+)", email, re.I)
                        if j:
                            self.extractedEmail.append(j.group())
                            self.totalExtracted += 1
                    f.close()
                if not os.path.isdir(self.outputDir):
                    os.mkdir(self.outputDir)
                timenow = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
                output_file = f"{os.path.splitext(file)[0]}_{timenow}.txt"
                with open(file=os.path.join(self.outputDir, output_file), mode="w", encoding="utf-8") as f:
                    for n in range(len(self.extractedEmail)):
                        f.write(f"{self.extractedEmail[n]}\n")
                        print(n, self.extractedEmail[n])
                    f.close()
                time_end = time.perf_counter()
                print()
                print(f"Done in {time_end - time_start:.2f}s")
                print(f"Total lines: {self.totalLines}")
                print(f"Total extracted: {self.totalExtracted}")
            else:
                sys.exit("Please, check your input file.")
        except argparse.ArgumentError:
            parser.print_help()
            sys.exit()


if __name__ == "__main__":
    try:
        App().run()
    except KeyboardInterrupt:
        sys.exit()
