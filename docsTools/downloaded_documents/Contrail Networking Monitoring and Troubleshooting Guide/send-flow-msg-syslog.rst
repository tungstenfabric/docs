Sending Flow Messages to the Contrail System Log
================================================

 

The ``contrail-vrouter-agent``\ can be configured to send flow messages
and other messages to the system log (syslog). To send flow messages to
syslog, configure the following parameters in
``/etc/contrail/contrail-vrouter-agent.conf``.

The following parameters are under the section ``DEFAULT``:

-  ``log_flow=1``—Enables logging of all flow messages.

-  ``use_syslog=1``—Enables sending of all messages, including flow
   messages, to syslog.

-  ``syslog_facility=LOG_LOCAL0``—Enables sending messages from the
   ``contrail-vrouter-agent`` to the syslog, using the facility
   ``LOCAL0``. You can configure ``LOCAL0`` to your required facility.

-  ``log_level=SYS_INFO``—Changes the logging level of
   ``contrail-vrouter-agent`` to INFO.

If syslog is enabled, flow messages are *not* sent to Contrail Analytics
because the two destinations are mutually exclusive.

Flow log sampling settings apply regardless of the flow log destination
specified. If sampling is enabled, the syslog messages will be sampled
using the same rules that would apply to Contrail Analytics. If
non-sampled flow data is required, sampling must be disabled by means of
configuration settings.

Flow events for termination will include both the appropriate tear-down
fields and the appropriate setup fields.

The flow messages will be sent to the syslog with a severity of INFO.

The user can configure the remote system log (``rsyslog``) on the
compute node to send syslog messages with facility LOCAL0, severity of
INFO (and lower), to the remote syslog server. Messages with a higher
severity than INFO can be logged to a local file to allow for debugging.

Flow messages appear in the syslog in a format similar to the following
log example:

``May 24 14:40:13 a7s10 contrail-vrouter-agent[29930]: 2016-05-24 Tue 14:40:13:921.098 PDT a7s10 [Thread 139724471654144, Pid 29930]: [SYS_INFO]: FlowLogDataObject: flowdata= [ [ [ flowuuid = 7ea8bf8f-b827-496e-b93e-7622a0c8eeea direction_ing = 1 sourcevn = default-domain:mock-gen-test:vn8 sourceip = 1.0.0.9 destvn = default-domain:mock-gen-test:vn58 destip = 1.0.0.59 protocol = 1 sport = -29520 dport = 20315 setup_time = 1464125225556930 bytes = 1035611592 packets = 2024830 diff_bytes = 27240 diff_packets = 40 ], ] ]``

**Note**

Several individual flow messages might be packed into a single syslog
message for improved efficiency.

 
