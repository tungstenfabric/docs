### Introduction
Nova CLI is used to specify the quality of service (QoS) setting of a virtual machine’s network interface. This is achieved by setting the quota of a nova flavor. Any virtual machine (VM) created with that nova flavor will inherit all of its QoS settings. If a VM has multiple virtual network interfaces in different virtual networks (VN), the same QoS settings will be applied to all of the VM’s network interfaces. These settings may be specified in unidirectional or in bidirectional mode. Quota driver in neutron converts these QoS parameters into libvirt network settings of the VM. Example usage is shown in the next section. The QoS parameters as specified via quota covers the aspect of rate limiting of the network interface, it doesn’t address policy based QoS as of now.

### Usage
The configuration can be specified via CLI and Horizon. However, in our observation, the quota creation via Horizon seems to be buggy and it has a limit of input characters upto 25. So, we would recommend using CLI only.

CLI takes the following format:

`nova flavor-key <flavor_name> set quota:vif_<direction> _<param_name> = value`

where, flavor_name is the name of an existing nova flavor,
vif_<direction>_<param_name> is the inbound or outbound QoS data name, which can be of following types:

* 	vif_inbound_average - average rate of inbound (receive) traffic, in kilobytes/sec.
* 	vif_outbound_ average – average rate of outbound (transmit) traffic, in kilobytes/sec.
* 	The optional parameters, vif_inbound_peak and vif_outbound_peak specify the maximum rate of inbound and outbound traffic respectively, in kilobytes/sec.
* 	Optional parameters, vif_inbound_burst and vif_outbound_peak specify the amount of kilobytes that can be received or transmitted respectively in a single burst at the peak rate.

Following example shows an inbound average of 1000 kilobytes/sec, peak of 1024 kilobytes/sec and a burst amount of 32 kilobytes. Details of these parameters can be found at http://libvirt.org/formatnetwork.html

`nova flavor-key m1.small set quota:vif_inbound_average=1000`  
`nova flavor-key m1.small set quota:vif_inbound_peak=1024`  
`nova flavor-key m1.small set quota:vif_inbound_burst=32`  

Similarly, the outbound parameters could be specified as follows:  

`nova flavor-key m1.small set quota:vif_outbound_average=1000`  
`nova flavor-key m1.small set quota:vif_outbound_peak=1024`  
`nova flavor-key m1.small set quota:vif_outbound_burst=32`  

Once the nova flavor is configured for QoS, an instance may be created either via CLI or horizon. The VM instance will have network settings corresponding to the above configurations as follows,

```xml
<interface type="ethernet">
      <mac address="02:a3:a0:87:7f:61"/>
      <model type="virtio"/>
      <script path=""/>
      <target dev="tapa3a0877f-61"/>
      <bandwidth>
        <inbound average="1000" peak="1024" burst="32"/>
        <outbound average="1000" peak="1024" burst="32"/>
      </bandwidth>
    </interface>
```
### Libvirt Issue and Workaround
The stock libvirt doesn’t have support for rate limiting of ‘ethernet’ interface types.  The above xml settings of the vm network interface will not result in any tc qdisc settings for the tap device, `tapa3a0877f-61` in the host. So, the vm network traffic will not be throttled as per the above rate limiting configuration data. There is a launchpad bug id, which describes what fix needs to be applied to get it working. Here is a link to the Launchpad bug id for the above issue:  
https://bugs.launchpad.net/juniperopenstack/+bug/1367095