Support for Amazon VPC APIs on Contrail OpenStack
=================================================

 

Overview of Amazon Virtual Private Cloud
----------------------------------------

The current Grizzly release of OpenStack supports Elastic Compute Cloud
(EC2) API translation to OpenStack Nova, Quantum, and Keystone calls.
EC2 APIs are used in Amazon Web Services (AWS) and virtual private
clouds (VPCs) to launch virtual machines, assign IP addresses to virtual
machines, and so on. A VPC provides a container where applications can
be launched and resources can be accessed over the networking services
provided by the VPC.

Contrail enhances its use of EC2 APIs to support the Amazon VPC APIs.

The Amazon VPC supports networking constructs such as: subnets, DHCP
options, elastic IP addresses, network ACLs, security groups, and route
tables. The Amazon VPC APIs are now supported on the Openstack Contrail
distribution, so users of the Amazon EC2 APIs for their VPC can use the
same scripts to move to an Openstack Contrail solution.

**Euca2ools** are command-line tools for interacting with Amazon Web
Services (AWS) and other AWS-compatible web services, such as OpenStack.
**Euca2ools** have been extended in OpenStack Contrail to add support
for the Amazon VPC, similar to the support that already exists for the
Amazon EC2 CLI.

For more information about Amazon VPC and AWS EC2, see:

-  Amazon VPC documentation:
   http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Introduction.html

-  Amazon VPC API list:
   http://docs.aws.amazon.com/AWSEC2/latest/APIReference/query-apis.html

Mapping Amazon VPC Features to OpenStack Contrail Features
----------------------------------------------------------

The following table compares Amazon VPC features to their equivalent
features in OpenStack Contrail.

Table 1: Amazon VPC and OpenStack Contrail Feature Comparison

================== ===========================
Amazon VPC Feature OpenStack Contrail Feature
================== ===========================
VPC                Project
Subnets            Networks (Virtual Networks)
DHCP options       IPAM
Elastic IP         Floating IP
Network ACLs       Network ACLs
Security Groups    Security Groups
Route Table        Route Table
================== ===========================

VPC and Subnets Example
-----------------------

When creating a new VPC, the user must provide a classless inter-domain
routing (CIDR) block of which all subnets in this VPC will be part.

In the following example, a VPC is created with a CIDR block of
10.1.0.0/16. A subnet is created within the VPC CIDR block, with a CIDR
block of 10.1.1.0/24. The VPC has a default network ACL named
``acl-default``.

All subnets created in the VPC are automatically associated to the
default network ACL. This association can be changed when a new network
ACL is created. The last command in the list below creates a virtual
machine using the image ``ami-00000003`` and launches with an interface
in ``subnet-5eb34ed2``.

.. raw:: html

   <div id="jd0e133" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   # euca-create-vpc 10.1.0.0/16
   VPC VPC:vpc-8352aa59 created

   # euca-describe-vpcs
   VpcId           CidrBlock       DhcpOptions
   -----           ---------       -----------
   vpc-8352aa59    10.1.0.0/16     None

   # euca-create-subnet -c 10.1.1.0/24 vpc-8352aa59
   Subnet: subnet-5eb34ed2 created

   # euca-describe-subnets
   Subnet-id       Vpc-id          CidrBlock
   ---------       ------          ---------
   subnet-5eb34ed2 vpc-8352aa59    10.1.1.0/24

   # euca-describe-network-acls
   AclId                               
   -----
   acl-default(def)
   vpc-8352aa59
                   Rule    Dir     Action  Proto   Port  Range   Cidr
                   ----    ---     ------  -----   ----  -----   ----
                   100     ingress allow   -1      0     65535   0.0.0.0/0
                   100     egress  allow   -1      0     65535   0.0.0.0/0
                   32767   ingress deny    -1      0     65535   0.0.0.0/0
                   32767   egress  deny    -1      0     65535   0.0.0.0/0


                   Assocation          SubnetId            AclId
                   ----------          --------            ------------
                   aclassoc-0c549d66   subnet-5eb34ed2     acl-default

   # euca-run-instances -s subnet-5eb34ed2 ami-00000003

.. raw:: html

   </div>

.. raw:: html

   </div>

Euca2ools CLI for VPC and Subnets
---------------------------------

The following ``euca2ools`` CLI commands are used to create, define, and
delete VPCs and subnets:

-  ``euca-create-vpc``

-  ``euca-delete-vpc``

-  ``euca-describe-vpcs``

-  ``euca-create-subnet``

-  ``euca-delete-subnet``

-  ``euca-describe-subnets``

Security in VPC: Network ACLs Example
-------------------------------------

Network ACLs support ingress and egress rules for traffic classification
and filtering. The network ACLs are applied at a subnet level.

In the following example, a new ACL, ``acl-ba7158``, is created and an
existing subnet is associated to the new ACL.

