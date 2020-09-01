Openstack allows VMs to access metadata by sending a HTTP request to the link local address 169.254.169.254. The metadata request from the VM is proxied to Nova, with additional HTTP header fields added. Nova uses these to identify the source instance and responds with appropriate metadata.

Contrail Vrouter acts as the proxy, trapping the metadata requests, adding the necessary header fields and sending the requests to the Nova Api server.

### Configuration
The metadata service is configured by setting the "linklocal-services" property on the "global-vrouter-config" object. The linklocal-services element should have an entry of the form:
 - linklocal-service-name = metadata
 - linklocal-service-ip = 169.254.169.254
 - linklocal-service-port = 80
 - ip-fabric-service-ip = [server-ip-address]
 - ip-fabric-service-port = [server-port]

This configuration can be done either thru UI or by using the following command:

python /opt/contrail/utils/provision_linklocal.py --admin_user \<user\> --admin_password \<passwd\> 
--linklocal_service_name metadata --linklocal_service_ip 169.254.169.254 --linklocal_service_port 80 
--ipfabric_service_ip \<nova-api-server-ip\> --ipfabric_service_port 8775

Contrail setup script creates this entry and hence there is no need to do this explicitly, if the setup scripts are used.

### Nova Configuration
The following has to be added to the DEFAULT section in nova.conf file to enable metadata proxy service. Restart the openstack-nova-api service after editing the nova.conf file.

service_quantum_metadata_proxy = True

Nova configuration also has a shared secret (configured as quantum_metadata_proxy_shared_secret = secret in nova.conf). The proxy uses this shared secret to add an instance-signature (HMAC SHA256 digest) in the HTTP header while sending the request to the Nova API server. If this shared secret is configured, the same has to be added in the agent configuration file in each compute node. An example agent.conf configuration is shown below. 

     <agent>
     ...
     <metadata-proxy>
            <shared-secret>secret</shared-secret>
     </metadata-proxy>
     ...
     </agent>

The shared secret can also be left empty (which is the default configuration).

### SSL support
SSL support is added for the http requests sent by VM for metadata service. Hence communication between vrouter agent and nova-api server can be secured using this. To enable this feature, certain configuration is required at Nova side as well as Agent side. 

Below configuration has to be added in default section of nova.conf file to enable this support for Nova:

- enabled_ssl_apis = metadata
- nova_metadata_protocol = https
- nova_metadata_insecure = False
- ssl_cert_file = cert.pem
- ssl_key_file  = privkey.pem
- ssl_ca_file   = cacert.pem

Below configuration has to be added in contrail-vrouter-agent.conf file to enable this support for Contrail vrouter agent:

- metadata_use_ssl = True
- metadata_client_cert = client_cert.pem
- metadata_client_key = client_key.pem
- metadata_ca_cert = cacert.pem

### Debugging 
To debug metadata transactions, below traces and statistics should help 

 http://compute-node:8085/Snh_SandeshTraceRequest?x=Metadata

 http://compute-node:8085/Snh_MetadataInfo?

vnswad should be listening on the port mentioned in "metadata_server_port" value got from the above query
 