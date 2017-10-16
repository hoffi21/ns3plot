##### NS3 TCP dumbbell example ######
#####################################
#provided by: Marion Hoffmann [2017]#
#####################################

import ns.core
import ns.network
import ns.internet
import ns.visualizer
import ns.point_to_point
import ns.applications
import sys
import os
import shutil

######################################################################################################

#CommandLine for --visualize
cmd = ns.core.CommandLine()
cmd.verbose = "True"
cmd.Parse(sys.argv)

starttime = 0
endtime = 600 

for start, ende in zip((1,1), (25,600)):
	starttime = start
	endtime = starttime + ende 

for x in ["NewReno", "Hybla", "Vegas"]:
	pass
	alg = 'ns3::Tcp' + x
	filename = x; ns.core.Config.SetDefault("ns3::TcpL4Protocol::SocketType", ns.core.StringValue(alg))

	######################################################################################################

	#Create Nodes NodeContainer
	c = ns.network.NodeContainer()
	c.Create(10)
	n0n1 = ns.network.NodeContainer(ns.network.NodeContainer(c.Get(0)), ns.network.NodeContainer(c.Get(1)))

	n0n2 = ns.network.NodeContainer(ns.network.NodeContainer(c.Get(0)), ns.network.NodeContainer(c.Get(2)))
	n0n3 = ns.network.NodeContainer(ns.network.NodeContainer(c.Get(0)), ns.network.NodeContainer(c.Get(3)))

	n0n4 = ns.network.NodeContainer(ns.network.NodeContainer(c.Get(0)), ns.network.NodeContainer(c.Get(4)))
	n0n5 = ns.network.NodeContainer(ns.network.NodeContainer(c.Get(0)), ns.network.NodeContainer(c.Get(5)))

	n1n6 = ns.network.NodeContainer(ns.network.NodeContainer(c.Get(1)), ns.network.NodeContainer(c.Get(6)))
	n1n7 = ns.network.NodeContainer(ns.network.NodeContainer(c.Get(1)), ns.network.NodeContainer(c.Get(7)))

	n1n8 = ns.network.NodeContainer(ns.network.NodeContainer(c.Get(1)), ns.network.NodeContainer(c.Get(8)))
	n1n9 = ns.network.NodeContainer(ns.network.NodeContainer(c.Get(1)), ns.network.NodeContainer(c.Get(9)))

	######################################################################################################
	
	#Internet Stack
	internetstack = ns.internet.InternetStackHelper()
	internetstack.Install(c)

	######################################################################################################
	
	#Channel Infos
	pointToPoint = ns.point_to_point.PointToPointHelper()
	pointToPoint.SetDeviceAttribute("DataRate", ns.core.StringValue("500kb/s"))
	pointToPoint.SetChannelAttribute("Delay", ns.core.StringValue("2ms"))

	bottle = ns.point_to_point.PointToPointHelper()
	bottle.SetDeviceAttribute("DataRate", ns.core.StringValue("100kb/s"))
	bottle.SetChannelAttribute("Delay", ns.core.StringValue("2ms"))

	devices01 = bottle.Install(n0n1)

	devices02 = pointToPoint.Install(n0n2)
	devices03 = pointToPoint.Install(n0n3)

	devices04 = pointToPoint.Install(n0n4)
	devices05 = pointToPoint.Install(n0n5)

	devices16 = pointToPoint.Install(n1n6)
	devices17 = pointToPoint.Install(n1n7)

	devices18 = pointToPoint.Install(n1n8)
	devices19 = pointToPoint.Install(n1n9)

	######################################################################################################
	
	#IP Addresses
	address01 = ns.internet.Ipv4AddressHelper()
	address01.SetBase(ns.network.Ipv4Address("10.1.1.0"), ns.network.Ipv4Mask("255.255.255.0"))
	interfaces01 = address01.Assign (devices01);

	address02 = ns.internet.Ipv4AddressHelper()
	address02.SetBase(ns.network.Ipv4Address("10.1.2.0"), ns.network.Ipv4Mask("255.255.255.0"))
	interfaces02 = address02.Assign (devices02);

	address03 = ns.internet.Ipv4AddressHelper()
	address03.SetBase(ns.network.Ipv4Address("10.1.3.0"), ns.network.Ipv4Mask("255.255.255.0"))
	interfaces03 = address03.Assign (devices03);

	address04 = ns.internet.Ipv4AddressHelper()
	address04.SetBase(ns.network.Ipv4Address("10.1.4.0"), ns.network.Ipv4Mask("255.255.255.0"))
	interfaces04 = address04.Assign (devices04);

	address05 = ns.internet.Ipv4AddressHelper()
	address05.SetBase(ns.network.Ipv4Address("10.1.5.0"), ns.network.Ipv4Mask("255.255.255.0"))
	interfaces05 = address05.Assign (devices05);

	address16 = ns.internet.Ipv4AddressHelper()
	address16.SetBase(ns.network.Ipv4Address("10.1.6.0"), ns.network.Ipv4Mask("255.255.255.0"))
	interfaces16 = address16.Assign (devices16);

	address17 = ns.internet.Ipv4AddressHelper()
	address17.SetBase(ns.network.Ipv4Address("10.1.7.0"), ns.network.Ipv4Mask("255.255.255.0"))
	interfaces17 = address17.Assign (devices17);

	address18 = ns.internet.Ipv4AddressHelper()
	address18.SetBase(ns.network.Ipv4Address("10.1.8.0"), ns.network.Ipv4Mask("255.255.255.0"))
	interfaces18 = address18.Assign (devices18);

	address19 = ns.internet.Ipv4AddressHelper()
	address19.SetBase(ns.network.Ipv4Address("10.1.9.0"), ns.network.Ipv4Mask("255.255.255.0"))
	interfaces19 = address19.Assign (devices19);

	######################################################################################################
	
	#GlobalRouting
	ns.internet.Ipv4GlobalRoutingHelper.PopulateRoutingTables()

	#############################################################################################
	
	# TCP-Connection Node <---> Node
	# Hinweis: nutze nullege.com

	# N2 <--TCP--> N9 (TCP0)
	port = 8080
	onoff = ns.applications.OnOffHelper("ns3::TcpSocketFactory", ns.network.Address(ns.network.InetSocketAddress(ns.network.Ipv4Address("10.1.9.2"), port)))
	onoff.SetConstantRate (ns.network.DataRate ("500kb/s"))
	app = onoff.Install(ns.network.NodeContainer(c.Get(2)))
	app.Start(ns.core.Seconds(starttime))
	app.Stop(ns.core.Seconds(endtime))
	#Sink 
	sink = ns.applications.PacketSinkHelper("ns3::TcpSocketFactory", ns.network.InetSocketAddress(ns.network.Ipv4Address.GetAny(), port))
	app2 = sink.Install(ns.network.NodeContainer(c.Get(9)))
	app2.Start(ns.core.Seconds(0.0))

	# N3 <--TCP--> N8 (TCP1)
	port = 8080
	onoff = ns.applications.OnOffHelper("ns3::TcpSocketFactory", ns.network.Address(ns.network.InetSocketAddress(ns.network.Ipv4Address("10.1.8.2"), port)))
	onoff.SetConstantRate (ns.network.DataRate ("500kb/s"))
	app = onoff.Install(ns.network.NodeContainer(c.Get(3)))
	app.Start(ns.core.Seconds(starttime))
	app.Stop(ns.core.Seconds(endtime))
	#Sink 
	sink = ns.applications.PacketSinkHelper("ns3::TcpSocketFactory", ns.network.InetSocketAddress(ns.network.Ipv4Address.GetAny(), port))
	app2 = sink.Install(ns.network.NodeContainer(c.Get(8)))
	app2.Start(ns.core.Seconds(0.0))

	# N4 <--UDP--> N7
	echoClient = ns.applications.UdpEchoClientHelper(ns.network.Address(ns.network.InetSocketAddress(ns.network.Ipv4Address("10.1.7.2"), port)))
	echoClient.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds (1.0)))
	echoClient.SetAttribute("PacketSize", ns.core.UintegerValue(1024)) # 1024 Bytes
	clientApps = echoClient.Install(c.Get(4))
	clientApps.Start(ns.core.Seconds(starttime))
	clientApps.Stop(ns.core.Seconds(endtime))
	#Sink 
	echoServer = ns.applications.UdpEchoServerHelper(port)
	serverApps = echoServer.Install(c.Get(7))
	serverApps.Start(ns.core.Seconds(0.0))
	serverApps.Stop(ns.core.Seconds(endtime + 100))


	# N5 <--UDP--> N6
	echoClient = ns.applications.UdpEchoClientHelper(ns.network.Address(ns.network.InetSocketAddress(ns.network.Ipv4Address("10.1.6.2"), port)))
	echoClient.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds (1.0)))
	echoClient.SetAttribute("PacketSize", ns.core.UintegerValue(1024))
	clientApps = echoClient.Install(c.Get(5))
	clientApps.Start(ns.core.Seconds(starttime))
	clientApps.Stop(ns.core.Seconds(endtime))
	#Sink 
	echoServer = ns.applications.UdpEchoServerHelper(port)
	serverApps = echoServer.Install(c.Get(6))
	serverApps.Start(ns.core.Seconds(0.0))
	serverApps.Stop(ns.core.Seconds(endtime + 100))

	# # N4 <--UDP--> N7
	# port = 8080
	# onoff = ns.applications.OnOffHelper("ns3::UdpSocketFactory", ns.network.Address(ns.network.InetSocketAddress(ns.network.Ipv4Address("10.1.7.2"), port)))
	# onoff.SetConstantRate (ns.network.DataRate ("1024B/s"))
	# app = onoff.Install(ns.network.NodeContainer(c.Get(4)))
	# app.Start(ns.core.Seconds(1.0))
	# app.Stop(ns.core.Seconds(endtime))
	# #Sink 
	# sink = ns.applications.PacketSinkHelper("ns3::UdpSocketFactory", ns.network.InetSocketAddress(ns.network.Ipv4Address.GetAny(), port))
	# app2 = sink.Install(ns.network.NodeContainer(c.Get(7)))
	# app2.Start(ns.core.Seconds(0.0))


	# # N5 <--UDP--> N6
	# port = 8080
	# onoff = ns.applications.OnOffHelper("ns3::UdpSocketFactory", ns.network.Address(ns.network.InetSocketAddress(ns.network.Ipv4Address("10.1.6.2"), port)))
	# onoff.SetConstantRate (ns.network.DataRate ("1024B/s"))
	# app = onoff.Install(ns.network.NodeContainer(c.Get(5)))
	# app.Start(ns.core.Seconds(1.0))
	# app.Stop(ns.core.Seconds(endtime))
	# #Sink 
	# sink = ns.applications.PacketSinkHelper("ns3::UdpSocketFactory", ns.network.InetSocketAddress(ns.network.Ipv4Address.GetAny(), port))
	# app2 = sink.Install(ns.network.NodeContainer(c.Get(6)))
	# app2.Start(ns.core.Seconds(0.0))

	#############################################################################################
	
	#Tracing/Sniffing
	ascii = ns.network.AsciiTraceHelper()
	stream_trace = ascii.CreateFileStream("tcp_flow.tr")
	internetstack.EnableAsciiIpv4All(stream_trace)
	device = 0
	interface = 1
	bottle.EnablePcap(filename, devices01.Get(device), interface)

	#############################################################################################

	#Start the thing
	print '>>>> JETZT GEHTS LOS...'
	ns.core.Simulator.Run()
	ns.core.Simulator.Destroy()

	#############################################################################################

	#save pcap
	path = "dump"
	outfilename = filename + '-' + str(device) + '-' + str(interface) + '.pcap'
	if not os.path.isdir(path):
		os.mkdir( path, 0755 )
	filepath = path + "/" + outfilename
	print '>>>> ' + outfilename +' erzeugt'

	#############################################################################################

	#make csv and plot
	#shutil.copyfile("/media/sf_virtualbox_share/NS3/script/pcap_to_csv.sh", "./pcap_to_csv.sh")
	#os.chmod("./pcap_to_csv.sh", 755)
	#os.system("./pcap_to_csv.sh "+ outfilename + " " + path + "/")

	#############################################################################################

	#mv pcap into outputdir
	#os.rename(outfilename , filepath ) 
	#print '>>>> pcap gespeichert unter: ' + filepath

######################################################################################################

#make compare and plot
#shutil.copyfile("/media/sf_virtualbox_share/NS3/script/compare_csv.sh", "./compare_csv.sh")
#os.chmod("./compare_csv.sh", 755)
#os.system("./compare_csv.sh " + path + "/")