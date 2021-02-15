Configuring Network QoS Parameters
==================================

Overview
--------

You can use the OpenStack Nova command-line interface (CLI) to specify a
quality of service (QoS) setting for a virtual machine’s network
interface, by setting the ``quota`` of a Nova flavor. Any virtual
machine created with that Nova flavor will inherit all of the specified
QoS settings. Additionally, if the virtual machine that was created with
the QoS settings has multiple interfaces in different virtual networks,
the same QoS settings will be applied to all of the network interfaces
associated with the virtual machine. The QoS settings can be specified
in unidirectional or bidirectional mode.

The ``quota`` driver in Neutron converts QoS parameters into ``libvirt``
network settings of the virtual machine.

The QoS parameters available in the quota driver only cover rate
limiting the network interface. There are no specifications available
for policy-based QoS at this time.

QoS Configuration Examples
--------------------------

Although the QoS setting can be specified in quota by using either
Horizon or CLI, quota creation using CLI is more robust and stable,
therefore, creating by CLI is the recommended method.

Example
~~~~~~~

CLI for Nova flavor has the following format:

::

   nova flavor-key <flavor_name> set quota:vif_<direction> _<param_name> = value

where:

``<flavor_name>`` is the name of an existing Nova flavor.

``vif_<direction>_<param_name>`` is the inbound or outbound QoS data
name.

QoS ``vif`` types include the following:

-  ``vif_inbound_average`` lets you specify the average rate of inbound
   (receive) traffic, in kilobytes/sec.

-  ``vif_outbound_average`` lets you specify the average rate of
   outbound (transmit) traffic, in kilobytes/sec.

-  Optional: ``vif_inbound_peak``\ and ``vif_outbound_peak`` specify the
   maximum rate of inbound and outbound traffic, respectively, in
   kilobytes/sec.

-  Optional: ``vif_inbound_burst`` and ``vif_outbound_peak`` specify the
   amount of kilobytes that can be received or transmitted,
   respectively, in a single burst at the peak rate.

Details for various QoS parameters for ``libvirt`` can be found at
http://libvirt.org/formatnetwork.html.

The following example shows an inbound average of 800 kilobytes/sec, a
peak of 1000 kilobytes/sec, and a burst amount of 30 kilobytes.

::

   nova flavor-key m1.small set quota:vif_inbound_average=800
   nova flavor-key m1.small set quota:vif_inbound_peak=1000
   nova flavor-key m1.small set quota:vif_inbound_burst=30

The following is an example of specified outbound parameters:

::

   nova flavor-key m1.small set quota:vif_outbound_average=800
   nova flavor-key m1.small set quota:vif_outbound_peak=1000
   nova flavor-key m1.small set quota:vif_outbound_burst=30

After the Nova flavor is configured for QoS, a virtual machine instance
can be created, using either Horizon or CLI. The instance will have
network settings corresponding to the nova flavor-key, as in the
following:

::

   <interface type="ethernet">
         <mac address="02:a3:a0:87:7f:61"/>
         <model type="virtio"/>
         <script path=""/>
         <target dev="tapa3a0877f-61"/>
         <bandwidth>
           <inbound average="800" peak="1000" burst="30"/>
           <outbound average="800" peak="1000" burst="30"/>
         </bandwidth>
       </interface>
       
Limitations
-----------

-  The stock ``libvirt`` does not support rate limiting of ``ethernet``
   interface types. Consequently, settings like those in the example for
   the guest interface will not result in any ``tc qdisc`` settings for
   the corresponding tap device in the host.

-  The ``nova flavor-key rxtx_factor`` takes a float as an input and
   acts as a scaling factor for receive (inbound) and transmit
   (outbound) throughputs. This key is only available to Neutron
   extensions (private extensions). The TF Neutron plugin doesn’t
   implement this private extension. Consequently, setting the
   ``nova flavor-key rxtx_factor``\ will not have any effect on the QoS
   setting of the network interface(s) of any virtual machine created
   with that nova flavor.

-  The outbound rate limits of a virtual machine interface are not
   strictly achieved. The outbound throughput of a virtual machine
   network interface is always less than the average outbound limit
   specified in the virtual machine's libvirt configuration file. The
   same behavior is also seen when using a Linux bridge.

 