.. raw:: html

   <div id="jd0e183" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   # euca-create-network-acl vpc-8352aa59
   acl-ba7158c

   # euca-describe-network-acls
   AclId
   -----
   acl-default(def)
   vpc-8352aa59
                   Rule    Dir     Action  Proto   Port  Range   Cidr
                   ----    ---     ------  -----   ----  -----   ----
                   100     ingress allow   -1      0     65535   0.0.0.0/0
                   100     egress  allow   -1      0     65535   0.0.0.0/0
                   32767   ingress deny    -1      0     65535   0.0.0.0/0
                   32767   egress  deny    -1      0     65535   0.0.0.0/0


                   Assocation          SubnetId            AclId
                   ----------          --------            ------------
                   aclassoc-0c549d66   subnet-5eb34ed2     acl-default
   AclId
   -----
   acl-ba7158c
   vpc-8352aa59
                   Rule    Dir     Action  Proto   Port  Range   Cidr
                   ----    ---     ------  -----   ----  -----   ----
                   32767   ingress deny    -1      0     65535   0.0.0.0/0
                   32767   egress  deny    -1      0     65535   0.0.0.0/0




   # euca-replace-network-acl-association -a aclassoc-0c549d66 acl-ba7158c
   aclassoc-0c549d66

   # euca-describe-network-acls
   AclId
   -----
   acl-default(def)
   vpc-8352aa59
                   Rule    Dir     Action  Proto   Port  Range   Cidr
                   ----    ---     ------  -----   ----  -----   ----
                   100     ingress allow   -1      0     65535   0.0.0.0/0
                   100     egress  allow   -1      0     65535   0.0.0.0/0
                   32767   ingress deny    -1      0     65535   0.0.0.0/0
                   32767   egress  deny    -1      0     65535   0.0.0.0/0


                   Assocation          SubnetId            AclId
                   ----------          --------            ------------

   AclId
   -----
   acl-ba7158c
   vpc-8352aa59
                   Rule    Dir     Action  Proto   Port  Range   Cidr
                   ----    ---     ------  -----   ----  -----   ----
                   32767   ingress deny    -1      0     65535   0.0.0.0/0
                   32767   egress  deny    -1      0     65535   0.0.0.0/0


                   Assocation          SubnetId            AclId
                   ----------          --------            ------------
                   aclassoc-0c549d66   subnet-5eb34ed2     acl-ba7158c

.. raw:: html

   </div>

.. raw:: html

   </div>

Euca2ools CLI for Network ACLs
------------------------------

The following ``euca2ools`` CLI commands are used to create, define, and
delete VPCs and subnets:

-  ``euca-create-network-acl``

-  ``euca-delete-network-acl``

-  ``euca-replace-network-acl-association``

-  ``euca-describe-network-acls``

-  ``euca-create-network-acl-entry``

-  ``euca-delete-network-acl-entry``

-  ``euca-replace-network-acl-entry``

Security in VPC: Security Groups Example
----------------------------------------

Security groups provide virtual machine level ingress/egress controls.
Security groups are applied to virtual machine interfaces.

In the following example, a new security group is created. The rules can
be added or removed for the security group based on the commands listed
for ``euca2ools``. The last line launches a virtual machine using the
newly created security group.

.. raw:: html

   <div id="jd0e237" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   # euca-describe-security-groups

   GroupId         VpcId           Name                    Description
   -------         -----           ----                    -----------
   sg-6d89d7e2     vpc-8352aa59    default


                   Direction       Proto   Start   End     Remote
                   ---------       -----   -----   ---     ------
                   Ingress         any     0       65535   [0.0.0.0/0]
                   Egress          any     0       65535   [0.0.0.0/0]

   # euca-create-security-group -d "TestGroup" -v vpc-8352aa59 testgroup
   GROUP   sg-c5b9d22a     testgroup       TestGroup

   # euca-describe-security-groups


   GroupId         VpcId           Name                    Description
   -------         -----           ----                    -----------
   sg-6d89d7e2     vpc-8352aa59    default


                   Direction       Proto   Start   End     Remote
                   ---------       -----   -----   ---     ------
                   Ingress         any     0       65535   [0.0.0.0/0]
                   Egress          any     0       65535   [0.0.0.0/0]


   GroupId         VpcId           Name                    Description
   -------         -----           ----                    -----------
   sg-c5b9d22a     vpc-8352aa59    testgroup               TestGroup


                   Direction       Proto   Start   End     Remote
                   ---------       -----   -----   ---     ------
                   Egress          any     0       65535   [0.0.0.0/0]

   # euca-run-instances -s subnet-5eb34ed2 -g testgroup ami-00000003

.. raw:: html

   </div>

.. raw:: html

   </div>

Euca2ools CLI for Security Groups
---------------------------------

The following ``euca2ools`` CLI commands are used to create, define, and
delete security groups:

-  ``euca-create-security-group``

-  ``euca-delete-security-group``

-  ``euca-describe-security-groups``

-  ``euca-authorize-security-group-egress``

-  ``euca-authorize-security-group-ingress``

-  ``euca-revoke-security-group-egress``

-  ``euca-revoke-security-group-ingress``

Elastic IPs in VPC
------------------

