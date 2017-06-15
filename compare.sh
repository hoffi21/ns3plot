#!/bin/bash

############# compare streams #############
# created by: Mario Hoffmann
# year: 2017
###########################################
path="graphs/"
start=0
end=660
dataformat=png
name0="stream0"
name1="stream1"
var="overall"

command -v tshark >/dev/null 2>&1 || { echo >&2 ">>>> tshark is not installed.  Aborting."; exit 1; }
command -v gnuplot >/dev/null 2>&1 || { echo >&2 ">>>> gnuplot is not installed.  Aborting."; exit 1; }

echo '>>>> Create File to plot...'
paste graphs/tcp_flow_hybla-5-5.pcap.TCP_IO graphs/tcp_flow_vegas-5-5.pcap.TCP_IO graphs/tcp_flow_newreno-5-5.pcap.TCP_IO > graphs/overall_TCP_IO

echo '>>>> Plot...'

function plot {
gnuplot <<__EOF
	set terminal $dataformat size 1500,500
	set output '$path$var-$name0-${start}s-${end}s.$dataformat'
	set datafile separator "|"
	set xrange [$start:$end]
	set yrange [0:8000]
	set xlabel "Zeit(s)"
	set ylabel "Byte/s"
	set style line 1 lt 3 lc rgb "orange" lw 1
	set style line 2 lt 3 lc 3
    set style line 3 lt 3 lc rgb "green" lw 1
	plot \
	"<(awk 'NR>=13 && NR<=660' graphs/overall_TCP_IO)" using 0:6 t "Hybla; TCP Stream 0 eq 10.1.1.1 - 10.1.6.1" with lines linestyle 1, \
	"<(awk 'NR>=13 && NR<=660' graphs/overall_TCP_IO)" using 0:12 t "Vegas; TCP Stream 0 eq 10.1.1.1 - 10.1.6.1" with lines linestyle 2, \
    "<(awk 'NR>=13 && NR<=660' graphs/overall_TCP_IO)" using 0:18 t "NewReno; TCP Stream 0 eq 10.1.1.1 - 10.1.6.1" with lines linestyle 3
    set output '$path$var-$name1-${start}s-${end}s.$dataformat
    plot \
    "<(awk 'NR>=675 && NR<=999999' graphs/overall_TCP_IO)" using 0:6 t "Hybla; TCP Stream 0 eq 10.1.2.1 - 10.1.7.1" with lines linestyle 1, \
	"<(awk 'NR>=674 && NR<=999999' graphs/overall_TCP_IO)" using 0:12 t "Vegas; TCP Stream 0 eq 10.1.2.1 - 10.1.7.1" with lines linestyle 2, \
    "<(awk 'NR>=675 && NR<=999999' graphs/overall_TCP_IO)" using 0:18 t "NewReno; TCP Stream 0 eq 10.1.2.1 - 10.1.7.1" with lines linestyle 3
__EOF
#0:6 --> plotte Spalte 0 gegen Spalte 6...
#awk Befehl definiert ab welcher Zeile gelesen werden soll. --> erspart das Erstellen von .temp-Files
echo ">>>> Finished..."
}

start=0  ; end=660; plot
start=0  ; end=25 ; plot
start=625; end=660; plot
