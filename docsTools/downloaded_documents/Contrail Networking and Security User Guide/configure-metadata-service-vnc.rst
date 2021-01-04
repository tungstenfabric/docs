Configuring Metadata Service
============================

 

OpenStack enables virtual machines to access metadata by sending an HTTP
request to the link-local address 169.254.169.254. The metadata request
from the virtual machine is proxied to Nova with additional HTTP header
fields that Nova uses to identify the source instance, then responds
with appropriate metadata.

In Contrail, the vRouter acts as the proxy, by trapping the metadata
requests, adding the necessary header fields, and sending the requests
to the Nova API server.

The metadata service is configured by setting the ``linklocal-services``
property on the ``global-vrouter-config`` object.

Use the following elements to configure the ``linklocal-services``
element for metadata service:

-  ``linklocal-service-name = metadata``

-  ``linklocal-service-ip = 169.254.169.254``

-  ``linklocal-service-port = 80``

-  ``ip-fabric-service-ip = [server-ip-address]``

-  ``ip-fabric-service-port = [server-port]``

The ``linklocal-services`` properties can be set from the Contrail UI
(**Configure > Infrastructure > Link Local Services**) or by using the
following command:

``python /opt/contrail/utils/provision_linklocal.py --admin_user <user> --admin_password <passwd>  --linklocal_service_name metadata --linklocal_service_ip 169.254.169.254 --linklocal_service_port 80 --ipfabric_service_ip --ipfabric_service_port 8775``

 