Elastic IPs in VPCs are equivalent to the floating IPs in the Contrail
Openstack solution.

In the following example, a floating IP is requested from the system and
assigned to a particular virtual machine. The prerequisite is that the
provider or Contrail administrator has provisioned a network named
“public” and allocated a floating IP pool to it. This “public” floating
IP pool is then internally used by the tenants to request public IP
addresses that they can use and attach to virtual machines.

.. raw:: html

   <div id="jd0e288" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   # euca-allocate-address --domain vpc
   ADDRESS 10.84.14.253    eipalloc-78d9a8c9 

   # euca-describe-addresses --filter domain=vpc
   Address         Domain    AllocationId       InstanceId(AssociationId)
   -------         ------    ------------       -------------------------
   10.84.14.253    vpc       eipalloc-78d9a8c9

   # euca-associate-address  -a eipalloc-78d9a8c9 i-00000008
   ADDRESS eipassoc-78d9a8c9

   # euca-describe-addresses --filter domain=vpc
   Address         Domain    AllocationId       InstanceId(AssociationId)
   -------         ------    ------------       -------------------------
   10.84.14.253    vpc       eipalloc-78d9a8c9  i-00000008(eipassoc-78d9a8c9)

.. raw:: html

   </div>

.. raw:: html

   </div>

Euca2ools CLI for Elastic IPs
-----------------------------

The following ``euca2ools`` CLI commands are used to create, define, and
delete elastic IPs:

-  ``euca-allocate-address``

-  ``euca-release-address``

-  ``euca-describe-addresses``

-  ``euca-associate-address``

-  ``euca-disassociate-address``

Euca2ools CLI for Route Tables
------------------------------

Route tables can be created in an Amazon VPC and associated with
subnets. Traffic exiting a subnet is then looked up in the route table
and, based on the route lookup result, the next hop is chosen.

The following ``euca2ools`` CLI commands are used to create, define, and
delete route tables:

-  ``euca-create-route-table``

-  ``euca-delete-route-table``

-  ``euca-describe-route-tables``

-  ``euca-associate-route-table``

-  ``euca-disassociate-route-table``

-  ``euca-replace-route-table-association``

-  ``euca-create-route``

-  ``euca-delete-route``

-  ``euca-replace-route``

Supported Next Hops
-------------------

The supported next hops are:

-  Local Next Hop

   Designating local next hop indicates that all subnets in the VPC are
   reachable for the destination prefix.

-  Internet Gateway Next Hop

   This next hop is used for traffic destined to the Internet. All
   virtual machines using the Internet gateway next hop are required to
   use an Elastic IP to reach the Internet, because the subnet IPs are
   private IPs.

-  NAT instance

   To create this next hop, the user needs to launch a virtual machine
   that provides network address translation (NAT) service. The virtual
   machine has two interfaces: one internal and one external, both of
   which are automatically created. The only requirement here is that a
   “public” network should have been provisioned by the admin, because
   the second interface of the virtual machine is created in the
   “public” network.

Internet Gateway Next Hop Euca2ools CLI
---------------------------------------

The following ``euca2ools`` CLI commands are used to create, define, and
delete Internet gateway next hop:

-  ``euca-attach-internet-gateway``

-  ``euca-create-internet-gateway``

-  ``euca-delete-internet-gateway``

-  ``euca-describe-internet-gateways``

-  ``euca-detach-internet-gateway``

NAT Instance Next Hop Euca2ools CLI
-----------------------------------

The following ``euca2ools`` CLI commands are used to create, define, and
delete NAT instance next hops:

-  ``euca-run-instances``

-  ``euca-terminate-instances``

Example: Creating a NAT Instance with Euca2ools CLI
---------------------------------------------------

The following example creates a NAT instance and creates a default route
pointing to the NAT instance.

.. raw:: html

   <div id="jd0e451" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   # euca-describe-route-tables
   RouteTableId    Main    VpcId               AssociationId       SubnetId
   ------------    ----    -----               -------------       --------
   rtb-default     yes     vpc-8352aa59        rtbassoc-0c549d66   subnet-5eb34ed2

                   Prefix                  NextHop
                   ------                  -------
                   10.1.0.0/16             local

   # euca-describe-images
   IMAGE   ami-00000003    None (ubuntu)       2c88a895fdea4461a81e9b2c35542130 
   IMAGE   ami-00000005    None (nat-service)  2c88a895fdea4461a81e9b2c35542130 

   # euca-run-instances ami-00000005

   # euca-create-route --cidr 0.0.0.0/0 -i i-00000006 rtb-default

   # euca-describe-route-tables
   RouteTableId    Main    VpcId               AssociationId       SubnetId
   ------------    ----    -----               -------------       --------
   rtb-default     yes     vpc-8352aa59        rtbassoc-0c549d66   subnet-5eb34ed2

                   Prefix                  NextHop
                   ------                  -------
                   10.1.0.0/16             local
                   0.0.0.0/0               i-00000006

.. raw:: html

   </div>

.. raw:: html

   </div>

 
