Server Requirements and Supported Platforms
===========================================

 

This topic discusses server requirements in a Contrail Networking
cluster.

Each server must have a minimum of:

-  64 GB memory.

-  300 GB hard drive.

-  4 CPU cores.

-  At least one Ethernet port.

A server can either be a physical device or a virtual machine. For
scalability and availability reasons, it is highly recommended to use
physical servers in most use cases whenever possible.

Server role assignments vary by environment. All non-compute roles can
be configured in each controller node if desired in your topology.

All installation images are available in repositories and can also be
downloaded from `Contrail Downloads
page <https://www.juniper.net/support/downloads/?p=contrail#sw>`__.

The Contrail image includes the following software:

-  All dependent software packages needed to support installation and
   operation of OpenStack and Contrail.

-  Contrail Controller software – all components.

-  OpenStack release currently in use for Contrail.

All components required for installing the Contrail Controller are
available for each Contrail release, for the supported Linux operating
systems and versions, and for the supported versions of OpenStack.

For a list of supported platforms for all Contrail Networking releases,
see `Contrail Networking Supported Platforms
List <https://www.juniper.net/documentation/en_US/release-independent/contrail/topics/reference/contrail-supported-platforms.pdf>`__  .

Access ``Container Tags`` are located at `README Access to Contrail
Registry
20XX </documentation/en_US/contrail20/information-products/topic-collections/release-notes/readme-contrail-20.pdf>`__  .

If you need access to Contrail docker private secure registry, e-mail
contrail-registry@juniper.net for Contrail container registry
credentials.

 
