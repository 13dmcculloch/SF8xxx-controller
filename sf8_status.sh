#!/bin/bash

# To be run from account .profile at login

LOGFILE="/tmp/sf8_status"

if [ ! -d "/run/screen/S-$LOGNAME"]; then
  echo "Screen run directory not present."
  exit
fi
SESSION_NAME=$(ls "/run/screen/S-$LOGNAME" | grep sf8_status)
if [ -z "$SESSION_NAME" ]; then
  screen -qS sf8_status watch cat "$LOGFILE"
  exit
fi
SESSION_COUNT=$(echo $SESSION_NAME | grep " ")
if [ -z "$SESSION_COUNT" ]; then
  screen -x "$SESSION_NAME"
else
  echo "Multiple screen sessions detected."
  exit
fi
