Installing OpenStack Octavia LBaaS with Juju Charms in Contrail Networking
==========================================================================

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

Follow the procedure to install OpenStack Octavia LBaaS in Canonical
deployment:

1. Prepare Juju setup with OpenStack Train version and Octavia overlay
   bundle.

   Refer to `Sample octavia-bundle.yaml file`_ output.

   .. raw:: html

      <div id="jd0e49" class="sample" dir="ltr">

   .. raw:: html

      <div id="jd0e50" dir="ltr">

   ``juju deploy --overlay=./octavia-bundle.yaml ./contrail-bundle.yaml``

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   or

   Add Octavia service after deploying the main bundle on the existing
   cluster.

   .. raw:: html

      <div id="jd0e56" class="sample" dir="ltr">

   .. raw:: html

      <div id="jd0e57" dir="ltr">

   ``juju deploy --overlay=./octavia-bundle.yaml --map-machines=existing ./contrail-bundle.yaml``

   .. raw:: html

      </div>

   .. raw:: html

      </div>

2. Prepare ssh key for amphora VM. Add the options in the
   ``octavia-bundle.yaml`` file.

   .. raw:: html

      <div id="jd0e65" class="sample" dir="ltr">

   .. raw:: html

      <div id="jd0e66" dir="ltr">

   ``ssh-keygen -f octavia # generate the key base64 octavia.pub # print public key data``

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   Add the following options to Octavia options.

   .. raw:: html

      <div id="jd0e70" class="sample" dir="ltr">

   .. raw:: html

      <div id="jd0e71" dir="ltr">

   ``amp-ssh-pub-key: # paste public key data here amp-ssh-key-name: octavia``

   .. raw:: html

      </div>

   .. raw:: html

      </div>

3. Generate certificates.

   .. raw:: html

      <div id="jd0e76" class="sample" dir="ltr">

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      rm -rf demoCA/
      mkdir -p demoCA/newcerts
      touch demoCA/index.txt
      touch demoCA/index.txt.attr
      openssl genrsa -passout pass:foobar -des3 -out issuing_ca_key.pem 2048
      openssl req -x509 -passin pass:foobar -new -nodes -key issuing_ca_key.pem \
          -config /etc/ssl/openssl.cnf \
          -subj "/C=US/ST=Somestate/O=Org/CN=www.example.com" \
          -days 30 \
          -out issuing_ca.pem
      openssl genrsa -passout pass:foobar -des3 -out controller_ca_key.pem 2048
      openssl req -x509 -passin pass:foobar -new -nodes \
              -key controller_ca_key.pem \
          -config /etc/ssl/openssl.cnf \
          -subj "/C=US/ST=Somestate/O=Org/CN=www.example.com" \
          -days 30 \
          -out controller_ca.pem
      openssl req \
          -newkey rsa:2048 -nodes -keyout controller_key.pem \
          -subj "/C=US/ST=Somestate/O=Org/CN=www.example.com" \
          -out controller.csr
      openssl ca -passin pass:foobar -config /etc/ssl/openssl.cnf \
          -cert controller_ca.pem -keyfile controller_ca_key.pem \
          -create_serial -batch \
          -in controller.csr -days 30 -out controller_cert.pem
      cat controller_cert.pem controller_key.pem > controller_cert_bundle.pem
      juju config octavia \
          lb-mgmt-issuing-cacert="$(base64 controller_ca.pem)" \
          lb-mgmt-issuing-ca-private-key="$(base64 controller_ca_key.pem)" \
          lb-mgmt-issuing-ca-key-passphrase=foobar \
          lb-mgmt-controller-cacert="$(base64 controller_ca.pem)" \
          lb-mgmt-controller-cert="$(base64 controller_cert_bundle.pem)"

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   Make sure all the units are in *active* or *blocked* state.

