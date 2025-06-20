#!/bin/bash

{
  cron -f -L 15 -x bit 2>&1 | while IFS= read -r line
  do
    timestamp=$(date +"%Y-%m-%d %H:%M:%S,%3N")
    echo "$timestamp INFO    [cron] $line"
  done
} 2>&1 | tee -a /proc/1/fd/1 >> /data/log/cron.log