import argparse
import sys
from datetime import datetime


weekdays_array = ["Monday", "Tuesday", "Wednessday", "Thursday", "Friday", "Saturday", "Sunday"]

def log(msg, type="warn"):
    print("type: " + msg, file=sys.stderr)


def write_data(output_file, ohlc, curr_date, date_fmt):
    line = f"{ohlc.open},{ohlc.high},{ohlc.low},{ohlc.close},{curr_date.strftime(date_fmt)}\n"
    if output_file is not None:
        output_file.write(line)
    else:
        print(line, end='')

class ohlc:
    def __init__(self, open_value, high, low, close):
        self.open = float(open_value)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)
    
def main(file_path, date_column, low_column, high_column, open_column, close_column, previous_heiken_ohlc, date_format, output_file, no_headers):
    line_no = 0
    first_line = True
    
    with open(file_path, "r") as input_file:
        for line in input_file:
            log(f"read line : {line}")
            line_no = line_no + 1
            if line_no == 1 and not no_headers:
                continue

            cols = line.strip().split(',')
            date_str = cols[date_column]
            curr_date = datetime.strptime(date_str, date_format)
            year, weekday = curr_date.year, curr_date.weekday()
            curr_ohlc = ohlc(cols[open_column], cols[high_column], cols[low_column], cols[close_column])

            if first_line and weekday != 0:
                log(f"File does not start with a monday. First line starts with {date_str} which is {weekdays_array[weekday]}")

            if weekday == 5 or weekday == 6:
                log(f"File contains {weekdays_array[weekday]} data for day {curr_date} at line number {line_no}")

            hieken_ashi_ohlc = hieken_ashi(previous_heiken_ohlc, curr_ohlc)
            write_data(output_file, hieken_ashi_ohlc, curr_date, date_format)

            first_line = False
            previous_heiken_ohlc = hieken_ashi_ohlc


def hieken_ashi(previous_heiken_ohlc, curr_ohlc):
    # print(f" previous_day_ohlc {previous_day_ohlc} \n  curr_ohlc : {curr_ohlc}")
    o = (previous_heiken_ohlc.open + previous_heiken_ohlc.close)/2
    c = 1/4*(curr_ohlc.high + curr_ohlc.low + curr_ohlc.open + curr_ohlc.close)
    h = max(curr_ohlc.high, o, c)
    l = min(curr_ohlc.low, o, c)
    return ohlc(o,h,l,c)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''given a csv file containing daily low high open close values, convert it to weekly csv values. 
        with monday as a weekly start date and friday as weekly end date. If friday data is not available then previous
        day is considered weekly end date ( not implemented yet) '''
    )

    parser.add_argument('-if', '--file-path', help='file-path', default=None, required=True)
    parser.add_argument('-df', '--date-format', help='date-format', default="%d-%B-%Y", required=False)
    parser.add_argument('-dc', '--date-column', help='date-column', default=1, type=int, required=False)
    parser.add_argument('-lc', '--low-column', help='low-column', default=4, type=int, required=False)
    parser.add_argument('-hc', '--high-column', help='high-column', default=3, type=int, required=False)
    parser.add_argument('-oc', '--open-column', help='open-column', default=2, type=int, required=False)
    parser.add_argument('-cc', '--close-column', help='close-column', default=5, type=int, required=False)
    parser.add_argument('-lv', '--low-value', help='last low-value', type=float, required=True)
    parser.add_argument('-hv', '--high-value', help='last high-value', type=float, required=True)
    parser.add_argument('-ov', '--open-value', help='last open-value', type=float, required=True)
    parser.add_argument('-cv', '--close-value', help='last close-value',  type=float, required=True)
    parser.add_argument('-of', '--output-file', help='output-file', required=False)
    parser.add_argument('-nh', '--no-headers', help='always assumes headers, set this to say no headers',
                        action='store_true', required=False)

    args = parser.parse_args()
    previous_heiken_ohlc = ohlc(args.open_value, args.high_value, args.low_value, args.close_value)
    if args.output_file is None:
        main(args.file_path, args.date_column - 1, args.low_column - 1, args.high_column - 1, args.open_column - 1,
             args.close_column - 1, previous_heiken_ohlc, args.date_format,
             None,
            args.no_headers)
    else:
        with open(args.output_file, "w") as out_file:
            main(args.file_path, args.date_column - 1, args.low_column - 1, args.high_column - 1, args.open_column - 1,
                 args.close_column - 1, previous_heiken_ohlc, args.date_format,
                 out_file, args.no_headers)