4. Configure vault service.

   1. SSH into the machine where vault service is installed.

      .. raw:: html

         <div id="jd0e94" class="sample" dir="ltr">

      .. raw:: html

         <div id="jd0e95" dir="ltr">

      ``juju ssh vault/0``

      .. raw:: html

         </div>

      .. raw:: html

         </div>

   2. Export vault address and run ``init``.

      .. raw:: html

         <div id="jd0e103" class="sample" dir="ltr">

      .. raw:: html

         <div id="jd0e104" dir="ltr">

      ``export VAULT_ADDR='http://localhost:8200'/snap/bin/vault operator init -key-shares=5 -key-threshold=3``

      .. raw:: html

         </div>

      .. raw:: html

         </div>

      It will print 5 unseal keys and initial root token.

   3. Call unseal command by using any three of the five printed unseal
      keys.

      .. raw:: html

         <div id="jd0e113" class="sample" dir="ltr">

      .. raw:: html

         <div id="jd0e114" dir="ltr">

      ``/snap/bin/vault operator unseal Key1/snap/bin/vault operator unseal Key2/snap/bin/vault operator unseal Key3``

      .. raw:: html

         </div>

      .. raw:: html

         </div>

   4. Export initial root token.

      .. raw:: html

         <div id="jd0e123" class="sample" dir="ltr">

      .. raw:: html

         <div id="jd0e124" dir="ltr">

      ``export VAULT_TOKEN="..."``

      .. raw:: html

         </div>

      .. raw:: html

         </div>

   5. Create user token.

      .. raw:: html

         <div id="jd0e129" class="sample" dir="ltr">

      .. raw:: html

         <div id="jd0e130" dir="ltr">

      ``/snap/bin/vault token create -ttl=10m``

      .. raw:: html

         </div>

      .. raw:: html

         </div>

   6. Exit from vault’s machine and initialize vault’s charm with the
      user token.

      .. raw:: html

         <div id="jd0e135" class="sample" dir="ltr">

      .. raw:: html

         <div id="jd0e136" dir="ltr">

      ``juju run-action --wait vault/leader authorize-charm token=”...”``

      .. raw:: html

         </div>

      .. raw:: html

         </div>

5. Create amphora image.

   .. raw:: html

      <div id="jd0e141" class="sample" dir="ltr">

   .. raw:: html

      <div id="jd0e142" dir="ltr">

   ``juju run-action --wait octavia-diskimage-retrofit/leader retrofit-image``

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   For more details, refer to
   https://docs.openstack.org/project-deploy-guide/charm-deployment-guide/latest/app-octavia.html#amphora-image.

6. Install *python-openstackclient* and *python-octaviaclient* and
   create management network for Octavia.

   You must create these objects in *services* project.

   .. raw:: html

      <div id="jd0e163" class="sample" dir="ltr">

   .. raw:: html

      <div id="jd0e164" dir="ltr">

   ``project=$(openstack project list --domain service_domain | awk '/services/{print $2}')openstack network create octavia --tag charm-octavia --project $projectopenstack subnet create --subnet-range 172.x.0.0/24 --network octavia --tag charm-octavia octavia# security group for octaviaopenstack security group create octavia --tag charm-octavia --project $projectopenstack security group rule create --ingress --ethertype IPv4 --protocol icmp octaviaopenstack security group rule create --ingress --ethertype IPv6 --protocol icmp octaviaopenstack security group rule create --ingress --ethertype IPv4 --protocol tcp --dst-port 22:22 octaviaopenstack security group rule create --ingress --ethertype IPv6 --protocol tcp --dst-port 22:22 octaviaopenstack security group rule create --ingress --ethertype IPv6 --protocol tcp --dst-port 9443:9443 octaviaopenstack security group rule create --ingress --ethertype IPv4 --protocol tcp --dst-port 9443:9443 octavia # security group for octavia-healthopenstack security group create octavia-health --tag charm-octavia-health --project $projectopenstack security group rule create --ingress --ethertype IPv4 --protocol icmp octavia-healthopenstack security group rule create --ingress --ethertype IPv6 --protocol icmp octavia-healthopenstack security group rule create --ingress --ethertype IPv4 --protocol udp --dst-port 5555:5555 octavia-healthopenstack security group rule create --ingress --ethertype IPv6 --protocol udp --dst-port 5555:5555 octavia-health``

   .. raw:: html

      </div>

   .. raw:: html

      </div>

