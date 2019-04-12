#!/bin/bash
# basic test of performance of exporter & WLC responsivnes
#
# ./benchmark.sh fortiwlc_exporter.yaml wlc1.anso.arnes.si wlc2.anso.arnes.si \
#   wlc3.anso.arnes.si wlc4.anso.arnes.si wlc5.anso.arnes.si \
#   wlc6.anso.arnes.si wlc7.anso.arnes.si wlc8.anso.arnes.si \
#   wlc9.anso.arnes.si wlc10.anso.arnes.si wlc11.anso.arnes.si \
#   wlc12.anso.arnes.si wlc13.anso.arnes.si wlc14.anso.arnes.si
#
CONFIG=${1:-fortiwlc_exporter.yaml}
WLC_LIST=("${@:2}")

if [[ "$CONFIG" == "-h" ]]; then
    echo "Usage $0 [config.yaml] [rounds]"
    echo
    echo "Run benchmark on foritwlc_exporter"
    exit 0
fi

echo "running benchmark; config=${CONFIG}"

poetry run python fortiwlc_exporter/exporter.py -c $CONFIG --debug 2>/dev/null &
SPID=$!
echo exporter pid: $SPID

function finish {
    pkill -P $SPID
}
trap finish EXIT

sleep 2

echo "running benchmark"

time printf '%s\n' "${WLC_LIST[@]}" | xargs -n1 -P30 -i curl -s -w "{}: %{time_total}\n" "http://localhost:9118/probe?target={}" -o /dev/null

echo "____________________________________________________"
