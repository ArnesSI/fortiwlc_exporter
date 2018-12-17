#!/bin/bash

ROUNDS=${2:-3}
CONFIG=${1:-fortiwlc_exporter.ini}

if [[ "$CONFIG" == "-h" ]]; then
    echo "Usage $0 [config.ini] [rounds]"
    echo
    echo "Run benchmark on foritwlc_exporter"
    exit 0
fi

echo "running benchmark; config=${CONFIG}; rounds=${ROUNDS}"

pipenv run python fortiwlc_exporter/server.py -c $CONFIG --debug &
SPID=$!

function finish {
    kill $SPID
}
trap finish EXIT

sleep 2
for i in $(seq ${ROUNDS}); do
echo "#### ROUND $i"
curl -s -w "
            time_namelookup:  %{time_namelookup}
               time_connect:  %{time_connect}
            time_appconnect:  %{time_appconnect}
           time_pretransfer:  %{time_pretransfer}
              time_redirect:  %{time_redirect}
         time_starttransfer:  %{time_starttransfer}
                            ----------
                 time_total:  %{time_total}
" "http://localhost:9118/" -o /dev/null
echo "____________________________________________________"
done