7. The management network created in step
   `6 <canonical-octavia.html#mgmtnetwork>`__ is in overlay network and
   Octavia services are running in the underlay network. Verify network
   connectivity between overlay and underlay network via SDN gateway.

8. Configure Octavia with the created network.

   .. raw:: html

      <div id="jd0e206" class="sample" dir="ltr">

   .. raw:: html

      <div id="jd0e207" dir="ltr">

   ``juju run-action --wait octavia/leader configure-resources``

   .. raw:: html

      </div>

   .. raw:: html

      </div>

   Make sure the juju cluster is functional and all units have *active*
   status.

| If you want to run amphora instances on DPDK computes, you have to
  create your own flavor with the required options and set the ID to
  configuration of Octavia charm via *custom-amp-flavor-id* option
  before call configure-resources.
| Or
| Set the required options to created flavor with name *charm-octavia*
  by charm

.. raw:: html

   <div id="jd0e226" class="sample" dir="ltr">

.. raw:: html

   <div id="jd0e227" dir="ltr">

``openstack flavor set  charm-octavia  --property hw:mem_page_size=any``

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

       <div id="jd0e250" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e251" dir="ltr">

    ``openstack network create privateopenstack subnet create private --network private --subnet-range 10.10.10.0/24 --allocation-poolstart=10.10.10.50,end=10.10.10.70 --gateway none``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

2.  Create security group.

    .. raw:: html

       <div id="jd0e260" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e261" dir="ltr">

    ``openstack security group create allow_allopenstack security group rule create --ingress --protocol any --prefix '0.0.0.0/0' allow_all``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

3.  Check available flavors and images. You can create them, if needed.

    .. raw:: html

       <div id="jd0e268" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e269" dir="ltr">

    ``openstack flavor listopenstack image list``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

4.  Create two servers for load balancer.

    .. raw:: html

       <div id="jd0e276" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e277" dir="ltr">

    ``openstack server create --flavor test_flavor --image cirros --security-group allow_all --network private cirros1openstack server create --flavor test_flavor --image cirros --security-group allow_all --network private cirros2``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

5.  Create additional server to test load balancer.

    .. raw:: html

       <div id="jd0e284" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e285" dir="ltr">

    ``openstack server create --flavor test_flavor --image cirros --security-group allow_all --network private cirros-test``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

6.  Check status and IP addresses.

    .. raw:: html

       <div id="jd0e290" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e291" dir="ltr">

    ``openstack server list --long``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

7.  Create simple HTTP server on every cirros. Login on both the cirros
    instances and run following commands:

    .. raw:: html

       <div id="jd0e296" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e297" dir="ltr">

    ``MYIP=$(ifconfig eth0|grep 'inet addr'|awk -F: '{print $2}'| awk '{print $1}') while true; do echo -e "HTTP/1.0 200 OK\r\n\r\nWelcome to $MYIP" | sudo nc -l -p 80 ; done&``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

8.  Create load balancer

    .. raw:: html

       <div id="jd0e302" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e303" dir="ltr">

    ``openstack loadbalancer create --name lb1 --vip-subnet-id private``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

    Make sure *provisioning_status* is *Active*.

    .. raw:: html

       <div id="jd0e313" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e314" dir="ltr">

    ``openstack loadbalancer show lb1``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

9.  Setup load balancer

    .. raw:: html

       <div id="jd0e319" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e320" dir="ltr">

    ``openstack loadbalancer listener create --protocol HTTP --protocol-port 80 --name listener1 lb1openstack loadbalancer show lb1  # Wait for the provisioning_status to be ACTIVE.openstack loadbalancer pool create --lb-algorithm ROUND_ROBIN --listener listener1 --protocol HTTP --name pool1openstack loadbalancer healthmonitor create --delay 5 --timeout 2 --max-retries 1 --type HTTP pool1openstack loadbalancer member create --subnet-id private --address 10.10.10.50 --protocol-port 80 pool1openstack loadbalancer member create --subnet-id private --address 10.10.10.51 --protocol-port 80 pool1``

    .. raw:: html

       </div>

    IP addresses 10.10.10.50 and 10.10.10.51 belong to VMs created with
    test http server in step
    `7 <canonical-octavia.html#CreateSimpleHTTPServerOnEveryCirros>`__.

    .. raw:: html

       </div>

