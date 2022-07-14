Using Security Groups with Virtual Machines (Instances)
=======================================================

:date: 2015-11-30

Security Groups Overview
------------------------

A **security group** is a container for security group rules. Security
groups and security group rules allow administrators to specify the type
of traffic that is allowed to pass through a port. When a virtual
machine (VM) is created in a virtual network (VN), a security group can
be associated with the VM when it is launched. If a security group is
not specified, a port is associated with a default security group. The
default security group allows both ingress and egress traffic. Security
rules can be added to the default security group to change the traffic
behavior.

Creating Security Groups and Adding Rules
-----------------------------------------

A default security group is created for each project. You can add
security rules to the default security group and you can create
additional security groups and add rules to them. The security groups
are then associated with a VM, when the VM is launched or at a later
date.

To add rules to a security group:

1. From the OpenStack interface, click the :guilabel:`Project` tab, select
   :guilabel:`Access & Security`, and click the :guilabel:`Security Groups` tab.

   Any existing security groups are listed under the :guilabel:`Security Groups`
   tab, including the default security group.

   |Figure 1: Security Groups|

2. Select the :guilabel:`default-security-group` and click :guilabel:`Edit Rules` in the
   :guilabel:`Actions` column.

   The :guilabel:`Edit Security Group Rules` window is displayed. Any
   rules already associated with the security group are listed.

   |Figure 2: Edit Security Group Rules|

3. Click :guilabel:`Add Rule` to add a new rule.

   |Figure 3: Add Rule|

   Table 1: Add Rule Fields

   +-----------------+---------------------------------------------------+
   | Column          | Description                                       |
   +=================+===================================================+
   | **IP Protocol** | Select the IP protocol to apply for this rule:    |
   |                 | TCP, UDP, ICMP.                                   |
   +-----------------+---------------------------------------------------+
   | **From Port**   | Select the port from which traffic originates to  |
   |                 | apply this rule. For TCP and UDP, enter a single  |
   |                 | port or a range of ports. For ICMP rules, enter   |
   |                 | an ICMP type code.                                |
   +-----------------+---------------------------------------------------+
   | **To Port**     | The port to which traffic is destined that        |
   |                 | applies to this rule, using the same options as   |
   |                 | in the :guilabel:`From Port` field.               |
   +-----------------+---------------------------------------------------+
   | **Source**      | Select the source of traffic to be allowed by     |
   |                 | this rule. Specify subnet—the CIDR IP address or  |
   |                 | address block of the inter-domain source of the   |
   |                 | traffic that applies to this rule, or you can     |
   |                 | choose security group as source. Selecting        |
   |                 | security group as source allows any other         |
   |                 | instance in that security group access to any     |
   |                 | other instance via this rule.                     |
   +-----------------+---------------------------------------------------+

4. Click :guilabel:`Create Security Group` to create additional security groups.

   The :guilabel:`Create Security Group` window is displayed.

   Each new security group has a unique 32-bit security group ID and an
   ACL is associated with the configured rules.

   |Figure 4: Create Security Group|

5. When an instance is launched, there is an opportunity to associate a
   security group.

   In the :guilabel:`Security Groups` list, select the security group name to
   associate with the instance.

   |Figure 5: Associate Security Group at Launch Instance|

6. You can verify that security groups are attached by viewing the
   ``SgListReq`` and ``IntfReq`` associated with the ``agent.xml``.

 

.. |Figure 1: Security Groups| image:: images/s041610.gif
.. |Figure 2: Edit Security Group Rules| image:: images/s041860.gif
.. |Figure 3: Add Rule| image:: images/s041862.gif
.. |Figure 4: Create Security Group| image:: images/s041861.gif
.. |Figure 5: Associate Security Group at Launch Instance| image:: images/s041863.gif