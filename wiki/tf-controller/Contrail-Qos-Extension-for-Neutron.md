# 1. Introduction  #
This blueprint gives details about the list of QoS features that the 
Contrail Neutron API will support in the Contrail 4.0 release.

# 2. Problem statement #
Contrail vRouter data path supports different QoS features such as marking,
mapping to forwarding class, from 3.x release. Bandwidth limiting and
policing are not supported features yet. Details
of what the data path supports can be found at
https://github.com/Juniper/contrail-controller/wiki/QoS

However,the configuration of these QoS features through Horizon or the Neutron CLI
was not supported since the Contrail Neutron extensions API did not implement 
the Neutron QoS extensions. More details on what is supported in the Neutron 
CLI can be found here in this blueprint. 
https://review.openstack.org/#/c/88599/14/specs/liberty/qos-api-extension.rst

This blueprint scheduled for Contrail 4.0 gives the details of how the
Contrail Neutron Extensions will add support to the existing Neutron 
QoS features.

# 3. Proposed solution #
## 3.1 The Neutron QoS Model ##
The Neutron QoS Model operates on the idea of policies and rules. Policies
can be associated to a Port or a network (QosPolicy -> Port/Network). 
The QosPolicy can be linked to a base QosRule. New rules could be 
introduced by adding new submodels to QoSRule. A QoSPolicy can be
associated to a VM (Interface/Port) or a complete network.

The following Neutron QoS objects are supported in the Newton release of 
Openstack.

**QosPolicy** - id, name, description, shared, tenant_id

**QoSRule** - id, qos_policy_id, type, direction, tenant_id

**QoSBandwidthLimitRule** - qos_rule_id, max_kbps, max_burst_kbps (this is derived
from the QoSRule object)
Details here - http://specs.openstack.org/openstack/neutron-specs/specs/liberty/qos-api-extension.html

**QoSDSCPMarkingRule** - Qos_Policy_id, dscp_mark (This is derived from the QosRule object)
details here - https://specs.openstack.org/openstack/neutron-specs/specs/newton/ml2-qos-with-dscp.html

