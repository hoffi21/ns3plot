# ns3plot
Scripts to plot (gnuplot) and compare NS3 pcap files.

### csv.sh
The "csv" bash script creates the IO statistics via tshark and put them into a separate file.
With some gnuplot magic it will create PNG-files containing the stream IO information.

### compare.sh
To compare different pcaps it does similar magic as csv.sh does....gnuplot is your best friend.

### arrive.sh
Want some arrival curves for network calculus?
Get them here.
Maximum of 3 pcap files at once.
Minimum of 2.

# Usage
./csv.sh foo.pcap

./compare.sh

./arrival.sh foo.pcap bar.pcap test.pcap
