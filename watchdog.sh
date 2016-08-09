#!/bin/bash

mkdir -p "$HOME/tmp"
PIDFILE = "$HOME/tmp/lever-arena.pid"

if [ -e "${PIDFILE}" ] && (ps -u $(whoami) -opid= | grep -P "^\s*$(cat ${PIDFILE})$" &> /dev/null); then
	exit 99
fi

/home/pi/Desktop/lever-arena/lever-arena.py > $HOME/tmp/lever-arena.log & chmod 644 "${PIDFILE}"
