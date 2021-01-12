Installing OpenStack Octavia LBaaS with RHOSP in Contrail Networking
====================================================================

 

Contrail Networking Release 2005 supports Octavia as LBaaS. The
deployment supports RHOSP and Juju platforms.

With Octavia as LBaaS, Contrail Networking is only maintaining network
connectivity and is not involved in any load balancing functions.

For each OpenStack load balancer creation, Octavia launches a VM known
as *amphora VM*. The VM starts the HAPROXY when listener is created for
the load balancer in OpenStack. Whenever the load balancer gets updated
in OpenStack, *amphora VM* updates the running HAPROXY configuration.
The *amphora VM* is deleted on deleting the load balancer.

Contrail Networking provides connectivity to *amphora VM* interfaces.
*Amphora VM* has two interfaces; one for management and the other for
data. The management interface is used by the Octavia services for the
management communication. Since, Octavia services are running in the
underlay network and *amphora VM* is running in the overlay network, SDN
gateway is needed to reach the overlay network. The data interface is
used for load balancing.

Follow the procedure to install OpenStack Octavia LBaaS with Contrail
Networking:

1. Deploy RHOSP13 with Contrail Networking without Octavia.

   .. raw:: html

      <div id="jd0e45" class="sample" dir="ltr">

   .. raw:: html

      <div id="jd0e46" dir="ltr">

   ``openstack overcloud deploy --templates tripleo-heat-templates/ \--roles-file tripleo-heat-templates/roles_data_contrail_aio.yaml \-e environment-rhel-registration.yaml \-e tripleo-heat-templates/extraconfig/pre_deploy/rhel-registration/rhel-registration-resource-registry.yaml \-e tripleo-heat-templates/environments/contrail/contrail-services.yaml \-e tripleo-heat-templates/environments/contrail/contrail-net-single.yaml \-e tripleo-heat-templates/environments/contrail/contrail-plugins.yaml \-e misc_opts.yaml \-e contrail-parameters.yaml \-e docker_registry.yaml``

   .. raw:: html

      </div>

   .. raw:: html

      </div>

2. Make a copy of
   ``tripleo-heat-templates/docker/services/octavia/octavia-deployment-config.yaml``
   file.

   .. raw:: html

      <div id="jd0e72" class="sample" dir="ltr">

   .. raw:: html

      <div id="jd0e73" dir="ltr">

   ``cp tripleo-heat-templates/docker/services/octavia/octavia-deployment-config.yaml tripleo-heat-templates/docker/services/octavia/octavia-deployment-config.bak``

   .. raw:: html

      </div>

   .. raw:: html

      </div>

3. Make the following changes in *generate_certs* section of the
   ``tripleo-heat-templates/docker/services/octavia/octavia-deployment-config.yaml``
   file.

   .. raw:: html

      <div id="jd0e84" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

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

   .. raw:: html

      </div>

   .. raw:: html

      </div>

4. Deploy RHOSP13 with Octavia services.

   .. raw:: html

      <div id="jd0e90" class="sample" dir="ltr">

   .. raw:: html

      <div id="jd0e91" dir="ltr">

   ``openstack overcloud deploy --templates tripleo-heat-templates/ \ --roles-file tripleo-heat-templates/roles_data_contrail_aio.yaml \-e environment-rhel-registration.yaml \-e tripleo-heat-templates/extraconfig/pre_deploy/rhel-registration/rhel-registration-resource-registry.yaml \-e tripleo-heat-templates/environments/contrail/contrail-services.yaml \-e tripleo-heat-templates/environments/contrail/contrail-net-single.yaml \-e tripleo-heat-templates/environments/contrail/contrail-plugins.yaml \-e tripleo-heat-templates/environments/services/octavia.yaml \-e misc_opts.yaml \-e contrail-parameters.yaml \-e docker_registry.yaml``

   .. raw:: html

      </div>

   .. raw:: html

      </div>

5. Rollback changes in
   ``tripleo-heat-templates/docker/services/octavia/octavia-deployment-config.yaml``
   file.

   .. raw:: html

      <div id="jd0e117" class="sample" dir="ltr">

   .. raw:: html

      <div id="jd0e118" dir="ltr">

   ``cp tripleo-heat-templates/docker/services/octavia/octavia-deployment-config.bak tripleo-heat-templates/docker/services/octavia/octavia-deployment-config.yaml``

   .. raw:: html

      </div>

   .. raw:: html

      </div>

Here is an example for creating and testing load balancer:

Prerequisites:

-  You must have connectivity between Octavia controller and amphora
   instances,

-  You must have OpenStack services into LXD containers.

-  You must have separate interfaces for control plane and data plane.

