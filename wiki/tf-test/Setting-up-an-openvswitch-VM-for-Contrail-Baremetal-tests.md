This document describes the bring-up of a openvswitch VM on a virt-manager. 
This VM can then be used to run ovsdb-server,vtep and simulate netns namespaces as BMS endpoints. Contrail Baremetal-integration tests could then be performed

# Installation of basic packages
On a Centos 6.5, I usually install the following 

    yum groupinstall "Desktop" "Desktop Platform" "X Window System" "Fonts"
    yum install libvirt virt-manager kvm qemu-utils screen tigervnc-server tcpdump

In virt-manager UI, goto Edit> Connection Details > Network Interfaces and create a bridge interface(say br0) and choose an existing interface (say eth0) to make it part of the bridge. br0 would then get the IP of eth0. The ovs VM could then pick this network to send/receive traffic
 
On Ubuntu, virt-manager UI does not seem to provide good support to work with bridge interfaces

# Setup openvswitch on VM 

Boot the VM from http://10.204.217.158/images/base-ovs-vm-qcow2.img 

    virt-install --virt-type kvm --name tor-vm1 --ram 1024 --disk path=<path-of-base-ovs-vm-qcow2.img>,format=qcow2  --network bridge=br0,mac=52:54:00:01:01:01  --noautoconsole --os-type=linux  --boot hd --graphics vnc,listen=0.0.0.0
Make sure that the MAC Address, bridge name is specified correctly and check that the VM gets a DHCP IP or assign an IP statically
Once the VM boots up, login as root:c0ntrail123, and run 

    rm -f /etc/openvswitch/*.db
    cd ~/openvswitch-2.3.1/
    ovsdb-tool create /etc/openvswitch/ovs.db vswitchd/vswitch.ovsschema ; ovsdb-tool create /etc/openvswitch/vtep.db vtep/vtep.ovsschema
    service openvswitch-switch stop
    ovsdb-server --pidfile --detach --log-file --remote punix:/var/run/openvswitch/db.sock --remote=db:hardware_vtep,Global,managers --remote ptcp:6632 /etc/openvswitch/ovs.db /etc/openvswitch/vtep.db
    ovs-vswitchd --log-file --detach --pidfile unix:/var/run/openvswitch/db.sock
    
Set the ptcp port as desired. contrail-tor-agent has to be configured appropriately
# Create the TOR

    cd ~/openvswitch-2.3.1
    ovs-vsctl add-br TOR1
    vtep-ctl add-ps TOR1
    vtep-ctl set Physical_Switch TOR1 tunnel_ips=<IP of the TOR> 
    python vtep/ovs-vtep --log-file=/var/log/openvswitch/ovs-vtep.log --pidfile=/var/run/openvswitch/ovs-vtep.pid --detach TOR1

Note that the TOR IP above should be reachable from the Contrail ToR Agent and TSN

# Simulating a BMS endpoint on the ToR

The connection would look something like this 

    Physical-network-----(TOR1)torport1-----nstap1(ns1)

On the Openvswitch VM, netns namespaces will be used as BMS endpoints 


    ip netns add ns1
    ip link add nstap1 type veth peer name tortap1
    ovs-vsctl add-port TOR1 tortap1
    ip link set nstap1 netns ns1
    ip netns exec ns1 ip link set dev nstap1 up
    ip link set dev tortap1 up
    ip netns exec ns1 ip link set nstap1 address 00:01:00:00:05:78
    ip netns exec ns1 dhclient nstap1
    
Suitably set the MAC address above 

# Deleting a BMS on the ToR
Incase things get messed up, you could delete the BMS endpoint and add it back 

    ip netns delete ns1
    ovs-vsctl del-port TOR1 torport1
    ip link delete torport1

### References 

1. [[ovs-vtep Readme | https://github.com/openvswitch/ovs/blob/master/vtep/README.ovs-vtep.md]]