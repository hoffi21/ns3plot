#!/bin/bash

############# plot pcap throughput #############
# created by: Philipp Dockhorn
# edited by: Mario Hoffmann
# year : 2017
################################################

path="graphs/"
start=0
end=660
dataformat=png

command -v tshark >/dev/null 2>&1 || { echo >&2 ">>>> tshark is not installed.  Aborting."; exit 1; }
command -v gnuplot >/dev/null 2>&1 || { echo >&2 ">>>> gnuplot is not installed.  Aborting."; exit 1; }

if  [ $# != 1 ]
	then
	echo "pls offer a pcap-file like:"
	echo "./csv.sh test.pcap"

	exit
fi
bild="${1%.*}"

echo '>>>> Create an csv for plotting...'
tshark -r $1 -qz io,stat,1,tcp.stream==1,ip.src==10.1.2.1 -qz io,stat,1,tcp.stream==0,ip.src==10.1.1.1 > TCP_IO

echo '>>>> Plot...'

function plot {
gnuplot <<__EOF
	set terminal $dataformat size 1500,500
	set output '$path$bild-${start}s-${end}s.$dataformat'
	set datafile separator "|"
	set xrange [$start:$end]
	set yrange [0:8000]
	set xlabel "Zeit(s)"
	set ylabel "Byte/s"
	set style line 1 lt 3 lc rgb "orange" lw 1
	set style line 2 lt 3 lc 3
	plot \
	"<(awk 'NR>=13 && NR<=999999' TCP_IO)" using 0:6 t "TCP Stream 0 eq 10.1.1.1 --> 10.1.6.1" with lines linestyle 1, \
	"<(awk 'NR>=674 && NR<=999999' TCP_IO)" using 0:6 t "TCP Stream 1 eq 10.1.2.1 --> 10.1.7.1" with lines linestyle 2
__EOF
#0:6 --> plotte Spalte 0 gegen Spalte 6...
#awk Befehl definiert ab welcher Zeile gelesen werden soll. --> erspart das Erstellen von .temp-Files
echo ">>>> Finished..."
}

start=0  ; end=660; plot
start=0  ; end=25 ; plot
start=625; end=660; plot
mv TCP_IO $path$1.TCP_IO