import argparse
import sys
from datetime import datetime


weekdays_array = ["Monday", "Tuesday", "Wednessday", "Thursday", "Friday", "Saturday", "Sunday"]


def log(msg, type="warn"):
    print("type: " + msg, file=sys.stderr)


def write_line(output_file, line):
    if output_file is not None:
        output_file.write(line)
    else:
        print(line, end='')


def write_data(output_file, ohlc, curr_date, date_fmt):
    line = f"{ohlc.open},{ohlc.high},{ohlc.low},{ohlc.close},{curr_date.strftime(date_fmt)}\n"
    write_line(output_file, line)
    
    
class ohlc:
    def __init__(self, open_value, high, low, close):
        self.open = float(open_value)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)


def main(file_path, close_column, open_column, output_file, no_headers, ):
    line_no = 0
    first_line = True

    with open(file_path, "r") as input_file:
        for line in input_file:
            log(f"read line : {line}")
            line_no = line_no + 1
            if line_no == 1 and not no_headers:
                continue

            cols = line.strip().split(',')
            curr_close = cols[close_column]
            curr_open = cols[open_column]

            if not first_line:
                color = decide_candle_color(curr_open, curr_close)
                write_line(output_file, f"{line.strip()},{color}\n")

            first_line = False


def decide_candle_color(curr_open, curr_close):
    return "green" if curr_open < curr_close else "red"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=''' '''
    )

    parser.add_argument('-if', '--file-path', help='file-path', default=None, required=True)
    parser.add_argument('-cc', '--close-column', help='close-column', default=4, type=int, required=False)
    parser.add_argument('-oc', '--open-column', help='open-column', default=1, type=int, required=False)
    parser.add_argument('-of', '--output-file', help='output-file', required=False)
    parser.add_argument('-nh', '--no-headers', help='always assumes headers, set this to say no headers',
                        action='store_true', required=False)

    args = parser.parse_args()

    if args.output_file is None:
        main(args.file_path, args.close_column - 1, args.open_column - 1, None, args.no_headers)
    else:
        with open(args.output_file, "w") as out_file:
            main(args.file_path, args.close_column - 1, args.open_column - 1, out_file, args.no_headers)

