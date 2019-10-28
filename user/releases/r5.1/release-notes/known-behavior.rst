.. This work is licensed under the Creative Commons Attribution 4.0 International License.
   To view a copy of this license, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

==============
Known Behavior
==============

This section lists known limitations with this release.

-  `Known Behavior in Tungsten Fabric Release 5.1`_

Known Behavior in Tungsten Fabric Release 5.1
---------------------------------------------

- CEM-5402 Though the APIs allow 4 byte ASN, the backend code only support 2 byte ASN. Do not use 4 byte ASN in API integrations.

- CEM-5400 Configuring both tagged and un-tagged vlan in Contrail Fabric VPG is not supported.

- CEM-5284 Cloud Compute/vrouter nodes will not be listed in the cluster-nodes/compute node page, all nodes/computes will be listed in the servers page

- CEM-5283 For all-in-one cluster, where vrouter and openstack roles exist on the same node, "enable_haproxy" must not be enabled (set to 'yes') in the ansible yaml file. This is because of multicast traffic restrictions when vrouter is running.

    ::
     ansible-playbook  -i inventory/ -e orchestrator=openstack --tags nova playbooks/install_openstack.yml
     ansible-playbook  -i inventory/ -e orchestrator=openstack playbooks/install_contrail.yml

    ::
     global_configuration:
       ENABLE_DESTROY: True

     instances:
     
       srvr5:
         provider: bms
         ip: 19x.xxx.x.55
         roles:


- CEM-5282 When Azure cloud is extended to On-Prem cluster running on RHEL hosts, contrail-status shows vRouters running on Azure as initializing, though the services are up. This is due to the Red Hat issue https://access.redhat.com/solutions/2766251.

- CEM-5043 VNI update on a LR doesnt update the RouteTable. Workaround is to delete the LogicalRouter and create a new LogicalRouter with the new VNI.

- CEM-5042 Adding new subnet on an already provisioned VPC is not supported. If all the subnets are added during initial bringup of VPC, nodes can be added incrementally to the subnets anytime.

- CEM-5041 Provisioning of Region or VPC objects only on the cloud without any nodes is not supported. Add at least one node while provisioning Region/VPC.

- CEM-4865 Provisioning of Contrail Controllers on public cloud is not supported. Controllers need to be provisioned On-prem.

- CEM-4862 The cloud security objects associated with the underlay fabric in cloud cannot be configured with port range or CIDR.

- CEM-4381 Contrail Fabric device manager tasks can fail if one or more Contrail API servers is down. Contrail-status on the Contrail config nodes can be used to determine if this situation occur.

- CEM-4370 After creating a PNF Service Instance, the fields like PNF eBGP ASN*, RP IP Address, PNF Left BGP Peer ASN*, Left Service VLAN*, PNF Right BGP Peer ASN* ,Right Service VLAN* cannot be modified. If there is a need to modify these values, delete and re-create the Service Instance with intended values.

- CEM-4190 IPtables rules are not updated on MC-GW nodes. As a workaround, you must configure IPtables on the on-premise MC-GW nodes with INPUT and FORWARD and default ACCEPT policy.

- CEM-3959 BMS movement across TORs is not supported. To move BMS across TORs the whole VPG need to be moved. That means if there are more than one BMS associated to one VPG, and one of the BMS need to be moved, the whole VPG need to be deleted and re-configured as per the new association.

- CEM-3324 Users cannot provision Contrail Cluster entirely in Public cloud. Contrail Cluster need to be On-Prem and vRouters can be extended to public cloud.

- JCB-204796 In a Helm-based provisioned cluster, VM launch fails if MariaDB replication is set to >1.

- JCB-202874 After deleting a vRouter chart with DPDK, the NICS do not rebind to the host in Helm.

- JCB-190956 While creating ironic-provision, service address in the subnet must be pointing to openstack ironic node ip/kolla internal vip.

- JCB-187320 On a DPDK compute vif list –rate core-dumps with traffic.

- JCB-187287 High Availability provisioning of Kubernetes master is not supported.

- JCB-186493 When a snapshot of an active VM fails, shutdown the VM before generating the snapshot.

- JCB-184837 After provisioning Contrail by using a Helm-based provisioned cluster, restart nova-compute container.

- JCB-184776 When the vRouter receives the head fragment of an ICMPv6 packet, the head fragment is immediately enqueued to the assembler. The flow is created as hold flow and then trapped to the agent. If fragments corresponding to this head fragment are already in the assembler or if new fragments arrive immediately after the head fragment, the assembler releases them to flow module. Fragments get enqueued in the hold queue if agent does not write flow action by the time the assembler releases fragments to the flow module. A maximum of three fragments are enqueued in the hold queue at a time. The remaining fragments are dropped from the assembler to the flow module. As a workaround, the head fragment is enqueued to assembler only after flow action is written by agent. If the flow is already present in non-hold state, it is immediately enqueued to assembler.

- JCB-177787 In DPDK vRouter use cases such as SNAT and LBaaS that require netns, jumbo MTU cannot be set. Maximum MTU allowed: <=1500.

- JCB-177541 When you receive an error message during Kolla provisioning, rerunning the code will not work. In order for the provisioning to work, restart provisioning from scratch.

- JCB-171466 Metadata SSL works only in HA deployment mode.

- JCB-163773 A false alarm for config service is generated when config and configdb services are installed on different nodes. Ignore the false alarm.

- JCB-162927 SR-IOV with DPDK co-existence deployment is not supported using contrail-helm-deployer.
