## Step 0 - Pre-requisites

* Ensure on all servers disk on ****all partitions**** are not exhausted.

    ``df -kh``

* Ensure time is synchronized on all servers with ntp.

* Collect output of ``contrail-status`` on all nodes  
contrail-status first checks if a process is running, and if it is, it does introspect into the process to get it's functionality status, and outputs the 'aggregate' status. The states displayed are

  * active - if the process is running and functional [internal state is good]
  * inactive - stopped by user
  * failed - process exited too quickly and not restarted
  * initializing - if the process is running, but internal state is not yet functional.  
When a process shows _initializing_, then it is not in fully functional mode. Most likely
reason would be it's not able to connect to one of its servers. Further information can be obtained using introspect into the process as explained at  
https://github.com/Juniper/contrail-controller/wiki/Monitoring-of-contrail-node-status-and-contrail-process'-status

* `initializing (NTP state unsynchronized.)`  
contrail controller requires all the servers to be in NTP synchronized state. The nodemgr starts monitoring the ntp state few minutes after it is up and reports if the NTP is not synchronized. It determines this by using 'ntpq -p' output. You should verify that
 * ntpd is installed and running
 * ntp server is configured in /etc/ntp.conf
 * 'ntqp -q' shows ntp is in sync

NTP can be configured using fabric by adding a NTP server hostname to the fabric `testbed.py` file and then provisioning using fabric. For example, to use _ntp.juniper.net_ as NTP server, the following can be added to the `testbed.py` file

`env.ntp_server = 'ntp.juniper.net'`


## If floating-ip is not reachable

* Ensure the project has a ingress security group rule to allow from 0.0.0.0/0

* While instantiating a VM, say you are using a CirrOS image directly downloaded from web and creating it through the horizon UI i.e. you didn't use glance to create it. Leave the architecture field "**blank**". Cause if you put amd64 / x86-64 for the respective 64-bit image, you can end up in the following issue:
https://ask.openstack.org/en/question/47756/instance-not-supported/