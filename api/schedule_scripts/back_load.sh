#!/bin/bash

start_time=1685947453
week_s=604800


# File to store the counter
counter_file="run_count.txt"

# If the counter file doesn't exist, create it with an initial value of 0
if [ ! -f $counter_file ]; then
    echo 0 > $counter_file
fi

# Read the current counter value from the file
counter=$(cat $counter_file)

s_t=$((start_time - (counter * week_s)))

curl -X 'POST' \
  "localhost/load_vivacity/?delta_t=704800&end_t=${s_t}" \
  -H 'accept: application/json' \
  -H "access_token: ${EXTERNAL_API_TOKEN}" \
  -d ''

# Increment the counter by 1
counter=$((counter + 1))

# Save the new counter value back to the file
echo $counter > $counter_file

# Output the current run number
echo "This script has been run $counter times. Start Time: $s_t "


