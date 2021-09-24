
trade_input_file=$1
ho=$2   # previous heiken ashi open 
hh=$3    # previous heiken ashi high
hl=$4    # previous heiken ashi low
hc=$5    # previous heiken ashi close

python to_heikin_ashi.py -if "$trade_input_file.csv" --date-format "%Y-%m-%d" --date-column 1  --open-column 2 \
--high-column 3 --low-column 4 --close-column 5 --open-value $ho --high-value $hh \
--low-value $hl --close-value $hc -of "$trade_input_file.heiken.csv" && \ 
python set_heikenashi_candle_color.py -if "$trade_input_file.heiken.csv" \
-of "$trade_input_file.heiken.color.csv" --close-column 4 --open-column 1 --no-headers && \
python simulate_heikin_ashi.py -hf "$trade_input_file.heiken.color.csv" -tf "$trade_input_file.csv" \
--end-date-column 5 --date-format "%Y-%m-%d" --trade-date-column 1 --trade-close-column 5 --heiken-color-column 6  \
--output-file "$trade_input_file.simulation.result.csv"



