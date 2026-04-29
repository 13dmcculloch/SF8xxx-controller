#!/bin/bash

LOGFILE="/tmp/sf8_status"

# start sf8 status session if not in existence
if [ ! -d "/run/screen/S-$LOGNAME"]; then
  echo "Screen run directory not present."
  exit
fi
# start detached sf8 status session
if [ -z "$(ls "/run/screen/S-$LOGNAME" | grep sf8_status)" ]; then
  screen -qdmS sf8_status watch cat "$LOGFILE"
fi
SESSION_NAME=$(ls "/run/screen/S-$LOGNAME" | grep sf8_status)

./SF8xxx-controller.py "$LOGFILE"

screen -X -S "$SESSION_NAME" exit
