# System Log Receiver in Contrail Analytics

 

## Overview

The contrail-collector process on the Contrail Analytics node can act as
a system log receiver.

## Redirecting System Logs to Contrail Collector

You can enable the contrail-collector to receive system logs by giving a
valid `syslog_port` as a command line option:

`--DEFAULT.syslog_port <arg>`

or by adding `syslog_port` in the DEFAULT section​ of the configuration
file at `/etc/contrail/contrail-collector.conf` .

For nodes to send system logs to the contrail-collector, the system log
configuration for the node should be set up to direct the system logs to
contrail-collector.

<div id="jd0e40" class="example" dir="ltr">

### Example

Add the following line in `/etc/rsyslog.d/50-default.conf `on an Ubuntu
system to redirect the system logs to contrail-collector.

    *.* @<collector_ip>:<collector_syslog_port> :: @ for udp, @@ for tcp

</div>

The logs can be retrieved by using Contrail tool, either by using the
contrail-logs utility on the analytics node or by using the Contrail
user interface on the system log query page.

## Exporting Logs from Contrail Analytics

You can also export logs stored in Contrail analytics to another system
log receiver by using the `contrail-logs `utility.

The contrail-logs utility can take these options:
`--send-syslog, --syslog-server, --syslog-port,` to query Contrail
analytics, then send the results as system logs to a system log server.
This is an on-demand command, one can write a cron job or a job that
continuously invokes `contrail-logs` to achieve continuous sending of
logs to another system log server.

 
