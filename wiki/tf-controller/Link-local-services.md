It might be required for a virtual machine to access specific services running on the fabric infrastructure. For example, a VM might be a nova client requiring access to the nova api service running in the fabric. Such access can be provided by configuring the required service as a link local service.

A link local address (use 169.254.169.x and a service port) is chosen for the specific service running on a TCP / UDP port on a server in the fabric. Once the link local service is configured, virtual machines can access the service using the link local address.

Link local service can be configured using the webui (Configure -> Infrastructure -> Link Local Services) or using the following command:

python /opt/contrail/utils/provision_linklocal.py --admin_user \<user\> --admin_password \<passwd\> 
--linklocal_service_name \<name\> --linklocal_service_ip \<169.254.169.x\> --linklocal_service_port \<port\> 
--ipfabric_service_ip \<fabric-ip\> --ipfabric_service_port \<fabric-port\>

### Example : Configure NTP

To configure NTP link local service, run the following on the config node:

python /opt/contrail/utils/provision_linklocal.py --admin_user \<user\> --admin_password \<passwd\> --linklocal_service_name ntp --linklocal_service_ip 169.254.169.254 --linklocal_service_port 123 --ipfabric_service_ip 172.17.28.5 --ipfabric_service_port 123

On the VM, to set the date and time via NTP, run:
`sudo ntpdate 169.254.169.254`

### Listing configured Linklocal services

* via curl:

Use correct configuration api server ip address

    curl -s $(curl -s http://localhost:8082/global-vrouter-configs | python -m json.tool | grep href | awk '{ print $2 }' | sed -e 's/"//g' -e 's/,//g') | python -m json.tool