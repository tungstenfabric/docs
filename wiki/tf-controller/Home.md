Welcome to the Opencontrail wiki!

Overview:
* [Project Overview](https://github.com/Juniper/contrail-controller/wiki/Contrail:-Project-Overview)
* [Bug Management](https://github.com/Juniper/contrail-controller/wiki/Bug-management)
* [Installation and provisioning](https://github.com/Juniper/contrail-controller/wiki/OpenContrail-bring-up-and-provisioning)
* [Deploy OpenContrail 1.06](Install-and-Configure-OpenContrail-1.06)

Architecture:

* [Roles, Daemons and Ports](Roles-Daemons-Ports)
* [OpenContrail Internal Services](OpenContrail-Internal-Services)

Opencontrail Development:
* [Continuous Integration (CI)](OpenContrail-Continuous-Integration-(CI))
* [Code submission + review checklist](Code-Review-Checklist)
* [Developer sandbox](https://hub.docker.com/r/opencontrail/developer-sandbox/tags/) using a [container](https://github.com/Juniper/contrail-dev-env/blob/master/container/Dockerfile)

    ```docker run --name $USER-opencontrail-sandbox -it opencontrail/developer-sandbox:centos-7.4```

Releases:
* [Schedule ](https://github.com/Juniper/contrail-controller/wiki/Contrail-Release-Schedule#contrail-releases)

Provisioning:  
* [TTL configuration for Analytics](TTL-configuration-for-analytics-data)
* [Module Parameters for vRouter](Vrouter-Module-Parameters)

Packaging:
* [Contrail Docker Distribution](https://github.com/Juniper/contrail-controller/wiki/Contrail-Docker-Distribution#contrail-docker-distributions)  

Debug and Troubleshooting:
* [Checklist](Debug-Checklist)
* [Tips](Debug-Tips)
* [VRouter-Agent introspect](Contrail-Vrouter-Agent---Introspect)
* [Virtual DNS](vDNS-Debugging)
* [Scenarios](Scenario-Troubleshooting)
* [Dump sandesh trace buffer](Dump-sandesh-trace-buffer)
* [Disk Performance for database](Disk-performance-debug)

Maintenance Procedures:
* [Removing + Adding DB node](Removing_Adding_DB_Node)
* [Adding and Removing a hypervisor/compute node](Adding_Removing_Compute_Node)
* [Increasing Limits (nfiles/nprocs) for a service](Increasing_Service_Limits)
* [Analytics DB usage and purge](Contrail-Analytics-DB-data-purge)
* [Enabling kernel core dump on ubuntu](https://github.com/Juniper/contrail-vrouter/wiki/Enabling-kernel-core-dump-on-Ubuntu)

Features:
* [Simple Gateway](Simple-Gateway)
* [Virtual DNS and IPAM](DNS-and-IPAM)
* [Layer2 EVPN](EVPN)
* [Link Local Services](Link-local-services)
* [Metadata Service](Metadata-service)
* [Subnet options](Subnet-Options)
* [Extra DHCP options configuration](Extra-DHCP-Options)
* [Network Rate Limiting Configuration](https://techwiki.juniper.net/Documentation/Contrail/Contrail_Controller_Feature_Guide/Configuration/Configuring_Network_QoS_Parameters_in_VM)
* [VPC API support](VPC-API-support)
* [Support for Baremetal](Baremetal-Support)
* [Configuring Contrail SSL with Openstack](https://github.com/Juniper/contrail-controller/wiki/Configuring-Contrail-SSL-with-Openstack)
* [Customized field selection for ECMP load balancing](https://github.com/Juniper/contrail-controller/wiki/Customized-field-selection-for-ECMP-load-balancing)
* [RBAC](RBAC)
* [LLGR](https://github.com/Juniper/contrail-controller/wiki/Vrouter-agent-LLGR)
* [Resource Manager](https://github.com/Juniper/contrail-controller/wiki/Agent-Resource-Manager)
* [Kubernetes](https://github.com/Juniper/contrail-controller/wiki/Kubernetes)

Miscellaneous:
* [Blueprint Format](Blueprint-Format)
* [Python coding standard](https://github.com/Juniper/contrail-controller/wiki/Python-coding-style)
* [Moving Files Across Repos](https://github.com/Juniper/contrail-controller/wiki/Moving-Files-Across-Contrail-Repos-with-History-Intact)