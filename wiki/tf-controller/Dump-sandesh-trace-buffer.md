# Dump sandesh trace buffer from core file

The python module that is used to dump the sandesh trace buffers from the core file -> [sandesh_trace_dump.py](https://github.com/Juniper/contrail-sandesh/blob/master/utils/sandesh_trace_dump.py)
 
**print_trace_buffer_list()**
  - dumps the trace buffer list created by the daemon

**print_trace_buffer('#trace buffer name#')**
  - dumps the content of the specified trace buffer

**Before running gdb, please do the following steps**
- get the python pretty-printers package  
  https://gcc.gnu.org/svn/gcc/trunk/libstdc++-v3/python/

  -> svn co https://gcc.gnu.org/svn/gcc/trunk/libstdc++-v3/python/
- activate the pretty-printers by adding the following lines in  
  ~/.gdbinit

`python`

`import sys`

`sys.path.insert(0, <path of python pretty-printers package>)`

`from libstdcxx.v6.printers import register_libstdcxx_printers`

`register_libstdcxx_printers (None)`

`end`
 
Now, you are all set for trace mining 

**Example:**
 
bash-4.2$ **gdb vnswad -core core.23531**

GNU gdb (GDB) Fedora (7.4.50.20120120-42.fc17)
Copyright (C) 2012 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-redhat-linux-gnu".
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>...
Reading symbols from /home/srajanga/vnswad...done.
[New LWP 23534]
[New LWP 23535]
[New LWP 23536]
[New LWP 23537]
[New LWP 23531]
…
…

(gdb) **source #path to sandesh_trace_dump.py#**

<<<< source the python module that contains the functions to dump the sandesh trace buffer

<<<< You may add this to .gdbinit


(gdb) **python print_trace_buffer_list()**

<<<< List the trace buffers in vnswad

"Controller"

"XmppMessageTrace"

"XmppTrace"

"Flow"

"IOTraceBuf"

"Config"

"KSync"

"Multicast"

"Oper DB"

"httpbuf"

"Packet"

"Services"


(gdb) **python print_trace_buffer('httpbuf')**

<<<<< dumps the content of the "httpbuf" trace buffer

2013-04-22 18:15:51 SandeshTraceText: tracemsg = "<Initializing httpbuf" file = "src/sandesh/library/cpp/sandesh_http.cc" line = 378
2013-04-22 18:15:51 SandeshTraceText: tracemsg = "Size 100" file = "src/sandesh/library/cpp/sandesh_http.cc" line = 379
 
(gdb) **python print_trace_buffer('XmppMessageTrace')**
   
<<<< dumps the content of "XmppMessageTrace" trace buffer

2013-04-22 18:15:53 XmppRxStream: str1 = "Received xmpp message from: " IPaddress = "172.27.58.9" str3 = "Port" port = 5269 str5 = "Size: " size = 229 str7 = "Packet: " packet = "<?xml version=\"1.0\"?>\n<stream:stream from=\"\" to=\"default-global-system-config:nodea1.bng-contrail.englab.juniper.net\" id=\"++123\" version=\"1.0\" xml:lang=\"en\" xmlns=\"jabber:client\" xmlns:stream=\"http://etherx.jabber.org/streams\"  >" str9 = "$" file = "src/xmpp/xmpp_connection.cc" line = 290
2013-04-22 18:15:53 XmppTxStream: str1 = "Sent xmpp message to: " IPaddress = "172.27.58.9" str3 = "Port" port = 5269 str5 = "Size: " size = 290 str7 = "Packet: " packet = "<iq type=\"set\" from=\"default-global-system-config:nodea1.bng-contrail.englab.juniper.net\" to=\"network-control@contrailsystems.com/config\"><pubsub xmlns=\"http://jabber.org/protocol/pubsub\"><subscribe node=\"default-global-system-config:nodea1.bng-contrail.englab.juniper.net\" /></pubsub></iq>" str9 = "$" file = "src/xmpp/xmpp_connection.cc" line = 159
2013-04-22 18:15:53 XmppTxStream: str1 = "Sent xmpp message to: " IPaddress = "172.27.58.9" str3 = "Port" port = 5269 str5 = "Size: " size = 350 str7 = "Packet: " packet = "<iq type=\"set\" from=\"default-global-system-config:nodea1.bng-contrail.englab.juniper.net\" to=\"network-control@contrailsystems.com/bgp-peer\" id=\"subscribe0\"><pubsub xmlns=\"http://jabber.org/protocol/pubsub\"><subscribe node=\"default-domain:default-project:ip-fabric:__default__\"><options><instance-id>0</instance-id></options></subscribe></pubsub></iq>" str9 = "$" file = "src/xmpp/xmpp_connection.cc" line = 159