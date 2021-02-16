Setting Up the Undercloud
=========================

:date: 2020-07-07

Install the Undercloud
----------------------

Use this example procedure to install the undercloud.

1. Log in to the undercloud VM from the undercloud KVM host.
   
   ::

      ssh ${undercloud_ip}

2. Configure the hostname.
   
   ::

      undercloud_name=`hostname -s` 
      undercloud_suffix=`hostname -d` 
      hostnamectl set-hostname ${undercloud_name}.${undercloud_suffix} 
      hostnamectl set-hostname --transient ${undercloud_name}.${undercloud_suffix}

3. Add the hostname to the ``/etc/hosts`` file. The following example
   assumes the management interface is eth0.
   
   ::

      undercloud_ip=`ip addr sh dev eth0 | grep "inet " | awk '{print $2}' | awk -F"/" '{print $1}'`
      echo ${undercloud_ip} ${undercloud_name}.${undercloud_suffix} ${undercloud_name} >> /etc/hosts
      
4. Set up the repositories.

   -  CentOS
      
      ::

         tripleo_repos=`python -c 'import requests;r = requests.get("https://trunk.rdoproject.org/centos7-queens/current"); print r.text ' | grep python2-tripleo-repos|awk -F"href=\"" '{print $2}' | awk -F"\"" '{print $1}'` 
         yum install -y https://trunk.rdoproject.org/centos7-queens/current/${tripleo_repos} 
         tripleo-repos -b queens current

   -  RHEL
      
      ::

         #Register with Satellite (can be done with CDN as well) 
         satellite_fqdn=device.example.net 
         act_key=xxx 
         org=example 
         yum localinstall -y http://${satellite_fqdn}/pub/katello-ca-consumer-latest.noarch.rpm 
         subscription-manager register --activationkey=${act_key} --org=${org}

5. Install the Tripleo client.
   
   ::

      yum install -y python-tripleoclient tmux

6. Copy the undercloud configuration file sample and modify the
   configuration as required. See `Red Hat
   documentation <https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/13/html-single/director_installation_and_usage/>`__
   for information on how to modify that file.
   
   ::

      su - stack 
      cp /usr/share/instack-undercloud/undercloud.conf.sample ~/undercloud.conf
      vi ~/undercloud.conf

7. Install the undercloud.
   
   ::

      openstack undercloud install 
      source stackrc

Perform Post-Install Configuration
----------------------------------

1. Configure a forwarding path between the provisioning network and the
   external network:
   
   ::

      sudo iptables -A FORWARD -i br-ctlplane -o eth0 -j ACCEPT 
      sudo iptables -A FORWARD -i eth0 -o br-ctlplane -m state --state RELATED,ESTABLISHED -j ACCEPT 
      sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

2. Add the external API interface:

   ::

      sudo ip link add name vlan720 link br-ctlplane type vlan id 720 
      sudo ip addr add 10.2.0.254/24 dev vlan720 
      sudo ip link set dev vlan720 up

3. Add the ``stack`` user to the docker group:

   ::

      newgrp docker 
      exit 
      su - stack 
      source stackrc