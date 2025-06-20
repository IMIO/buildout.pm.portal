#!/bin/bash

{
  SITE_ID="$1"
  timestamp=$(date +"%Y-%m-%d %H:%M:%S,%3N")
  label="[cron.tick_fifteen]"
  response=$(curl -s -m 10 --netrc-file /plone/.netrc http://localhost:8081/$SITE_ID/@@tick_fifteen)

  exit_code=$?
  if [ $exit_code -eq 0 ]; then
      echo "$timestamp INFO    $label Tick $SITE_ID/@@tick_fifteen: $response"
  else
      echo "$timestamp ERROR   $label Failed to tick (exit $exit_code)"
      echo "$timestamp ERROR   $label Response: $response"
  fi
} 2>&1 | tee -a /proc/1/fd/1 >> /data/log/cron.log