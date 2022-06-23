
=====================================
Release Notes: Tungsten Fabric R21.12
=====================================


Supported Platforms and Versions
--------------------------------


.. _Table 1:

*Table 1* : Supported Release Versions

        +--------------------------------+------------------+-----------+----------+
        | Tungsten Fabric Release        | Operating System | OpenStack | Deployer |
        +================================+==================+===========+==========+
        | Tungsten Fabric Release R21.05 |     RHEL 8.2     | OSP16     |  OSPd16  |
        +--------------------------------+------------------+-----------+----------+


Support for Dynamic Address Learning with IPVLAN Networking
------------------------------------------------------------

In the latest release of Tungsten Fabric a vRouter can learn multiple MAC-IP address bindings for a single MAC address when Dynamic Address Learning is enabled in a virtual network.

For more information see: :ref:`Dynamic MAC/IP Learning <DynamicMacIP>`.



Support for Layer 3 Multihoming
-------------------------------

It is now possible to provide high availability to vRouters with Layer 3 multihoming, without the need for MC-LAG or bond interfaces.

For more information see: LINK MISSING

Support for Flow Stickiness in a Load-Balanced System
------------------------------------------------------

Improved flow stickiness is a feature that helps to minimize flow remapping across equal cost multipath (ECMP) groups in a load-balanced system. Flow stickiness reduces such flow being remapped and retains the flow with the original path when the ECMP group's member change. When a flow is affected by a member change, vRouter reprograms flow table and rebalances the flow.

For more information see: LINK MISSING

Support for User-Defined Tags in Security Policy
----------------------------------------------------

In this latest release security policy allows optional user-defined tags which enables you to define tag IDs along with tag names. You can also create a predefined tag type with user-defined tag value ID.

For more information see: LINK MISSING


Upgrade Contrail Networking Through Kubernetes and/or Red Hat OpenShift
------------------------------------------------------------------------

Starting in Contrail Networking Release 21.3, you can update Contrail Networking through Kubernetes and/or Red Hat OpenShift. You can use this procedure to update Contrail Networking deployed by the Tungsten Fabric (TF) Operator.

For more information see: LINK MISSING


Configure MTU For Virtual Networks
------------------------------------

Starting in Contrail Networking Release 21.3, you can configure Maximum Transmission Unit (MTU) for virtual networks(VN) in the Contrail Command UI. To configure MTU, select Overlay>Virtual Networks>Create Virtual Network. In the Advanced option, you can configure the MTU value in the MTU field. The available range is 0-9216. The Dynamic Host Configuration Protocol (DHCP) will not use the MTU value and it will not be inherited by VMIs attached to the VN.


