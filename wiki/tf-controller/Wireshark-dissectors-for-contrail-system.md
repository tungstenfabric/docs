Wireshark Dissectors:
    Each wireshark dissector decodes its part of the protocol and then hands off decoding to subsequent dissectors for an encapsulated protocol. Wireshark dissectors can be developed in two ways. One is to modify wireshark source-code for new dissector, compile it and build the required binary. Another way is to make use of embedded Lua interpreter of wireshark. Lua scripts can be written for dissectors and can be used as command-Line option for tshark. 

Complete development information can be found in following link: [Wireshark development wiki](https://wiki.wireshark.org/Development)

Usage:
As a security measure, tshark protects the system from running the script(greater possibilities to mess-up the system if not written properly) with root previleges. Hence script can be used only by non-root users. By default, dumpcap utility will not allow non-root users to perform packet capturing. Hence to use wireshark packet dissectors written as lua scripts, following ways can be used:

1) Modify wireshark dumpcap settings to allow non-root users to capture packets. This setting can be modified any time by running: 

dpkg-reconfigure wireshark-common

2) Capture packets with root privileges and write them to a file. Give read permissions to file for non-root users. Use the lua script with tshark as non-root user

New user to be added to wireshark group and can be added on debian systems as below:
useradd guest -g wireshark 

Please make sure to use required tshark filters for interested packets to avoid huge outputs. 

Some important flags to be used with tshark:

-X lua_script:<example.lua> (using lua script with command-line option)

-V (displays the protocol tree fields)

-i <interface> (interface to capture the packets)

-r <file.pcap> (read from captured file)

-w <file.pcap> (write captures to a file)

Currently two Lua dissectors are written for contrail system. These are stored in following location in contrail-system: 
/usr/share/contrail-utils
• agent_dissector.lua 
       * To decode the agent header(used for communication between agent and vrouter)
• mpls_dissector.lua
       * To decode mpls header for mpls label(for both MPLSoUDP and MPLSoGRE packets)

For mirrored-packets, a plugin is already added to wireshark which parses the metadata and displays the packet fields. For more details, refer to [Analyzer vm](http://www.juniper.net/techpubs/en_US/contrail2.2/topics/concept/analyzer-vm.html)

Example output for ping packet received to agent from local vm:

$ tshark -i pkt0 -V -X lua_script:/usr/share/contrail-utils/agent_dissector.lua  
Frame 8: 142 bytes on wire (1136 bits), 142 bytes captured (1136 bits) on interface 0  
    Interface id: 0  
    Encapsulation type: Ethernet (1)  
    Arrival Time: Aug  9, 2016 09:15:24.985112000 IST  
    [Time shift for this packet: 0.000000000 seconds]  
    Epoch Time: 1470714324.985112000 seconds  
    [Time delta from previous captured frame: 0.718611000 seconds]  
    [Time delta from previous displayed frame: 0.718611000 seconds]  
    [Time since reference or first frame: 0.919188000 seconds]  
    Frame Number: 8  
    Frame Length: 142 bytes (1136 bits)  
    Capture Length: 142 bytes (1136 bits)  
    [Frame is marked: False]  
    [Frame is ignored: False]  
    [Protocols in frame: agent:ip:icmp:data]  
agent Protocol  
    Interface index: 3  
    Vrf: 1  
    command: 4  
    command parameter: 0  
    command parameter 1: 0  
    command parameter 2: 0  
    command parameter 3: 0  
    command parameter 4: 0  
    command parameter 5: 0  
Internet Protocol Version 4, Src: 17.1.1.4 (17.1.1.4), Dst: 17.1.1.2 (17.1.1.2)  
    Version: 4  
    Header length: 20 bytes  
    Differentiated Services Field: 0x00 (DSCP 0x00: Default; ECN: 0x00: Not-ECT (Not ECN-Capable Transport))  
        0000 00.. = Differentiated Services Codepoint: Default (0x00)  
        .... ..00 = Explicit Congestion Notification: Not-ECT (Not ECN-Capable Transport) (0x00)  
    Total Length: 84  
    Identification: 0x0000 (0)  
    Flags: 0x02 (Don't Fragment)  
        0... .... = Reserved bit: Not set  
        .1.. .... = Don't fragment: Set  
        ..0. .... = More fragments: Not set  
    Fragment offset: 0  
    Time to live: 63  
    Protocol: ICMP (1)  
    Header checksum: 0x17a2 [validation disabled]  
        [Good: False]  
        [Bad: False]  
    Source: 17.1.1.4 (17.1.1.4)  
    Destination: 17.1.1.2 (17.1.1.2)  
    [Source GeoIP: Unknown]  
    [Destination GeoIP: Unknown]  
Internet Control Message Protocol  
    Type: 8 (Echo (ping) request)  
    Code: 0  
    Checksum: 0x33d1 [correct]  
    Identifier (BE): 21006 (0x520e)  
    Identifier (LE): 3666 (0x0e52)  
    Sequence number (BE): 5 (0x0005)  
    Sequence number (LE): 1280 (0x0500)  
    Timestamp from icmp data: Aug  9, 2016 09:15:24.000000000 IST  
    [Timestamp from icmp data (relative): 0.985112000 seconds]  
    Data (48 bytes)  
  
0000  27 9f 0e 00 00 00 00 00 10 11 12 13 14 15 16 17   '...............  
0010  18 19 1a 1b 1c 1d 1e 1f 20 21 22 23 24 25 26 27   ........ !"#$%&'  
0020  28 29 2a 2b 2c 2d 2e 2f 30 31 32 33 34 35 36 37   ()*+,-./01234567  
        Data: 279f0e0000000000101112131415161718191a1b1c1d1e1f...  
        [Length: 48]  
