Summary
========

Various OpenContrail services (or their corresponding linux processes) need to be managed with respect to functions and events like:
a) starting/stopping/restarting
b) restarting in case of process crash/exit
c) monitoring status of the processes.
d) defining event handlers to take care of process interdependencies
 
This document discusses a process management infrastructure using Supervisor package (http://www.supervisord.org).

Why Supervisor package?
========

We decided to use Supervisor as process management infrastructure instead of upstart or systemd because:
a)    Platform-Independence: Supervisor package is written in python and works seamlessly on all flavors of linux (and non-linux systems as well).  Using Supervisor package prevents us from rewriting policy files for process/service management (in Supervisor package .ini files) when moving to a new platform.
b)   Extensibility: Supervisor package allows for external plugins that can be stand-alone programs that are fed process events. External plugins can extend the basic functionality provided by Supervisor package to do more useful functions. For e.g. OpenContrail software can have a Node Manager that can regularly log process states and core file information. More details on Node Manager software is detailed in a later section.
a.     There are other third-party plugins (whole library of them is listed on supervisord.org) which one can use based on the need. For e.g. there is a Nagios plugin to work with Nagios software.

Launch Sequence
========

In OpenContrail, a set of processes providing a related functionality is grouped together into an independent nodetype. For e.g. Analytics Node consists of contrail-collector, contrail-query-engine and contrail-analytics-api.
 
Independent supervisord instances are launched through upstart files for following Nodetypes:
1)   vrouter
2)   control
3)   analytics
4)   config
5)   webui
6)   database
 
These supervisord instances in turn launch processes corresponding to the individual OpenContrail services.
 
For e.g. supervisord instance for analytics launches contrail-collector, contrail-query-engine and contrail-analytics-api services.
Files
Upstart files for supervisord instances for different nodetypes are located in /etc/init/ directory. They are named  “supervisor-<nodetype>.conf”.
 
“supervisord” ini files for different OpenContrail services are located in /etc/contrail/supervisor_<nodetype>_files/ directory.
 
To let “service” command work, we have init.d files for both:
a)    supervisord instances of nodes:  For e.g. “service  supervisor-analytics restart” restarts all of the analytics services.
b)   Individual services: For e.g. “service contrail-collector restart” restarts contrail-collector service.  These init.d files internally simply invoke “supervisorctl” (cli tool for supervisord) to restart/start/stop the service.
 
Handling Process Exits/Crashes
========

When a service like contrail-collector that is part of analytics node crashes or exits, supervisord instance for the analytics node automatically restarts contrail-collector (supervisord .ini file for contrail-collector specifies the restart policy).
 
When supervisord instance of a nodetype itself dies down, the upstart file restarts that node. Do note that when the supervisord instance dies down all of the services in that node type also die down.
 
Node Manager
========

Node manager reports the status of processes in a given Node type to the Analytics Node. This allows Analytics Node to provide API to give status of various Nodetypes.
 
Node manager collects information regarding the state of the processes using the event handler mechanism of supervisord. Node manager also takes special actions for some events as defined in a rules files. An example rules file for Analytics Node is as follows:
 
{ "Rules": [
        {"processname": "contrail-query-engine", "process_state": "PROCESS_STATE_FATAL", "action": "service contrail-analytics-api stop"},
        {"processname": "contrail-collector", "process_state": "PROCESS_STATE_STOPPED", "action": "redis-cli -n 1 eval \"redis.call('flushdb'); redis.log(redis.LOG_NOTICE,'EV_STOP - Nodemgr Flushing Redis UVE')\" 0"},
        ..
    ]
}
 
As contrail-analytics-api requires contrail-query-engine to be running to provide API service, when contrail-query-engine dies, we would want to stop contrail-analytics-api too. The first rule above achieves the same.
 
Debugging and troubleshooting
========

Do note that traditional usage of linux “service” command still works with Supervisor package based process management infrastructure. You can use service command to even start/stop/restart all services of a nodetype collectively.
 
Examples are shown below:
 root@a6s45:~# service supervisor-analytics restart  <<<< whole of analytics node restarted
supervisor-analytics stop/waiting
supervisor-analytics start/running, process 14624
 
root@a6s45:~# service contrail-query-engine restart  <<<< contrail-query-engine restarted
contrail-query-engine: stopped
contrail-query-engine: started
 
 
One can also use “supervisorctl” command to connect to a supervisord instance for a nodetype and issue process control commands.
 
Examples are show below:
root@a6s45:~# supervisorctl -s unix:///tmp/supervisor_analytics.sock
contrail-analytics-api           RUNNING    pid 14631, uptime 0:04:24
contrail-analytics-nodemgr       RUNNING    pid 14628, uptime 0:04:24
contrail-collector               RUNNING    pid 14629, uptime 0:04:24
contrail-query-engine            RUNNING    pid 18135, uptime 0:02:38
supervisor> restart contrail-collector
contrail-collector: stopped
contrail-collector: started
supervisor> help
 
default commands (type help <topic>):
add    clear  fg        open  quit    remove  restart   start   stop  update
avail  exit   maintail  pid   reload  reread  shutdown  status  tail  version
 
supervisor> quit()
root@a6s45:~#
 
Log files
Log files of individual services are present in /var/log/contrail.  They are prefixed by the service name. For e.g.  /var/log/contrail/contrail-collector-stdout.log is log file for “contrail-collector” service.
 
Log files of supervisord instances are also present in /var/log/contrail. They are prefixed by supervisord. For e.g. /var/log/contrail/supervisord-analytics.log is log file for the supervisord instance for the analytics nodetype.
 