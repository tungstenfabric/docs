Installing OpenStack Octavia LBaaS with RHOSP in Tungsten Fabric
====================================================================

Tungsten Fabric Release 2005 supports Octavia as LBaaS. The
deployment supports RHOSP and Juju platforms.

With Octavia as LBaaS, Tungsten Fabric is only maintaining network
connectivity and is not involved in any load balancing functions.

For each OpenStack load balancer creation, Octavia launches a VM known
as *amphora VM*. The VM starts the HAPROXY when listener is created for
the load balancer in OpenStack. Whenever the load balancer gets updated
in OpenStack, *amphora VM* updates the running HAPROXY configuration.
The *amphora VM* is deleted on deleting the load balancer.

Tungsten Fabric provides connectivity to *amphora VM* interfaces.
*Amphora VM* has two interfaces; one for management and the other for
data. The management interface is used by the Octavia services for the
management communication. Since, Octavia services are running in the
underlay network and *amphora VM* is running in the overlay network, SDN
gateway is needed to reach the overlay network. The data interface is
used for load balancing.

Follow the procedure to install OpenStack Octavia LBaaS with tungsten Fabric:

1. Deploy RHOSP13 with Tungsten Fabric without Octavia.

   ``openstack overcloud deploy --templates tripleo-heat-templates/ \--roles-file tripleo-heat-templates/roles_data_contrail_aio.yaml \-e environment-rhel-registration.yaml \-e tripleo-heat-templates/extraconfig/pre_deploy/rhel-registration/rhel-registration-resource-registry.yaml \-e tripleo-heat-templates/environments/contrail/contrail-services.yaml \-e tripleo-heat-templates/environments/contrail/contrail-net-single.yaml \-e tripleo-heat-templates/environments/contrail/contrail-plugins.yaml \-e misc_opts.yaml \-e contrail-parameters.yaml \-e docker_registry.yaml``

2. Make a copy of
   ``tripleo-heat-templates/docker/services/octavia/octavia-deployment-config.yaml``
   file.

   ``cp tripleo-heat-templates/docker/services/octavia/octavia-deployment-config.yaml tripleo-heat-templates/docker/services/octavia/octavia-deployment-config.bak``

3. Make the following changes in *generate_certs* section of the
   ``tripleo-heat-templates/docker/services/octavia/octavia-deployment-config.yaml``
   file.

   ::

      conditions:

        generate_certs:
            and:
            - get_param: OctaviaGenerateCerts
            - or:
              - equals:
                - get_param: StackAction
                - CREATE
              - equals:
                - get_param: StackAction
                - UPDATE

4. Deploy RHOSP13 with Octavia services.

   ``openstack overcloud deploy --templates tripleo-heat-templates/ \ --roles-file tripleo-heat-templates/roles_data_contrail_aio.yaml \-e environment-rhel-registration.yaml \-e tripleo-heat-templates/extraconfig/pre_deploy/rhel-registration/rhel-registration-resource-registry.yaml \-e tripleo-heat-templates/environments/contrail/contrail-services.yaml \-e tripleo-heat-templates/environments/contrail/contrail-net-single.yaml \-e tripleo-heat-templates/environments/contrail/contrail-plugins.yaml \-e tripleo-heat-templates/environments/services/octavia.yaml \-e misc_opts.yaml \-e contrail-parameters.yaml \-e docker_registry.yaml``

5. Rollback changes in
   ``tripleo-heat-templates/docker/services/octavia/octavia-deployment-config.yaml``
   file.

   ``cp tripleo-heat-templates/docker/services/octavia/octavia-deployment-config.bak tripleo-heat-templates/docker/services/octavia/octavia-deployment-config.yaml``

Here is an example for creating and testing load balancer:

Prerequisites:

-  You must have connectivity between Octavia controller and amphora
   instances,

-  You must have OpenStack services into LXD containers.

-  You must have separate interfaces for control plane and data plane.

1.  Create private network.

    ``openstack network create privateopenstack subnet create private --network private --subnet-range 10.10.10.0/24 --allocation-poolstart=10.10.10.50,end=10.10.10.70 --gateway none``

2.  Create security group.

    ``openstack security group create allow_allopenstack security group rule create --ingress --protocol any --prefix '0.0.0.0/0' allow_all``

3.  Check available flavors and images. You can create them, if needed.

    ``openstack flavor listopenstack image list``

4.  Create two servers for load balancer.

    ``openstack server create --flavor test_flavor --image cirros --security-group allow_all --network private cirros1openstack server create --flavor test_flavor --image cirros --security-group allow_all --network private cirros2``

5.  Create additional server to test load balancer.

    ``openstack server create --flavor test_flavor --image cirros --security-group allow_all --network private cirros-test``

6.  Check status and IP addresses.

    ``openstack server list --long``

7.  Create simple HTTP server on every cirros. Login on both the cirros
    instances and run following commands:

    ``MYIP=$(ifconfig eth0|grep 'inet addr'|awk -F: '{print $2}'| awk '{print $1}') while true; do echo -e "HTTP/1.0 200 OK\r\n\r\nWelcome to $MYIP" | sudo nc -l -p 80 ; done&``

8.  Create load balancer

    ``openstack loadbalancer create --name lb1 --vip-subnet-id private``

    Make sure *provisioning_status* is *Active*.

    ``openstack loadbalancer show lb1``

9.  Setup load balancer

    ``openstack loadbalancer listener create --protocol HTTP --protocol-port 80 --name listener1 lb1openstack loadbalancer show lb1  # Wait for the provisioning_status to be ACTIVE.openstack loadbalancer pool create --lb-algorithm ROUND_ROBIN --listener listener1 --protocol HTTP --name pool1openstack loadbalancer healthmonitor create --delay 5 --timeout 2 --max-retries 1 --type HTTP pool1openstack loadbalancer member create --subnet-id private --address 10.10.10.50 --protocol-port 80 pool1openstack loadbalancer member create --subnet-id private --address 10.10.10.51 --protocol-port 80 pool1``
    IP addresses 10.10.10.50 and 10.10.10.51 belong to VMs created with
    test http server in step
    `7 <rhosp-octavia.html#CreateSimpleHTTPServerOnEveryCirros>`__.
10. Check the status of load balancer.

    ``openstack loadbalancer show lb1  # Wait for the provisioning_status to be ACTIVE. openstack loadbalancer pool listopenstack loadbalancer pool show pool1openstack loadbalancer member list pool1openstack loadbalancer listener list``

11. Login to load balancer client and verify if round robin works.

    ``cirros@169.x.0.9's password:$ curl 10.10.10.50Welcome to 10.10.10.52$ curl 10.10.10.50Welcome to 10.10.10.53$ curl 10.10.10.50Welcome to 10.10.10.52$ curl 10.10.10.50Welcome to 10.10.10.53$ curl 10.10.10.50Welcome to 10.10.10.52$ curl 10.10.10.50Welcome to 10.10.10.53``


.. list-table:: **Release History Table**
      :header-rows: 1

      * - Release
        - Description
      * - 2005
        - Tungsten Fabric Release 2005 supports Octavia as LBaaS.