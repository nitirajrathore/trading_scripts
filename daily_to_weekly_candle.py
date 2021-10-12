import argparse
import sys
from datetime import datetime


weekdays_array = ["Monday", "Tuesday", "Wednessday", "Thursday", "Friday", "Saturday", "Sunday"]

def log(msg, type="warn"):
    print("type: " + msg, file=sys.stderr)


def write_data(output_file, open_value, high, low, close, week_start_date, previous_date, date_format):
    line = f"{open_value},{high},{low},{close},{week_start_date.strftime(date_format)},{previous_date.strftime(date_format)}\n"
    if output_file is not None:
        output_file.write(line)
    else:
        print(line, end='')


def main(file_path, date_column, open_column, high_column, low_column,  close_column, date_format, output_file, 
         formula, no_headers):
    print("Ohlc columns : ")
    print(open_column, high_column, low_column,  close_column)
    line_no = 0
    first_line = True
    current_week = 0
    previous_date = None
    lows = []
    highs = []
    closes = []
    opens = []
    week_start_date = None

    with open(file_path, "r") as input_file:
        for line in input_file:
            log(f"read line : {line}")
            line_no = line_no + 1
            if line_no == 1 and not no_headers:
                continue

            cols = line.strip().split(',')
            date_str = cols[date_column]
            curr_date = datetime.strptime(date_str, date_format)
            week = curr_date.isocalendar()[1] #int(curr_date.strftime("%W"))
            year, weekday = curr_date.year, curr_date.weekday()

            if first_line:
                week_start_date = curr_date
                current_week = week
    
            if first_line and weekday != 0:
                log(f"File does not start with a monday. First line starts with {date_str} which is {weekdays_array[weekday]}")
    
            if weekday == 5 or weekday == 6:
                log(f"File contains {weekdays_array[weekday]} data for day {curr_date} at line number {line_no}")
    
            # if week < current_week:
            #     # this date's week cannot be smaller than current week unless its a different year.
            #     if previous_date is not None and previous_date.year == year:
            #         raise Exception(f"this date's week {week} cannot be smaller than current week {current_week} for the same year {year}")
    
            if week != current_week:
                open_value, high, low, close = formula(opens, highs, lows, closes)
                write_data(output_file, open_value, high, low, close, week_start_date, previous_date, date_format)
                lows = []
                highs = []
                closes = []
                opens = []
                current_week = week
                week_start_date = curr_date
    
            lows.append(float(cols[low_column]))
            highs.append(float(cols[high_column]))
            opens.append(float(cols[open_column]))
            closes.append(float(cols[close_column]))
    
            previous_date = curr_date
            first_line = False

    open_value, high, low, close = formula(opens, highs, lows, closes)
    write_data(output_file, open_value, high, low, close, week_start_date, previous_date, date_format)


def weekly_candle(opens, highs, lows, closes):
    # print(f" opens {opens} \n  highs = {highs} \n lows : {lows} \n closes : {closes} \n")
    return opens[0], max(highs + closes + opens), min(lows + closes + opens), closes[-1]


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
    parser.add_argument('-of', '--output-file', help='output-file', required=False)
    parser.add_argument('-nh', '--no-headers', help='always assumes headers, set this to say no headers',
                        action='store_true', required=False)

    args = parser.parse_args()

    if args.output_file is None:
        main(args.file_path, args.date_column - 1, args.open_column - 1, args.high_column - 1,  args.low_column - 1, 
             args.close_column - 1, args.date_format,
             None, 
             # sys.stdout if args.output_file is None else open(args.output_file), 
             weekly_candle, args.no_headers)
    else:
        with open(args.output_file, "w") as out_file:
            main(args.file_path, args.date_column - 1, args.open_column - 1, args.high_column - 1, args.low_column - 1,
                 args.close_column - 1, args.date_format,
                 out_file,
                 weekly_candle, args.no_headers)

