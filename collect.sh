#!/bin/bash

STATE="rn"
DOWNLOAD_PATH="download"
OUTPUT_PATH="output"
LOG_PATH="log"

mkdir -p $DOWNLOAD_PATH $OUTPUT_PATH $LOG_PATH


log_filename="$LOG_PATH/caso-${STATE}.log"
csv_filename="$OUTPUT_PATH/caso-${STATE}.csv"
rm -rf "$log_filename" "$csv_filename"
time scrapy runspider \
    --loglevel=INFO \
    --logfile="$log_filename" \
    -o "$csv_filename" \
    corona_rn_spider.py
