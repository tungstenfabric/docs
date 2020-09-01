In Release 3.0, ability to configure the set of fields one can use to hash during ECMP load balancing has been introduced.
This set of fields until 3.0 was always fixed to the standard 5 tuple (Source L3 address, Destination L3 address, L4 protocol, L4 SourcePort and L4 DestinationPort) fields. With this new feature, users can configure the exact sub-set of fields to hash upon when choosing the forwarding path among a set of eligible ECMP candidates.

The schema change for this feature can be found in [Hash Fields Schema](https://github.com/Juniper/contrail-controller/blob/master/src/schema/xmpp_unicast.xsd#L69)

Configuration can be applied on a global level, on a per virtual-network(VN) level and on a per virtual-network-interface(VMI) level. VMI's config takes precedence over VN config which takes precedence over global level configuration if present.

Typically this feature is useful whenever packets originated from a particular source and addressed a particular destination MUST go through a same set of service instances during the transit. This could be required if source/destination/transit nodes keep some state based on the flow and could be used for subsequent new flows as well, between the same pair of source and destination addresses. In such cases, subsequent flows must follow the same set of service nodes that the initial flow followed.

Instead of providing a feature to select pre-configured subsets of the 5 tuples to use during ECMP forwarding, a general feature to select necessary fields directly by the users themselves has been provided in 3.0 release.

e.g. ECMP fields can be selected from contrail web UI in virtual-network configuration section as shown in this picture 
![ECMP Fields Selection under VN](https://raw.githubusercontent.com/wiki/rombie/contrail-controller/virtual_network_ecmp_fields_selection.png)

If configured for the VirtualNetwork, all traffic destined to that VM will get the customized hash field selection during forwarding over ECMP paths (by VRouters).

Instead, in a more practical scenario in which, flows between a pair of source and destination must go through the same service-instance in between, one could configure customized ECMP fields for the ServiceInstances' VirtualMachineInterface (VMI). Then, all service-chain routes originated off that VMI would get the desired ECMP field selection applied as its path attribute, and eventually gets propagated to the ingress VRouter node.

![ECMP Fields Selection under VMI](https://raw.githubusercontent.com/wiki/rombie/contrail-controller/virtual_network_interface_ecmp_fields_selection.png)


### Applicability
This feature is mainly applicable in scenarios where in multiple ECMP paths exist for a destination. Typically these paths point ingress service instance nodes, which could be running any where in the contrail cloud. Following steps can be followed to create a setup with ECMP over service chains

1. Create necessary virtual networks to interconnect using service-chaining (with ECMP load-balancing).
2. Create a service template ST and enable scaling.
3. Create service instance SI using ST, select desired number if instances for scale-out, select desired left and right virtual network to connect and also select "shared address" space to make sure that instantiated services come up with the same IP address for left and right respectively. This enables ECMP among all those service instances during forwarding
4. Create a policy, select service instance SI and apply it to the desired VMIs or VNs.
5. After service VMs are instantiated, left and right interfaces' ports shall be available for further configuration. Select the left port (VMI) of the service instances and apply appropriate ECMP field selection configuration.

Note: At the moment, from the contrail UI, one cannot apply ECMP field selection configuration directly over the service's left or right interface. Instead, one has go to the ports(VMIs) section under networking and configure ECMP fields selection for each of the instantiated service instances' VMIs explicitly. This must be done for interface of all service instances in the group to ensure correctness.

Once all setup done correctly, vrouters shall be programmed with appropriate routing table with ECMP paths towards various service instances. Also vrouters are programmed with the desired ECMP fields to be used to hash during load balancing the traffic.

### Traffic flow path 'without' customized ecmp fields selection configuration (i.e, use all standard 5 tuple flow fields)
Here are various flows without ecmp-field selections configured in a sample setup with multiple in-network-nat service instances

```
tcpdump -i eth0 'port 1023 and tcp[tcpflags] & (tcp-syn) != 0 and tcp[tcpflags] & (tcp-ack) == 0'
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
14:55:10.115122 IP 2.2.2.5.18337 > 2.2.2.100.1023: Flags [S], seq 2276852196, win 29200, options [mss 1398,sackOK,TS val 25208882 ecr 0,nop,wscale 7], length 0
14:55:10.132753 IP 2.2.2.4.21193 > 2.2.2.100.1023: Flags [S], seq 4161487314, win 29200, options [mss 1398,sackOK,TS val 25208886 ecr 0,nop,wscale 7], length 0
14:55:10.152053 IP 2.2.2.5.24230 > 2.2.2.100.1023: Flags [S], seq 2466454857, win 29200, options [mss 1398,sackOK,TS val 25208892 ecr 0,nop,wscale 7], length 0
14:55:11.146029 IP 2.2.2.5.24230 > 2.2.2.100.1023: Flags [S], seq 2466454857, win 29200, options [mss 1398,sackOK,TS val 25209142 ecr 0,nop,wscale 7], length 0
14:55:13.147616 IP 2.2.2.5.24230 > 2.2.2.100.1023: Flags [S], seq 2466454857, win 29200, options [mss 1398,sackOK,TS val 25209643 ecr 0,nop,wscale 7], length 0
14:55:13.164367 IP 2.2.2.3.25582 > 2.2.2.100.1023: Flags [S], seq 2259034580, win 29200, options [mss 1398,sackOK,TS val 25209644 ecr 0,nop,wscale 7], length 0
14:55:13.179939 IP 2.2.2.5.24895 > 2.2.2.100.1023: Flags [S], seq 2174031724, win 29200, options [mss 1398,sackOK,TS val 25209648 ecr 0,nop,wscale 7], length 0
14:55:14.168282 IP 2.2.2.5.24895 > 2.2.2.100.1023: Flags [S], seq 2174031724, win 29200, options [mss 1398,sackOK,TS val 25209898 ecr 0,nop,wscale 7], length 0
14:55:16.172384 IP 2.2.2.5.24895 > 2.2.2.100.1023: Flags [S], seq 2174031724, win 29200, options [mss 1398,sackOK,TS val 25210399 ecr 0,nop,wscale 7], length 0
14:55:16.189864 IP 2.2.2.5.22952 > 2.2.2.100.1023: Flags [S], seq 3099816842, win 29200, options [mss 1398,sackOK,TS val 25210401 ecr 0,nop,wscale 7], length 0
14:55:16.205142 IP 2.2.2.4.16487 > 2.2.2.100.1023: Flags [S], seq 3961114202, win 29200, options [mss 1398,sackOK,TS val 25210405 ecr 0,nop,wscale 7], length 0
14:55:17.196763 IP 2.2.2.4.16487 > 2.2.2.100.1023: Flags [S], seq 3961114202, win 29200, options [mss 1398,sackOK,TS val 25210655 ecr 0,nop,wscale 7], length 0
14:55:19.200623 IP 2.2.2.4.16487 > 2.2.2.100.1023: Flags [S], seq 3961114202, win 29200, options [mss 1398,sackOK,TS val 25211156 ecr 0,nop,wscale 7], length 0
14:55:19.215809 IP 2.2.2.3.18914 > 2.2.2.100.1023: Flags [S], seq 3157557440, win 29200, options [mss 1398,sackOK,TS val 25211158 ecr 0,nop,wscale 7], length 0
14:55:19.228405 IP 2.2.2.7.15569 > 2.2.2.100.1023: Flags [S], seq 3850648420, win 29200, options [mss 1398,sackOK,TS val 25211161 ecr 0,nop,wscale 7], length 0
14:55:20.223482 IP 2.2.2.7.15569 > 2.2.2.100.1023: Flags [S], seq 3850648420, win 29200, options [mss 1398,sackOK,TS val 25211412 ecr 0,nop,wscale 7], length 0
14:55:22.232068 IP 2.2.2.7.15569 > 2.2.2.100.1023: Flags [S], seq 3850648420, win 29200, options [mss 1398,sackOK,TS val 25211913 ecr 0,nop,wscale 7], length 0
14:55:22.247325 IP 2.2.2.4.28388 > 2.2.2.100.1023: Flags [S], seq 3609240658, win 29200, options [mss 1398,sackOK,TS val 25211915 ecr 0,nop,wscale 7], length 0
```

### Traffic flow path 'with' customized ecmp fields selection configuration for source-ip and destination-ip only
```
root@two:~# tcpdump -i eth0 'port 1023 and tcp[tcpflags] & (tcp-syn) != 0 and tcp[tcpflags] & (tcp-ack) == 0'
tcpdump: verbose output suppressed, use -v or -vv for full protocol decode
listening on eth0, link-type EN10MB (Ethernet), capture size 65535 bytes
15:57:18.680853 IP 2.2.2.4.21718 > 2.2.2.100.1023: Flags [S], seq 2052086108, win 29200, options [mss 1398,sackOK,TS val 26141024 ecr 0,nop,wscale 7], length 0
15:57:18.696114 IP 2.2.2.4.13585 > 2.2.2.100.1023: Flags [S], seq 2039627277, win 29200, options [mss 1398,sackOK,TS val 26141028 ecr 0,nop,wscale 7], length 0
15:57:18.714846 IP 2.2.2.4.16414 > 2.2.2.100.1023: Flags [S], seq 3252526560, win 29200, options [mss 1398,sackOK,TS val 26141033 ecr 0,nop,wscale 7], length 0
15:57:18.731281 IP 2.2.2.4.32499 > 2.2.2.100.1023: Flags [S], seq 1389133175, win 29200, options [mss 1398,sackOK,TS val 26141037 ecr 0,nop,wscale 7], length 0
15:57:18.747051 IP 2.2.2.4.6081 > 2.2.2.100.1023: Flags [S], seq 427936299, win 29200, options [mss 1398,sackOK,TS val 26141041 ecr 0,nop,wscale 7], length 0
15:57:19.740204 IP 2.2.2.4.6081 > 2.2.2.100.1023: Flags [S], seq 427936299, win 29200, options [mss 1398,sackOK,TS val 26141291 ecr 0,nop,wscale 7], length 0
15:57:21.743951 IP 2.2.2.4.6081 > 2.2.2.100.1023: Flags [S], seq 427936299, win 29200, options [mss 1398,sackOK,TS val 26141792 ecr 0,nop,wscale 7], length 0
15:57:21.758532 IP 2.2.2.4.13800 > 2.2.2.100.1023: Flags [S], seq 3020971712, win 29200, options [mss 1398,sackOK,TS val 26141794 ecr 0,nop,wscale 7], length 0
15:57:21.772646 IP 2.2.2.4.23894 > 2.2.2.100.1023: Flags [S], seq 3373734307, win 29200, options [mss 1398,sackOK,TS val 26141797 ecr 0,nop,wscale 7], length 0
15:57:22.764469 IP 2.2.2.4.23894 > 2.2.2.100.1023: Flags [S], seq 3373734307, win 29200, options [mss 1398,sackOK,TS val 26142047 ecr 0,nop,wscale 7], length 0
15:57:24.768511 IP 2.2.2.4.23894 > 2.2.2.100.1023: Flags [S], seq 3373734307, win 29200, options [mss 1398,sackOK,TS val 26142548 ecr 0,nop,wscale 7], length 0
15:57:24.784119 IP 2.2.2.4.21858 > 2.2.2.100.1023: Flags [S], seq 2212369297, win 29200, options [mss 1398,sackOK,TS val 26142550 ecr 0,nop,wscale 7], length 0
15:57:24.797149 IP 2.2.2.4.29440 > 2.2.2.100.1023: Flags [S], seq 2007897735, win 29200, options [mss 1398,sackOK,TS val 26142554 ecr 0,nop,wscale 7], length 0
15:57:25.792816 IP 2.2.2.4.29440 > 2.2.2.100.1023: Flags [S], seq 2007897735, win 29200, options [mss 1398,sackOK,TS val 26142804 ecr 0,nop,wscale 7], length 0
15:57:27.797538 IP 2.2.2.4.29440 > 2.2.2.100.1023: Flags [S], seq 2007897735, win 29200, options [mss 1398,sackOK,TS val 26143305 ecr 0,nop,wscale 7], length 0
15:57:27.814002 IP 2.2.2.4.23452 > 2.2.2.100.1023: Flags [S], seq 1659332655, win 29200, options [mss 1398,sackOK,TS val 26143307 ecr 0,nop,wscale 7], length 0
```

## Hash consistency

An ECMP nexthop maintains list of all its member nexthops. For a given flow, Agent selects one of the members based on hash computed for the flow. The hash computation uses key fields according to algorithm explained above. The hash is used to index the array of members in ECMP Nexthop. The ECMP management logic ensures that position of a member nexthop does not change on add/delete of members to the list. As a result, flows continue to use a member nexthop even if new members are added or deleted into the ECMP nexthop.


The hash value is computed using boost::hash_combine() function. boost::hash_combine is a deterministic hash, as a result,  hash of given keys will always result in same value. So, hash value for a given flow is always same.
The algorithm ensures that packets of given 5-tuple use same ECMP member even if flow is deleted and added again.


Note, if Agent restarts there is no guarantee that members are built in same sequence inside the ECMP nexthop. So, flows can go to different ECMP members on Agent restart.