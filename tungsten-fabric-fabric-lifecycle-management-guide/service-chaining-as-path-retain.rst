Retaining the AS Path Attribute in a Service Chain
==================================================

:date: 2020-12-02

Service chaining allows two virtual networks to communicate with each
other using a service policy or network policy. The VNs communicate
through services instances defined in the network policy. Service
instances can be physical network functions or virtual network
functions.

For data to traverse between VNs, the BGP route attributes are modified
according to the network policy. One such BGP attribute, is the AS path
attribute. AS path is a sequence of autonomous systems that network
packets traverse. By default, the AS path is nullified while leaking
routes from the source to the destination network in a service chain.
Starting with Contrail Networking Release 2011, you can configure the AS
path to be retained in the routes re-originated from the destination VN
to the source VN in a service chain. You also have the ability to enable
or disable the path retention for selected service chains.

.. note::

   The AS path retention feature works only for virtual network functions.

You can enable or disable the **Retain AS Path** option while
configuring the network policy. A network policy is unique to a service
chain and configuring the knob at the policy level will apply that
feature to that service chain and its component service instances
defined by the policy. Even when service instances are shared between
multiple service chains, the same service instance can behave
differently in different service chains based on the **Retain AS Path**
knob in the policy configuration.

To configure the AS Path attribute to be retained in the routes
re-originated from the destination VN to the source VN in a service
chain:

1. Navigate to :menuselection:`Overlay > Network Policies > Create Network Policy`.

   The **Network Policy** tab of the **Create Network Policy** page is
   displayed.

2. Enter a name for the policy in the **Policy Name** field.

3. Edit the fields in the **Policy Rule(s)** section as per your policy
   requirement.

4. Click **Advanced Options** and edit the fields displayed as per your
   policy requirement.

5. Select the **Retain AS Path** check box if you want to retain the AS
   Path between the source and destination virtual networks. The check
   box is disabled, by default.

6. Click **Create** to create the network policy.

   The **Network Policies** page is displayed. You can now attach the
   network policies to the required VNs.

.. raw:: html

   <div class="table">

.. raw:: html

   <div class="caption">

Release History Table

.. raw:: html

   </div>

.. raw:: html

   <div class="table-row table-head">

.. raw:: html

   <div class="table-cell">

Release

.. raw:: html

   </div>

.. raw:: html

   <div class="table-cell">

Description

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="table-row">

.. raw:: html

   <div class="table-cell">

`2011 <#jd0e15>`__

.. raw:: html

   </div>

.. raw:: html

   <div class="table-cell">

Starting with Contrail Networking Release 2011, you can configure the AS
path to be retained in the routes re-originated from the destination VN
to the source VN in a service chain. You also have the ability to enable
or disable the path retention for selected service chains.

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   </div>

 
