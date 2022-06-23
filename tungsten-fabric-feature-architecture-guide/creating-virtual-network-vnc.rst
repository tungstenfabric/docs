.. _CreateVN:

Creating a Virtual Network with OpenStack TF
============================================

:date: 2020-01-06

You can create virtual networks in Tungsten Fabric from the
OpenStack. The following procedure shows how to create a virtual network
when using OpenStack.

1. To create a virtual network when using OpenStack TF, select
   :menuselection:`Project > Network > Networks`. The :guilabel:`Networks` page is displayed.

   |Figure 1: Networks Page|

2. Click :guilabel:`Create Network`. The :guilabel:`Create Network` window is displayed.

   |Figure 2: Create Networks|

   |Figure 3: Subnet and Gateway Details|

3. Click the :guilabel:`Network` and :guilabel:`Subnet` tabs to complete the fields in
   the :guilabel:`Create Network` window. See field descriptions below.

   Table 1: Create Network Fields

   +---------------------+-----------------------------------------------+
   | Field               | Description                                   |
   +=====================+===============================================+
   | **Network Name**    | Enter a name for the network.                 |
   +---------------------+-----------------------------------------------+
   | **Subnet Name**     | Enter a name for the subnetwork.              |
   +---------------------+-----------------------------------------------+
   | **Network Address** | Enter the network address in CIDR format.     |
   +---------------------+-----------------------------------------------+
   | **IP Version**      | Select IPv4 or IPv6.                          |
   +---------------------+-----------------------------------------------+
   | **Gateway IP**      | Optionally, enter an explicit gateway IP      |
   |                     | address for the IP address block. Check the   |
   |                     | Disable Gateway box if no gateway is to be    |
   |                     | used.                                         |
   +---------------------+-----------------------------------------------+

4. Click the :guilabel:`Subnet Details` tab to specify the Allocation Pool, DNS
   Name Servers, and Host Routes.

   |Figure 4: Additional Subnet Attributes|

5. To save your network, click :guilabel:`Create` , or click :guilabel:`Cancel` to
   discard your work and start over.

 

.. |Figure 1: Networks Page| image:: images/s008528.png
.. |Figure 2: Create Networks| image:: images/s008529.png
.. |Figure 3: Subnet and Gateway Details| image:: images/s008530.png
.. |Figure 4: Additional Subnet Attributes| image:: images/s008531.png