10. Check the status of load balancer.

    .. raw:: html

       <div id="jd0e339" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e340" dir="ltr">

    ``openstack loadbalancer show lb1  # Wait for the provisioning_status to be ACTIVE. openstack loadbalancer pool listopenstack loadbalancer pool show pool1openstack loadbalancer member list pool1openstack loadbalancer listener list``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

11. Login to load balancer client and verify if round robin works.

    .. raw:: html

       <div id="jd0e353" class="sample" dir="ltr">

    .. raw:: html

       <div id="jd0e354" dir="ltr">

    ``ubuntu@comp-1:~$ ssh cirros@169.x.0.9The authenticity of host '169.x.0.9 (169.x.0.9)' can't be established.RSA key fingerprint is SHA256:jv0qgZkorxxxxxxxmykOSVQV3fFl0.Are you sure you want to continue connecting (yes/no)? yesWarning: Permanently added '169.x.0.9' (RSA) to the list of known hosts.cirros@169.x.0.9's password:$ curl 10.10.10.50Welcome to 10.10.10.52$ curl 10.10.10.50Welcome to 10.10.10.53$ curl 10.10.10.50Welcome to 10.10.10.52$ curl 10.10.10.50Welcome to 10.10.10.53$ curl 10.10.10.50Welcome to 10.10.10.52$ curl 10.10.10.50Welcome to 10.10.10.53``

    .. raw:: html

       </div>

    .. raw:: html

       </div>

.. raw:: html

   <div id="SampleOctavia-bundle.yamlFile" class="sample" dir="ltr">

.. _Sample octavia-bundle.yaml file:

**Sample octavia-bundle.yaml file**

.. raw:: html

   <div class="output" dir="ltr">

::

   # Loadbalancer (LBAASv2) with Octavia - requires Rocky or later
   ---
   applications:
     barbican:
       charm: cs:barbican
       num_units: 1
       options:
         openstack-origin: cloud:bionic-train
       to:
       - lxd:4
     barbican-vault:
       charm: cs:barbican-vault-12
     octavia:
       series: bionic
       charm: cs:~apavlov-e/octavia
       num_units: 1
       options:
         openstack-origin: cloud:bionic-train
         create-mgmt-network: false
       to:
       - lxd:4
     octavia-dashboard:
       charm: cs:octavia-dashboard
     vault:
       charm: cs:vault
       num_units: 1
       to:
       - lxd:4
     glance-simplestreams-sync:
       charm: cs:glance-simplestreams-sync
       num_units: 1
       options:
         source: ppa:simplestreams-dev/trunk
         use_swift: false
       to:
       - lxd:4
     octavia-diskimage-retrofit:
       charm: cs:octavia-diskimage-retrofit
       options:
         amp-image-tag: 'octavia-amphora'
         retrofit-uca-pocket: train
   relations:
   - - mysql:shared-db
     - octavia:shared-db
   - - mysql:shared-db
     - barbican:shared-db
   - - mysql:shared-db
     - vault:shared-db
   - - keystone:identity-service
     - octavia:identity-service
   - - keystone:identity-service
     - barbican:identity-service
   - - rabbitmq-server:amqp
     - octavia:amqp
   - - rabbitmq-server:amqp
     - barbican:amqp
   - - neutron-api:neutron-load-balancer
     - octavia:neutron-api
   - - openstack-dashboard:dashboard-plugin
     - octavia-dashboard:dashboard
   - - barbican-vault:secrets
     - barbican:secrets
   - - vault:secrets
     - barbican-vault:secrets-storage
   - - glance-simplestreams-sync:juju-info
     - octavia-diskimage-retrofit:juju-info
   - - keystone:identity-service
     - glance-simplestreams-sync:identity-service
   - - rabbitmq-server:amqp
     - glance-simplestreams-sync:amqp
   - - keystone:identity-credentials
     - octavia-diskimage-retrofit:identity-credentials
   - - contrail-openstack
     - octavia

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

 