**QosMinimumBandwidthRule** - id, qos_policy_id, min_kpbs, direction`. (ToDo: To check whether egress bandwidth is supported)
Details here - https://specs.openstack.org/openstack/neutron-specs/specs/newton/ml2-qos-minimum-egress-bw-support.html

The following maps how the above mentioned entities are associated with each other.


	+-----------------+   +--------------------------+        +----------+ 
	+   Port/Network  + ->+-> +     QOS Policy       + ---->  +  QosRule + 
	+-----------------+	  +--------------------------+        + ---------+
															QoSBandwidthLimitRule
															QoSDSCPMarkingRule
															QosMinimumBandwidthRule (ToDo: Check support)

## 3.2 The Contrail QoS Model ##
As part of the solution, the Contrail Neutron API should obtain the above mentioned 
Neutron entities as JSON and convert that into relevant Contrail API calls with 
relevant parameters that the Contrail API server understands.

In Contrail, the above Neutron model could be mapped by the following two constructs:

* Queueing on the fabric interface, which involves queues, scheduling of queues 
  and drop policy AND
* Forwarding class, which involves marking and identifying which queue to use 
  and thus controls how packets are sent to fabric.

Tenants have the ability to define which forwarding class their traffic can use. 
So, in QOS config, they can decide which packets can use what forwarding class.

QOS config object has a mapping table from incoming DSCP or .1p to forwarding class mapping.
Additionally QOS config can be applied to a virtual-network, interface or network-policy.

        +--------------------------+       +---------------------+       +----------+ 
        +     QOS config object    + ----> +  Forwarding class   + ----> +  Queue   + 
        +--------------------------+       +---------------------+       + ---------+

However, current data path implementation does not change the packets header but only changes the tunnel header DSCP marking. This means that when the packet ingresses in the Destination VM it will not have corresponding DSCP marking since the tunnel header is stripped.

### Traffic originated by Virtual machine interface ###

* If interface sends a IP packet to another VM in remote compute node, then this DSCP value in IP header value would be used to look up in cos-config table, and the tunnel header would be marked with DSCP, 802.1p and MPLS EXP bit as specified by forwarding-class.
* If VM sends a layer 2 non IP packet with 802.1p value, then corresponding 802.1p value would be used to look into qos-config table and corresponding forwarding-class DSCP, 802.1p and MPLS EXP value would be written to tunnel header.
    
## 3.3 Neutron CLI Examples ##

The following Neutron CLIs are introduced (valid from Newton)

### 3.3.1 QoS Policy manipulation: ###
		neutron qos-policy-list
		neutron qos-policy-create  <policy-name> [--description policy-description]
									[--shared True]
		neutron qos-policy-update  <policy-name-or-id> [--description ....]
									[--name ...]

		neutron qos-policy-show    <policy-name-or-id>
		neutron qos-policy-delete  <policy-name-or-id>

### 3.3.2 QoS Policy Rules manipulation: ###

		neutron qos-dscp-marking-rule-create <policy-id> –dscp_mark <value>
		neutron qos-dscp-marking-rule-show <mark-rule-id> <policy-id>
		neutron qos-dscp-marking-rule-list <policy-id>
		neutron qos-dscp-marking-rule-update <mark-rule-id> <policy-id> –dscp_mark <value>
		neutron qos-dscp-marking-rule-delete <mark-rule-id> <policy-id>
		
### 3.3.3 Attach/Detach port/net to policy: ###

	neutron port-create NET-NAME-OR-ID --qos-policy <policy-name-or-id> ...
	neutron net-create NAME --qos-policy <policy-name-or-id> ....

	neutron port-update <port-id> --qos-policy <policy-name-or-id>
	neutron net-update <net-name-or-id> --qos-policy <policy-name-or-id>

	neutron port-update <port-id> --no-qos-policy

## 3.4 Neutron - Contrail Association ##
a. When a Neutron QosPolicy is created, a corresponding call to create
   Contrail QosConfig object along with a default Contrail QoSForwardingClass
   and the QosConfig object and the QosForwardingClass is linked.
   
b. When a Neutron QosRule is created, a corresponding call to create
   Contrail QosQueue object is created and linked with the Contrail QosForwardingClass
   that was created in the previous step.
   
c. When a Neutron attach policy to a port/network is configured, then we will
   attach the Contrail QosConfig object to the corresponding VMI or VN.

## 3.5  User workflow impact ##
First, create a QoS policy and its DSCP marking rule:

		neutron qos-policy-create mark-dscp

		Created a new policy:
		+-------------+--------------------------------------+
		| Field       | Value                                |
		+-------------+--------------------------------------+
		| description |                                      |
		| id          | 0ee1c673-5671-40ca-b55f-4cd4bbd999c7 |
		| name        | mark-dscp                            |
		| rules       |                                      |
		| shared      | False                                |
		| tenant_id   | 85b859134de2428d94f6ee910dc545d8     |
		+-------------+--------------------------------------+

		$ neutron qos-dscp-marking-rule-create mark-dscp --dscp-mark 5

		Created a new dscp_mark_rule:
		+----------------+--------------------------------------+
		| Field          | Value                                |
		+----------------+--------------------------------------+
		| id             | 92ceb52f-170f-49d0-9528-976e2fee2d6f |
		| dscp_mark      | 5                                  |
		+----------------+--------------------------------------+
		
Second, associate the created policy with an existing neutron port. 
In order to do this, user extracts the port id to be associated to the already 
created policy. In the next example, we will assign the mark-dscp policy to the VM.
	
		$ neutron port-update 88101e57-76fa-4d12-b0e0-4fc7634b874a --qos-policy mark-dscp
		Updated port: 88101e57-76fa-4d12-b0e0-4fc7634b874a

# 4. Implementation #
## 4.1 Assignee(s) ##
Ranjeet Ramalingam <rranjeet@juniper.net>

## 4.2 Work items ##

# 5. Documentation Impact #
Contrail QoS documentation needs to be modified to add the above mentioned
ways to configure QoS. Currently, new nova flavours with the relevant libvirt
parameters are used to provision QoS parameters.

# 6. References #
[1] Contrail QoS Wiki - https://github.com/Juniper/contrail-controller/wiki/QoS

[2] Neutron QoS API Models and Extension - 
https://specs.openstack.org/openstack/neutron-specs/specs/liberty/qos-api-extension.html

[3] Supported Openstack QoS Config -
http://docs.openstack.org/mitaka/networking-guide/config-qos.html

[4] - Neutron QoS DSCP Mapping - 
https://specs.openstack.org/openstack/neutron-specs/specs/newton/ml2-qos-with-dscp.html
