Setting Up the Undercloud
=========================

.. raw:: html

   <div class="section tp-summary">

Summary
-------

Follow this topic to setting up the undercloud for Contrail Networking
deployment with RHOSP 16.1.

.. raw:: html

   </div>

Install the Undercloud
----------------------

Use this example procedure to install the undercloud.

1. Log in to the undercloud VM from the undercloud KVM host.

   .. raw:: html

      <div id="jd0e26" class="example" dir="ltr">

   ::

      ssh ${undercloud_ip}

   .. raw:: html

      </div>

2. Configure the hostname.

   .. raw:: html

      <div id="jd0e32" class="example" dir="ltr">

   ::

      undercloud_name=`hostname -s` 
      undercloud_suffix=`hostname -d` 
      hostnamectl set-hostname ${undercloud_name}.${undercloud_suffix} 
      hostnamectl set-hostname --transient ${undercloud_name}.${undercloud_suffix}

   .. raw:: html

      </div>

3. Add the hostname to the ``/etc/hosts`` file. The following example
   assumes the management interface is eth0.

   .. raw:: html

      <div id="jd0e47" class="example" dir="ltr">

   ::

      undercloud_ip=`ip addr sh dev eth0 | grep "inet " | awk '{print $2}' | awk -F"/" '{print $1}'`
      echo ${undercloud_ip} ${undercloud_name}.${undercloud_suffix} ${undercloud_name} >> /etc/hosts

   .. raw:: html

      </div>

4. Set up the repositories.

   RHEL

   .. raw:: html

      <div id="jd0e55" class="example" dir="ltr">

   ::

      #Register with Satellite (can be done with CDN as well) 
      satellite_fqdn=device.example.net 
      act_key=xxx 
      org=example 
      yum localinstall -y http://${satellite_fqdn}/pub/katello-ca-consumer-latest.noarch.rpm 
      subscription-manager register --activationkey=${act_key} --org=${org}

   .. raw:: html

      </div>

5. Install the Tripleo client.

   .. raw:: html

      <div id="jd0e71" class="example" dir="ltr">

   ::

      yum install -y python-tripleoclient tmux

   .. raw:: html

      </div>

6. Copy the undercloud configuration file sample and modify the
   configuration as required. See `Red Hat
   documentation <https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/16.1/html/director_installation_and_usage/installing-the-undercloud#configuring-the-undercloud-with-environment-files>`__
   for information on how to modify that file.

   .. raw:: html

      <div id="jd0e80" class="example" dir="ltr">

   ::

      su - stack 
      cp /usr/share/python-tripleoclient/undercloud.conf.sample ~/undercloud.conf
      vi ~/undercloud.conf

   .. raw:: html

      </div>

7. Install the undercloud.

   .. raw:: html

      <div id="jd0e88" class="example" dir="ltr">

   ::

      openstack undercloud install 
      source stackrc

   .. raw:: html

      </div>

Perform Post-Install Configuration
----------------------------------

1. Configure a forwarding path between the provisioning network and the
   external network:

   .. raw:: html

      <div id="jd0e104" class="example" dir="ltr">

   ::

      sudo iptables -A FORWARD -i br-ctlplane -o eth0 -j ACCEPT 
      sudo iptables -A FORWARD -i eth0 -o br-ctlplane -m state --state RELATED,ESTABLISHED -j ACCEPT 
      sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

   .. raw:: html

      </div>

2. Add the external API interface:

   .. raw:: html

      <div id="jd0e114" class="example" dir="ltr">

   ::

      sudo ip link add name vlan720 link br-ctlplane type vlan id 720 
      sudo ip addr add 10.2.0.254/24 dev vlan720 
      sudo ip link set dev vlan720 up

   .. raw:: html

      </div>

3. Add the ``stack`` user to the docker group:

   .. raw:: html

      <div id="jd0e127" class="example" dir="ltr">

   ::

      newgrp docker 
      exit 
      su - stack 
      source stackrc

   .. raw:: html

      </div>

 
