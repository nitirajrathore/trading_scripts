
trade_input_file=$1
ho=$2   # previous heiken ashi open 
hh=$3    # previous heiken ashi high
hl=$4    # previous heiken ashi low
hc=$5    # previous heiken ashi close

python reverse_file.py -if "$trade_input_file" -of "$trade_input_file.reverse.csv" && \
python to_heikin_ashi.py -if "$trade_input_file.reverse.csv" --date-column 1  --open-column 2 --high-column 3 --low-column 4 --close-column 5 --open-value $ho --high-value $hh --low-value $hl --close-value $hc -of "$trade_input_file.heiken.csv" && \ 
python daily_to_weekly_candle.py -if "$trade_input_file.heiken.csv" --date-column 5 --open-column 1 --high-column 2 --low-column 3 --close-column 4 --output-file "$trade_input_file.heiken.weekly.csv" --no-headers && \
python set_candle_color.py -if "$trade_input_file.heiken.weekly.csv" -of "$trade_input_file.heiken.color.csv" --close-column 4 && \
python simulate_heikin_ashi.py -hf "$trade_input_file.heiken.color.csv" -tf "$trade_input_file.reverse.csv" --end-date-column 6 --trade-date-column 1 --trade-close-column 5 --heiken-color-column 7  --output-file "$trade_input_file.simulation.result.csv"



