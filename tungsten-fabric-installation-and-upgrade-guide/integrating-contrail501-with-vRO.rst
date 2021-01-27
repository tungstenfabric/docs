.. _integrating-contrail-release-50x-with-vmware-vrealize-orchestrator:

Integrating Tungsten Fabric Release 5.0.X with VMware vRealize Orchestrator
===========================================================================

A dedicated TF plugin is used to connect to VMware vRealize
Orchestrator (vRO). Tungsten Fabric 5.0 supported a Beta version of the
plugin. Starting with Tungsten Fabric 5.0.1, a fully supported version
of the plugin is available. The plugin is used to view the TF
controller configuration in the vRO inventory, and to modify
configurations by using vRO workflows. You can also create network
policies, security groups, and automate both simple and complex
workflows by using vRO.

Components of vRealize Orchestrator
-----------------------------------

vRO consists of the following components:

-  vRO Inventory—The vRO inventory displays the TF plugin and the
   TF node or endpoint. All TF plugin objects that represent
   your system are displayed in the vRO Inventory. Objects are displayed
   in a hierarchical order and are based on the TF schema.

   With Release 5.0, TF inventory objects such as projects,
   security groups, virtual networks, network IPAMs, network policies,
   ports, floating IP pools, and service templates are displayed in the
   vRO inventory. Relevant API objects are also displayed in the vRO
   inventory.

-  vRO Workflows—The vRO workflow is a process that manipulates objects
   in a vRO Inventory. Each plugin has a set of predefined workflows.
   vRO combines workflows from different plugins to create complex
   processes and manages them. Multiple workflows are used to create
   blueprints in vRA.

   .. note::

      VMware vCenter plugin workflows are represented as simple workflows
      in vRO plugin.

Tungsten Fabric workflows
-------------------------

You must connect to the TF controller or an endpoint before you
create TF workflows. You must use **Create TF controller
connection** to connect to an endpoint. You must use **Delete TF
controller connection** to terminate a connection with an endpoint. Once
you connect to the Control controller, the vRO plugin accesses the
TF inventory objects and then updates the vRO inventory with the
TF inventory objects.

The following workflows are defined for simple networking operations in
Tungsten Fabric 5.0:

-  Network

   -  Create network

   -  Delete network

   .. note::

      You must use the **Create network** workflow to create a network on
      the TF controller.

-  Network Policy

   -  Create network policy

   -  Add rule to network policy

   -  Remove network policy rule

   -  Delete network policy

-  Security policy

   -  Create security group

   -  Add rule to security group

   -  Edit security group

   -  Remove security group rule

   -  Delete security group

-  Service Instance

   -  Add port tuple to service instance

   -  Create service instance

   -  Delete service instance

   -  Remove port tuple from service instance

-  Network IPAM

-  Port

-  Project

-  Service Template

-  Virtual Network

-  Floating IP

   -  Create floating IP

   -  Delete floating IP

-  Floating IP pools

   -  Create floating IP pool

   -  Delete floating IP pool

   -  Edit floating IP pool

Starting with Tungsten Fabric 5.0.1, the following workflows are also
defined:

-  Tag

   -  Create global tag

   -  Create tag in project

   -  Delete tag

-  Tag Type

   -  Create tag type

   -  Delete tag type

-  Network Policy

   -  Edit network policy rule

-  Security policy

   -  Edit security group rule

-  Service Health Check

   -  Create service health check

   -  Add service instance to service health check

   -  Remove service instance from service health check

   -  Edit service health check

   -  Delete service health check

-  Project

   -  Add application policy set to project

   -  Remove application policy set to project

   -  Add tag to project

   -  Remove tag from project

-  Virtual Network

   -  Add tag to virtual network

   -  Remove tag from virtual network

-  Virtual Machine Interface (VMI) - Port

   -  Add tag to port

   -  Remove tag from port

-  Service Group

   -  Create service group in policy management

   -  Create service group in project

   -  Add service to service group

   -  Edit service of service group

   -  Remove service from service group

   -  Delete service group

-  Address Group

   -  Create global address group

   -  Create address group in project

   -  Add subnet to address group

   -  Remove subnet from address group

   -  Delete address group

   -  Add label to address group

   -  Remove label from address group

-  Application Policy Set

   -  Create global application policy set

   -  Create application policy set in project

   -  Add firewall policy to application policy set

   -  Remove firewall policy from application policy set

   -  Add tag to application policy set

   -  Remove tag from application policy set

   -  Delete application policy set

-  Firewall Policy

   -  Create global firewall policy

   -  Create firewall policy in project

   -  Add firewall rule to firewall policy

   -  Remove firewall rule from firewall policy

   -  Delete firewall policy

-  Firewall Rule

   -  Create global firewall rule

   -  Create firewall rule in project

   -  Edit firewall rule

   -  Delete firewall rule

 
