* [Setup: 3 controller nodes  and 20 VMs in each of the 3 compute nodes](http://10.84.13.20:8080)
* [GracefulRestart Functional specifications](https://github.com/Juniper/contrail-controller/wiki/Graceful-Restart)
* [GracefulRestart Tentative test plan](https://github.com/Juniper/contrail-test/wiki/Graceful-Restart)

***GR helper enabled in contrail-control***

* config_wait_time: 5s
* event: service contrail-vrouter-agent restart
* New Flood pings (new flows): Works after ~9s (100% loss before that)
  This increased further to ~17s when config_wait_time was larger (15s) (as vrouter is reset only after this timer expires, causing delays in new flow setups)
* running successful flood ping: minimal impact
    1. 123654 packets transmitted, 123210 received, 0.36% packet loss, time 38600ms

***GR helper disabled in contrail-control***

* config_wait_time: Not configured
* event: service contrail-vrouter-agent restart
* New pings (new flows): Works after ~8s (100% loss before that)
* running successful flood ping: 9s Loss after which ping resumed
    1. 127266 packets transmitted, 126763 received, 0.40% packet loss, time 39803ms

Few crashes seen at different times when "service contrail-vrouter-agent restart" was executed

* [Only with production contrail-vrouter-agent binary, in IndexVector<MplsLabel>::Update, raised new bug 1615149](https://bugs.launchpad.net/juniperopenstack/+bug/1615149)
* [With debug contrail-vrouter-agent binary in Pkt0Interface::InitControlInterface, existing issue raised in 2015-12-23](https://bugs.launchpad.net/juniperopenstack/+bug/1528806)
* [Only with production contrail-control binary, fixed via new bug 1614770](https://bugs.launchpad.net/juniperopenstack/+bug/1614770)

Found couple of memory leaks in contrail-vrouter-agent process

* [~90 bytes in AgentPath::ReorderCompositeNH, raised new bug 1615147](https://bugs.launchpad.net/juniperopenstack/+bug/1615147)
* [40K+ bytes in DnsHandler::HandleDefaultDnsRequest raised new bug 1615730](https://bugs.launchpad.net/juniperopenstack/+bug/1615730)

**Outstanding fixes**

* [Send EndOfRib for routes from control-node to agents](https://review.opencontrail.org/#/c/23303/)
* [Delay Vrouter reset after contrail-vrouter-agent restart](https://github.com/rombie/contrail-controller/commit/4c9da4bbaab993cb8ecd4d897c2fcaeed481da1d)


**Label preservation after agent restart (Email from Nischal)**
```
Hi Praveen/Prabhjot,

We will need to preserve the label(s) advertised for each route. Otherwise, vRouter
can black hole traffic or even worse, mis-direct it to an incorrect VMI. We realized this
when trying to brainstorm about the root cause of the 17 sec packet loss that Ananth
reported.

Per discussion with Harshad and Ashish, this means that agent needs to preserve all
interface, nh, vrf and other indices as well as labels. We can postpone/delay the effort
of doing a proper audit, but we still need to ensure that we have non-stop forwarding.
IOW, we should drop traffic only when we decide to blow away old FIB state in the
vRouter and program new state, not prior to that event.

We can have a meeting to discuss this further early next week.

-Nischal
```

**Questions**

* [GR Enable/Disable for ISSU ?](http://www.opencontrail.org/opencontrail-in-service-software-upgrade/)*
* EndOfRib
    1. EndOfRib Marker for configs from control-node to agent
    2. EndOfRib Marker for routes from control-node to agent
    3. EndOfRib Marker for routes from agent to control-node
    4. EndOfRib marker be sent per table (per instance) (Currently it is global and hence keeps implementation simpler)
* Preserve labels, vrf-id across agent restart (Refer to email snippet above)
* Preserve ifindex across agent restart
* GR Helper mode is currently configurable in /etc/contrail/contrail-control.conf (Should we add this to schema? We already have GR time values configurable via schema)

**Helper code to create VNs and VMs**

```
#!/usr/bin/env ruby

@vn_prefix = "network_"
@vm_prefix = "vm_"
@vns = 10
@vms_per_vn = 6

def setup_misc
    puts `nova flavor-create --is-public True m1.utiny 6 512 10 1`
    puts `nova keypair-add contrail > contrail.pem`   
end

def setup_networks
    1.upto(@vns) { |i|
        net = "#{@vn_prefix}#{i}"
        puts `neutron net-create #{net}`
        puts `neutron subnet-create #{net} 192.168.#{i}.0/24`
    }
end

def setup_vm_image
    puts `sshpass -p c0ntrail123 scp /cs-shared/ananth/images/xenial-server-cloudimg-amd64-disk1.img root@10.84.13.20:.`
    puts `glance image-create --container-format bare --disk-format qcow2 --file xenial-server-cloudimg-amd64-disk1.img --progress --name ubuntu-xenial`
end

def setup_docker_image
    `bash -c "cd /opt/contrail/utils; fab add_images:phusion-baseimage-enablesshd"`
end

def setup_instances (image = "phusion-baseimage-enablesshd")
    1.upto(@vns) { |i|
        net = "#{@vn_prefix}#{i}"
        cmd = "neutron net-show #{net} --fields id -f shell"
        o = `#{cmd}`
        next if o.chomp !~ /\"([a-z0-9\-]+)\"/
        net_id = $1
        1.upto(@vms_per_vn) { |j|
            puts `nova boot --image #{image} --flavor m1.utiny --key_name contrail --poll --nic net-id=#{net_id} --availability-zone nova:a6s20 u-a6s20-vn#{i}-vm#{j}`
            puts `nova boot --image #{image} --flavor m1.utiny --key_name contrail --poll --nic net-id=#{net_id} --availability-zone nova:a6s1 u-a6s1-vn#{i}-vm#{j}`
        }
    }
end

def setup
    setup_misc
    setup_networks
    setup_docker_image
end

# setup
setup_instances("phusion-baseimage-enablesshd")
```

