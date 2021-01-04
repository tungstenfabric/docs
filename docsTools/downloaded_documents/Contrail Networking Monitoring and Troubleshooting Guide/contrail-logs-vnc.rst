contrail-logs (Accessing Log File Messages)
===========================================

 

.. raw:: html

   <div id="intro">

.. raw:: html

   <div class="mini-toc-intro">

A command-line utility, ``contrail-logs``, uses REST APIs to retrieve
system log messages, object log messages, and trace messages.

.. raw:: html

   </div>

.. raw:: html

   </div>

Command-Line Options for Contrail-Logs
--------------------------------------

The command-line utility for accessing log file information is
``contrail-logs`` in the analytics node. The following are the options
supported at the command line for ``contrail-logs``, as viewed using the
``-–help`` option.

.. raw:: html

   <div id="jd0e45" class="example" dir="ltr">

::

   [root@host]#  contrail-logs --help
   usage: contrail-logs [-h] 
                        [--opserver-ip OPSERVER_IP]
                        [--opserver-port OPSERVER_PORT] 
                        [--start-time START_TIME]
                        [--end-time END_TIME] 
                        [--last LAST] 
                        [--source SOURCE]
                        [--module {ControlNode, VRouterAgent, ApiServer, Schema, OpServer, Collector, QueryEngine, ServiceMonitor, DnsAgent}]
                        [--category CATEGORY]
                        [--level LEVEL]
                        [--message-type MESSAGE_TYPE] 
                        [--reverse] 
                        [--verbose]
                        [--all]
                        [--object {ObjectVNTable, ObjectVMTable, ObjectSITable, ObjectVRouter, ObjectBgpPeer, ObjectRoutingInstance, ObjectBgpRouter, ObjectXmppConnection, ObjectCollectorInfo, ObjectGeneratorInfo, ObjectConfigNode}]
                        [--object-id OBJECT_ID]
                        [--object-select-field {ObjectLog,SystemLog}]
                        [--trace TRACE]

.. raw:: html

   </div>

Option Descriptions
-------------------

The following are the descriptions for each of the option arguments
available for ``contrail-logs``.

.. raw:: html

   <div id="jd0e56" class="example" dir="ltr">

::

   optional arguments:
     -h, --help
                           show this help message and exit
     --opserver-ip OPSERVER_IP
                           IP address of OpServer (default: 127.0.0.1)
     --opserver-port OPSERVER_PORT
                           Port of OpServer (default: 8081)
     --start-time START_TIME
                           Logs start time (format now-10m, now-1h) (default: now-10m)
     --end-time END_TIME   
                           Logs end time (default: now)
     --last LAST
                           Logs from last time period (format 10m, 1d) (default: None)
     --source SOURCE       
                           Logs from source address (default: None)
     --module {ControlNode, VRouterAgent, ApiServer, Schema, OpServer, Collector, QueryEngine, ServiceMonitor, DnsAgent}
                           Logs from module (default: None)
     --category CATEGORY   
                           Logs of category (default: None)
     --level LEVEL         
                           Logs of level (default: None)
     --message-type MESSAGE_TYPE
                           Logs of message type (default: None)
     --reverse             
                           Show logs in reverse chronological order (default: False)
     --verbose             
                           Show internal information (default: True)
     --all                 
                           Show all logs (default: False)
     --object {ObjectVNTable, ObjectVMTable, ObjectSITable, ObjectVRouter, ObjectBgpPeer, ObjectRoutingInstance, ObjectBgpRouter, ObjectXmppConnection, ObjectCollectorInfo, ObjectGeneratorInfo, ObjectConfigNode}
                           Logs of object type (default: None)
     --object-id OBJECT_ID
                           Logs of object name (default: None)
     --object-select-field {ObjectLog,SystemLog}
                           Select field to filter the log (default: None)
     --trace TRACE         
                           Dump trace buffer (default: None)

.. raw:: html

   </div>

Example Uses
------------

The following examples show how you can use the option arguments
available for ``contrail-logs`` to retrieve the information you specify.

1. View only the system log messages from all boxes for the last 10
   minutes.

   ``contrail-logs``

2. View all log messages (systemlog, objectlog, uve, ...) from all boxes
   for the last 10 minutes.

   ``contrail-logs --all``

3. View only the control node system log messagess from all boxes for
   the last 10 minutes.

   ``contrail-logs --module ControlNode``

   ``--module`` accepts the following values -
   ``ControlNode, VRouterAgent, ApiServer, Schema, ServiceMonitor, Collector, OpServer, QueryEngine, DnsAgent``

4. View the control node system log messages from source
   ``a6s23.contrail.juniper.net``\ for the last 10 minutes.

   ``contrail-logs --module ControlNode --source a6s23.contrail.juniper.net``

5. View the XMPP category system log messages from all modules on all
   boxes for the last 10 minutes.

   ``contrail-logs --category XMPP``

6. View the system log messages from all the boxes from the last hour.

   ``contrail-logs --last 1h``

7. View the system log messages from the VN object named
   ``demo:admin:vn1`` from all boxes for the last 10 minutes.

   ``contrail-logs --object ObjectVNTable --object-id demo:admin:vn1``

   ``--object``\ accepts the following values -
   ``ObjectVNTable, ObjectVMTable, ObjectSITable, ObjectVRouter, ObjectBgpPeer, ObjectRoutingInstance, ObjectBgpRouter, ObjectXmppConnection, ObjectCollectorInfo``

8. View the system log messages from all boxes for the last 10 minutes
   in reverse chronological order:

   ``contrail-logs --reverse``

9. View the system log messages from a specific time interval and
   display them in a specified date format.

   ``contrail-logs --start-time "2020 May 12 18:30:27.0" --end-time "2020 May 12 18:31:27.0"``

 
