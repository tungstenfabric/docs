#contrail-heat

## Release R2.x

In Release 2.x, we supported a few contrail heat resources which were hand coded.
These contrail-heat resources are Version 1 resources (**OS::Contrail::\<ResourceName\>**).
Here is the link of all the hand-written plugin resources supported by contrail-heat in Release 2.x
https://github.com/Juniper/contrail-heat/tree/master/contrail_heat/resources

* OS::Contrail::AttachPolicy  
* OS::Contrail::NetworkIpam  
* OS::Contrail::NetworkPolicy  
* OS::Contrail::PhysicalInterface  
* OS::Contrail::PhysicalRouter  
* OS::Contrail::PortTuple  
* OS::Contrail::RouteTable  
* OS::Contrail::ServiceHealthCheck  
* OS::Contrail::ServiceInstance  
* OS::Contrail::ServiceTemplate  
* OS::Contrail::VirtualMachineInterface  
* OS::Contrail::VirtualNetwork  
* OS::Contrail::VnSubnet  

## Release R3.x

With Release 3.0.2, contrail-heat resources and templates are being auto-generated from the Schema.
These contrail-heat resources are Version 2 resources (**OS::ContrailV2::\<ResourceName\>**).

The generated resources/templates are part of the python-contrail package and located in _**/usr/lib/python2.7/dist-packages/vnc_api/gen/heat/**_ directory in the target installation. This directory has three sub-directories

* **resources**: This sub-directory contains all the resources for the contrail-heat plugin. It runs in the context of the heat-engine service.
* **templates**: This sub-directory contains template for each resource. They are sample templates with every possible parameter in the schema. They should be used as a reference when you build up more complex templates for your network design.
* **env**: This sub-directories contains environment for input to each template.

Here is the link of all the generated plugin resources supported by contrail-heat in Release 3.x

https://github.com/Juniper/contrail-heat/tree/master/generated/resources

### Deprecation of heat resources

Heat resources Version 1 with hierarchy OS::Contrail::\<ResourceName\> will be deprecated. Hence new service chains should not be created using V1 heat templates. These heat resources will be available only to help with transition to the new version. Existing V1 templates will continue working for till further notice. There won't be any new features or bug fixes for Heat resources version 1.


### Release 3.0.0 and heat
In Contrail 3.0.0 release Heat versioning is broken. Contrail 3.x + Heat requires 3.0.2 as a minimum. Customers running previous 3.0.0 and want to use Contrail Heat resources should upgrade to 3.0.2 or later. In other words, all R3.0 releases prior to 3.0.2 will not support heat.

### Version-1 heat templates in 3.0.2 and later
The Version-1 heat templates used in R2.x releases, would still work in the R3.x release but they are being deprecated. 
We advise customers to rewrite the heat templates with the version-2 format. Example templates are here.  
https://github.com/Juniper/contrail-heat/tree/master/contrail_heat/new_templates

## Service chaining support in Release 3.x
Starting Release 3.0.2 a new version for service chaining (V2) has been introduced with **port-tuple**. Service chaining should now use port-tuple based mechanism in V2.

### Service chaining using Version-1 Service-templates
In R2.x, the service-monitor daemon would create a VM object for each VM based service
instance and create/attach ports to the VM. The VM object was being usedto bind the
VM based service instances to the ports.

In this model, heat engine knew only about the service instance object. The objects created 
by the service-monitor daemon (such as VM, ports, ...) were not visible to heat. 
We saw issues with this approach and decided on the new design of port-tuples.

Release 3.x will support service-chaining version 1 and service-chaining version 2. **However service chaining version 1 is not supported with heat version 2**. We recommend that customers should rewrite their heat-templates using version-2 service-chaining (port-tuple way). 

Here is a link to template using the version-1 service-chaining using version-1 contrail-heat resources  
https://github.com/Juniper/contrail-heat/blob/master/contrail_heat/template/service_chain.yaml

### Service chaining using Version-2 Service-templates

With the new design of service-chaining, user can create ports and bind them to the created VM based service instance. All the objects created are directly visible to the heat-engine and thus managed by heat directly.

A new object called PortTuple was added to the schema whcih contains all the ports of a VM.
The workflow is as follows:

- User creates a port-tuple
- User creates ports and marks them left/right/mgmt etc and adds them to a port-tuple.
- User links the port-tuple to a service instance
- User launches the virtual-machine using the ports in a port-tuple