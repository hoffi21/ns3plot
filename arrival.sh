#!/bin/bash

path="graphs/Arrival_Curves/"
start=0
end=710
dataformat=png
kind="arrivalcurve"
j=0
args_num="$#"

if [ $args_num != 2 ]; then
    if [ $args_num == 3 ]; then
        ARG1=$1
        ARG2=$2
        ARG3=$3
    else
        echo "Please provide at least 2 pcap files but not more than 3!"
        echo "e.g.: ./arrival.sh foo.pcap bar.pcap"
        exit
    fi  
else
    ARG1=$1
    ARG2=$2  
fi

for i in "$@";
    do
    j=$((j+1))
    echo '>>>> shark'
    tshark -r $i -qz io,stat,1,tcp.stream==1,ip.src==10.1.2.1 -qz io,stat,1,tcp.stream==0,ip.src==10.1.1.1 | awk -v RS="" '{ print $0 > ".temp" NR }'
    echo '>>>> build'
    paste .temp1 .temp2 > Arrival_TCP_IO_$j
    echo '>>>> clean temp-files'
    rm .temp*
done 

echo '>>>> merge'
if [ $args_num == 3 ]; then
    paste Arrival_TCP_IO_$((args_num-2)) Arrival_TCP_IO_$((args_num-1)) Arrival_TCP_IO_$args_num > Arrival_TCP_IO
else
    paste Arrival_TCP_IO_$((args_num-1)) Arrival_TCP_IO_$args_num > Arrival_TCP_IO
fi
echo '>>>> clean for a greater good'
for (( k=1; k<=$args_num; k++ ))
do
    rm Arrival_TCP_IO_$k
done

echo '>>>> plot'
function plot {
gnuplot <<EOF
	set terminal $dataformat size 900,500
	set output '$path$kind-${start}s-${end}s.$dataformat'
	set datafile separator "|"
	set xrange [$start:$end]
	set yrange [0:9000]
	set xlabel "Zeit(s)"
	set ylabel "Byte/s"
	set style line 1 lt 3 lc rgb "orange" lw 1
	set style line 2 lt 3 lc 3
    set style line 3 lt 4 lc 2
	plot \
	"<(awk 'NR>=13 && NR<=720' Arrival_TCP_IO)" using 0:(\$6+\$12) t '${ARG1}' with lines linestyle 1, \
    "<(awk 'NR>=13 && NR<=720' Arrival_TCP_IO)" using 0:(\$18+\$24) t '${ARG2}' with lines linestyle 2, \
    "<(awk 'NR>=13 && NR<=720' Arrival_TCP_IO)" using 0:(\$30+\$36) t '${ARG3}' with lines linestyle 3
EOF
echo ">>>> finished"
}

function plot2 {
gnuplot <<EOF
	set terminal $dataformat size 900,500
	set output '$path$kind-${start}s-${end}s.$dataformat'
	set datafile separator "|"
	set xrange [$start:$end]
	set yrange [0:9000]
	set xlabel "Zeit(s)"
	set ylabel "Byte/s"
	set style line 1 lt 3 lc rgb "orange" lw 1
	set style line 2 lt 3 lc 3
	plot \
	"<(awk 'NR>=13 && NR<=720' Arrival_TCP_IO)" using 0:(\$6+\$12) t '${ARG1}' with lines linestyle 1, \
    "<(awk 'NR>=13 && NR<=720' Arrival_TCP_IO)" using 0:(\$18+\$24) t '${ARG2}' with lines linestyle 2
EOF
echo ">>>> finished"
}


if [ $# == 3 ]; then
    start=0  ; end=710; plot
    start=0  ; end=30 ; plot
    start=680; end=710; plot
else
    start=0  ; end=710; plot2
    start=0  ; end=30 ; plot2
    start=680; end=710; plot2
fi
mv Arrival_TCP_IO $path$kind.TCP_IO