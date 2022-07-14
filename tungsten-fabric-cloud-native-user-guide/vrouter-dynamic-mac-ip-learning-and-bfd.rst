.. _DynamicMacIP:

vRouter Dynamic MAC/IP Address Learning and BFD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the latest Tungsten Fabric Release the vRouter agent dynamically learns the MAC address-IP address binding of a pod deployed on a virtual machine (VM). This enables the vRouter agent to perform an efficient pod to pod communication in nested Kubernetes scenarios, or other situations where many MAC/IP addresses are originated from a VM.

In previous releases, the MAC address - IP address of a nested workloads is assigned using Allowed Address Pairs. Tungsten Fabric is unable to perform pod to pod communication unless it has the reachability information of the pods hosted by the VMs.

A vRouter can learn multiple MAC-IP address bindings for a single MAC address when Dynamic Address Learning is enabled in a virtual network. In previous releases, a vRouter could only learn a single MAC-IP address binding per MAC address.

The vRouter automatically learns multiple MAC-IP address bindings when a single MAC address is bound to multiple IP addresses and Dynamic Address Learning is enabled; no additional user configuration to support learning of the MAC-IP address bindings is needed or possible. Cloud-networking environments using Openstack orchestration and Tungsten Fabric can seamlessly support the learning of IPVLAN MAC address-IP address bindings over VM interfaces as a result of the vRouters ability to learn multiple MAC-IP address bindings to a single MAC address.

In the Virtual Network configuration of the Tungsten Fabric user interface (UI), the Dynamic Address Learning checkbox must be enabled while creating a virtual network. This enables the vRouter agent to learn the MAC address-IP address of the pods connected to the virtual network.

In this release Tungsten Fabric also supports Bidirectional Forwarding and Detection (BFD) based health check to verify the liveliness of a pod. In the user interface (UI), you must create a BFD health check service, where the Health Check Type is assigned as VN IP List. The BFD session is enabled for a list of target IP addresses. In this release Tungsten Fabric supports IPv4 target IP addresses. The vRouter agent learns these IP addresses through the MAC address - IP address learning feature. The BFD health check session is initiated, when the vRouter agent learns the target IP address assigned to the BFD health check service. The BFD health check monitors the target list of health check for newly learnt IP addresses. If the BFD session is detected as DOWN, the vRouter agent deletes the routes generated for the MAC address - IP address of a pod learned by the vRouter.

The vRouter agent also sends address resolution protocol (ARP) packets in regular intervals to newly learnt IP addresses. The vRouter agent performs this action to check an endpoint's liveliness. If an endpoint responds to the ARP request sent by the vRouter, the endpoint is considered as UP. If the endpoint does not respond to the ARP packets, the endpoint is considered as DOWN. If vRouter identifies a endpoint as DOWN, it deletes the routes generated for the respective MAC address-IP address of the endpoint.

You must perform the following steps to enable the vRouter to dynamically learn the MAC address - IP address of an endpoint:

1. Navigate to Configure > Networking > Networks  page. Click Create to create a new virtual network.
Alternatively, you can also edit the properties of an existing virtual network. To edit an existing virtual network, select a virtual network from the displayed list and click the Edit (gear) icon.

2. Follow the steps given Create Virtual Network to create a virtual network.
In the Create Virtual Network page, select MAC Learning to enable vRouter to learn the MAC address - IP address of endpoints dynamically.

3. Click Create to create a VN where the vRouter can learn the MAC address - IP address of the pods connected to the VN.
The Virtual Networks page is displayed listing the newly created virtual network.

