import argparse
import sys
from datetime import datetime


def log(msg, type="warn"):
    print("type: " + type + " | " + msg, file=sys.stderr)


def write_line(output_file, line):
    print(f"writing line : {line}")
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


def main(heiken_file_path, trade_file_path, date_format, end_date_column, trade_date_column,
              trade_close_column, heiken_color_column, out_file, no_headers ):
    line_no = 0

    daily_map = dict()
    with open(trade_file_path, 'r') as trade_file:
        for line in trade_file:
            line_no = line_no + 1
            if line_no == 1 and not no_headers:
                continue

            cols = line.strip().split(',')
            curr_date = datetime.strptime(cols[trade_date_column], date_format)
            daily_map[curr_date] = cols

    curr_amt = 100.0
    curr_stocks = 0
    prev_color = None
    with open(heiken_file_path, "r") as heiken_file:
        for line in heiken_file:
            log(f"read line : {line}")
            line = line.strip()
            cols = line.split(',')
            curr_color = cols[heiken_color_column]
            curr_date = datetime.strptime(cols[end_date_column], date_format)
            trade_cols = daily_map[curr_date]
            curr_close = float(trade_cols[trade_close_column])
            log(f"curr_color : {curr_color}")
            action = "none"
            if curr_color == "green":
                if prev_color is not None and prev_color == "green":
                    log("previous was not None and green, so continue this time.")
                    action = "none" 
                    continue
                else:
                    log("else of green.")
                    curr_stocks = curr_amt/curr_close
                    curr_amt = 0
                    prev_color = "green"
                    action = "buy"

            if curr_color == "red":
                if prev_color is None or prev_color == "red":
                    log("previous is None or red, so continue this time.")
                    action = "none"
                    continue
                else:
                    log("else in red")
                    curr_amt = curr_stocks * curr_close
                    curr_stocks = 0
                    prev_color = "red"
                    action = "sell"
            write_line(out_file, ",".join(trade_cols) + ",|," + ",".join(cols) + ",|," + f"{action},{curr_amt},{curr_stocks}\n")
            
        if prev_color == "green":
            curr_amt = curr_stocks * curr_close
            curr_stocks = 0
            write_line(out_file, ",".join(trade_cols) + ",|," + ",".join(cols) + ",|," + f"sell,{curr_amt},{curr_stocks}\n")            


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=''' '''
    )

    parser.add_argument('-hf', '--heiken-file-path', help='file-path', default=None, required=True)
    parser.add_argument('-tf', '--trade-file-path', help='file-path', default=None, required=True)
    parser.add_argument('-df', '--date-format', help='date-format', default="%d-%B-%Y", required=False)
    parser.add_argument('-edc', '--end-date-column', help='end-date-column', default=1, type=int, required=False)
    parser.add_argument('-dc', '--trade-date-column', help='trade-date-column', default=1, type=int, required=False)
    parser.add_argument('-tcc', '--trade-close-column', help='trade-close-column', default=5, type=int, required=False)
    parser.add_argument('-hcc', '--heiken-color-column', help='heiken-color-column', default=6, type=int, required=False)
    parser.add_argument('-of', '--output-file', help='output-file', required=False)
    parser.add_argument('-nh', '--no-headers', help='always assumes headers, set this to say no headers', action='store_true', required=False)

    args = parser.parse_args()

    if args.output_file is None:
        main(args.heiken_file_path, args.trade_file_path, args.date_format, args.end_date_column - 1, args.trade_date_column - 1,
             args.trade_close_column - 1, args.heiken_color_column - 1, 
             None, args.no_headers)
    else:
        with open(args.output_file, "w") as out_file:
            main(args.heiken_file_path, args.trade_file_path, args.date_format, args.end_date_column - 1, args.trade_date_column - 1,
                 args.trade_close_column - 1, args.heiken_color_column - 1, 
                 out_file, args.no_headers)

