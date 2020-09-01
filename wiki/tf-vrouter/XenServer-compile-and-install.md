## Instructions for XenServer 6.1

In a XenServer DDK VM checkout the OpenContrail source code.
KERNEL_SOURCE is a directory where the linux kernel (with XenServer patches) is present.

1. Compile OpenContrail vrouter kernel module and agent:
```
    scons --target=i686 --kernel-dir=${KERNEL_SOURCE} src/vnsw/agent:vnswad
    scons --target=i686 --kernel-dir=${KERNEL_SOURCE} src/vnsw/dp
    scons src/sandesh/common
    scons src/sandesh/library/python
```
2. Build the OpenContrail thrift service
```
scons build/bin/thrift
build/bin/thrift -o build/debug/vnsw/agent/openstack -gen py src/vnsw/agent/openstack/instance_service.thrift
```

## On the target machine:
1. Install vnswad and the binaries in build/debug/vnsw/dp/utils in /opt/contrail/bin
2. Copy the kernel module to /lib/modules/<version>/extra/net/vrouter/vrouter.ko
3. Install python thrift client library: https://pypi.python.org/packages/source/t/thrift/thrift-0.8.0.tar.gz
4. Install python uuid library: https://pypi.python.org/packages/source/u/uuid/uuid-1.30.tar.gz
5. Install the python instance service library (build/debug/vnsw/agent/openstack/gen-py)
6. Install the sandesh python library (build/debug/tools/sandesh/library/python/dist/sandesh-0.1dev.tar.gz)
7. Create the agent configuration file (/etc/contrail/agent.conf)
```
<?xml version="1.0" encoding="utf-8"?>
<config>
    <agent>
        <!-- Physical ports connecting to IP Fabric -->
        <vhost>
            <name>xenbr1</name>
            <ip-address>10.x.x.x/24</ip-address>
            <gateway>10.x.x.x</gateway>
        </vhost>
        <eth-port>
            <name>eth1</name>
        </eth-port>
        <xmpp-server>
	    <ip-address>10.x.x.x</ip-address>
	</xmpp-server>
    </agent>
</config>
```
8. Install Xen utils from https://github.com/Juniper/vrouter-xen-utils
9. Create /etc/init.d/contrail-vrouter
```
# chkconfig: 2345 9 9
# description: OpenContrail Network Virtualization service offering
ulimit -c unlimited
. /etc/init.d/functions

LOG=/var/log/contrail-agent.log
PID_FILE=/var/run/contrail-agent.pid
CONF_FILE=/etc/contrail/agent.conf

insert_kmod() {
    KMOD=/lib/modules/$(uname -r)/extra/net/vrouter/vrouter.ko
    if [ ! -e $KMOD ]; then
	echo "Kernel module $KMOD: no such file"
	exit 1	
    fi

    insmod $KMOD
    if [ $? != 0 ]; then
	echo "Kernel module initialization failed"
	exit 1
    fi
}
admin_interface() {
    eth=$( cat $CONF_FILE | sed -n -e "s/.*<name>\(eth[0-9.]\+\).*/\1/gp" )
    echo $eth
}

br_interface() {
    br=$( cat $CONF_FILE | sed -n -e "s/.*<name>\(xenbr[0-9.]\+\).*/\1/gp" )
    echo $br
}

interface_setup() {
    ADMIN_IF=$( admin_interface )
    UNIT=$( echo "$ADMIN_IF" | sed -n -e "s/\(.*\)\([0-9.]\)\+/\2/gp" )
    BR_IF=$( br_interface )

    PHYSADDR=$(cat /sys/class/net/$ADMIN_IF/address)

    vif --create $BR_IF --mac $PHYSADDR
    if [ $? != 0 ]; then
	echo "Unable to create interface $BR_IF"
	exit 1
    fi

    vif --add $BR_IF --mac $PHYSADDR --vrf 0 --mode x --type vhost
    if [ $? != 0 ]; then
	echo "Unable to add interface $BR_IF to vrouter"
	exit 1
    fi

    if [ -e /etc/sysconfig/network-scripts/ifcfg-$BR_IF ]; then
	ifup $BR_IF
    fi

    brname=$(xe network-list name-label="cloud_link_local_network" | awk '/bridge/{print $4;}')
    if [ -n "$brname" ]; then
        vif --create ${brname}
    fi
}

start() {
    kmod_present=$(lsmod | grep vrouter)
    if [ -z "${kmod_present}" ]; then
	insert_kmod
	interface_setup
    fi
    
    /usr/bin/vnswad --config-file $CONF_FILE 1>$LOG 2>&1 &
    echo $! >$PID_FILE
}

stop() {
    kill `cat $PID_FILE`
#    rmmod vrouter
}

case $1 in
    start)
	start
	;;

    stop)
	stop
	;;
    restart)
	stop
	start
	;;
esac

```