1.  Create private network.

    .. raw:: html

       <div id="jd0e141" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e142" dir="ltr">

    ``openstack network create privateopenstack subnet create private --network private --subnet-range 10.10.10.0/24 --allocation-poolstart=10.10.10.50,end=10.10.10.70 --gateway none``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

2.  Create security group.

    .. raw:: html

       <div id="jd0e151" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e152" dir="ltr">

    ``openstack security group create allow_allopenstack security group rule create --ingress --protocol any --prefix '0.0.0.0/0' allow_all``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

3.  Check available flavors and images. You can create them, if needed.

    .. raw:: html

       <div id="jd0e159" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e160" dir="ltr">

    ``openstack flavor listopenstack image list``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

4.  Create two servers for load balancer.

    .. raw:: html

       <div id="jd0e167" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e168" dir="ltr">

    ``openstack server create --flavor test_flavor --image cirros --security-group allow_all --network private cirros1openstack server create --flavor test_flavor --image cirros --security-group allow_all --network private cirros2``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

5.  Create additional server to test load balancer.

    .. raw:: html

       <div id="jd0e175" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e176" dir="ltr">

    ``openstack server create --flavor test_flavor --image cirros --security-group allow_all --network private cirros-test``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

6.  Check status and IP addresses.

    .. raw:: html

       <div id="jd0e181" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e182" dir="ltr">

    ``openstack server list --long``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

7.  Create simple HTTP server on every cirros. Login on both the cirros
    instances and run following commands:

    .. raw:: html

       <div id="jd0e187" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e188" dir="ltr">

    ``MYIP=$(ifconfig eth0|grep 'inet addr'|awk -F: '{print $2}'| awk '{print $1}') while true; do echo -e "HTTP/1.0 200 OK\r\n\r\nWelcome to $MYIP" | sudo nc -l -p 80 ; done&``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

8.  Create load balancer

    .. raw:: html

       <div id="jd0e193" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e194" dir="ltr">

    ``openstack loadbalancer create --name lb1 --vip-subnet-id private``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

    Make sure *provisioning_status* is *Active*.

    .. raw:: html

       <div id="jd0e204" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e205" dir="ltr">

    ``openstack loadbalancer show lb1``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

9.  Setup load balancer

    .. raw:: html

       <div id="jd0e210" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e211" dir="ltr">

    ``openstack loadbalancer listener create --protocol HTTP --protocol-port 80 --name listener1 lb1openstack loadbalancer show lb1  # Wait for the provisioning_status to be ACTIVE.openstack loadbalancer pool create --lb-algorithm ROUND_ROBIN --listener listener1 --protocol HTTP --name pool1openstack loadbalancer healthmonitor create --delay 5 --timeout 2 --max-retries 1 --type HTTP pool1openstack loadbalancer member create --subnet-id private --address 10.10.10.50 --protocol-port 80 pool1openstack loadbalancer member create --subnet-id private --address 10.10.10.51 --protocol-port 80 pool1``

    .. raw:: html

       </div>

    IP addresses 10.10.10.50 and 10.10.10.51 belong to VMs created with
    test http server in step
    `7 <rhosp-octavia.html#CreateSimpleHTTPServerOnEveryCirros>`__.

    .. raw:: html

       </div>

10. Check the status of load balancer.

    .. raw:: html

       <div id="jd0e230" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e231" dir="ltr">

    ``openstack loadbalancer show lb1  # Wait for the provisioning_status to be ACTIVE. openstack loadbalancer pool listopenstack loadbalancer pool show pool1openstack loadbalancer member list pool1openstack loadbalancer listener list``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

11. Login to load balancer client and verify if round robin works.

    .. raw:: html

       <div id="jd0e244" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e245" dir="ltr">

    ``cirros@169.x.0.9's password:$ curl 10.10.10.50Welcome to 10.10.10.52$ curl 10.10.10.50Welcome to 10.10.10.53$ curl 10.10.10.50Welcome to 10.10.10.52$ curl 10.10.10.50Welcome to 10.10.10.53$ curl 10.10.10.50Welcome to 10.10.10.52$ curl 10.10.10.50Welcome to 10.10.10.53``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

.. raw:: html

   <div class="table">

.. raw:: html

   <div class="caption">

Release History Table

.. raw:: html

   </div>

.. raw:: html

   <div class="table-row table-head">

.. raw:: html

   <div class="table-cell">

Release

.. raw:: html

   </div>

.. raw:: html

   <div class="table-cell">

Description

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="table-row">

.. raw:: html

   <div class="table-cell">

`2005 <#jd0e11>`__

.. raw:: html

   </div>

.. raw:: html

   <div class="table-cell">

Contrail Networking Release 2005 supports Octavia as LBaaS.

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   </div>

 
