# Vrouter Module Parameters
Vrouter takes the following parameters:

* vr_flow_entries (uint)    : maximum flow entries (default is 512K)
* vr_oflow_entries (uint)   : maximum overflow entries (default is 8K)
* vr_bridge_entries (uint)  : maximum bridge entries (default is 256K)
* vr_bridge_oentries (uint) : maximum bridge overflow entries
* vr_mpls_labels (uint)     : maximum MPLS labels used in the node (default is 5K)
* vr_nexthops (uint)        : maximum nexthops in the node
* vr_vrfs (uint)            : maximum VRFs supported in the node
* vr_interfaces (uint)      : maximum interfaces that can be created (default is 4352); this can be modified
                              from release 3.1.1.0 & 3.2
* vrouter_dbg (int)         : 1 to dump packets, 0 to disable (disabled by default)

The currently configured limits can be seen using `vrouter --info`. These can be updated by editing /etc/modprobe.d/vrouter.conf with the desired options and by following it up with a reboot of the node.

`options vrouter vr_mpls_labels=196000 vr_nexthops=521000 vr_vrfs=65536 vr_bridge_entries=1000000`

The following could be used to derive the values:
* vrfs = Max number of VNs
* mpls_labels = (max number of VM interfaces * 2) + (4 * max number of VRFs) <br> = (L2, L3 labels for each interface) + (per VRF labels for (control node 1 + control node 2 + EVPN + VRF NH)) <br> For TSN, the number of VM interfaces need not be taken into consideration.
* nexthops = (max number of VNs * 4) + (max number of interfaces on the node * 5) + number of TORs + number of compute nodes + 100
* bridge entries / macs = Maximum number of MACs in a VN
* Flow table is hashed based on flow tuple. When flow bucket is full, new entries are added to overflow table. It is recommended not to increase the overflow table size as it could impact performance.

Some of these parameters can be provisioned during setup via fab, using the following testbed configuration.

    env.vrouter_module_params = {
        host4:{'mpls_labels':'196000', 'nexthops':'521000', 'vrfs':'65536', 'macs':'1000000'},
        host5:{'mpls_labels':'196000', 'nexthops':'521000', 'vrfs':'65536', 'macs':'1000000'}
    }


# VRouter memory requirements
VRouter will allocate few blocks of memory during its initialisation. The memory is normally available during bootup of compute node. If the vrouter module is reloaded on a running compute node, there are chances that vrouter may not get all required memory blocks and insertion of vrouter module can fail. Running command below will free-up os-cache and lets vrouter allocate memory blocks it needs. 

    root@nodel2:~$ free && sync && echo 3 > /proc/sys/vm/drop_caches && free
                 total       used       free     shared    buffers     cached
    Mem:     263785456   16921100  246864356       1312      73132     139468
    -/+ buffers/cache:   16708500  247076956
    Swap:    268324860          0  268324860
                 total       used       free     shared    buffers     cached
    Mem:     263785456   16749356  247036100       1312       1144      39532
    -/+ buffers/cache:   16708680  247076776
    Swap:    268324860          0  268324860

# Steps to reload vrouter with new parameters
1. Create/edit file /etc/modprobe.d/vrouter.conf with new parameters
1. Stop vrouter processes with "service supervisor-vrouter stop"
1. Ensure no vrouter utility programs such as "flow, nh, vif..." are running
1. Unload vrouter module with "rmmod vrouter"
1. Run “free && sync && echo 3 > /proc/sys/vm/drop_caches && free” on host-os
1. Insert module again with "modprobe vrouter"
1. Restart vrouter processes with "service supervisor-vrouter start"
1. Verify new parameters with "vrouter —info"