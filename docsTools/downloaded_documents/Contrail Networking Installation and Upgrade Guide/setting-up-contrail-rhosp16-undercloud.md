# Setting Up the Undercloud

 

<div class="section tp-summary">

##### Summary

Follow this topic to setting up the undercloud for Contrail Networking
deployment with RHOSP 16.1.

</div>

## Install the Undercloud

Use this example procedure to install the undercloud.

1.  <span id="jd0e23">Log in to the undercloud VM from the undercloud
    KVM host.</span>
    <div id="jd0e26" class="example" dir="ltr">

        ssh ${undercloud_ip}

    </div>

2.  <span id="jd0e29">Configure the hostname.</span>
    <div id="jd0e32" class="example" dir="ltr">

        undercloud_name=`hostname -s` 
        undercloud_suffix=`hostname -d` 
        hostnamectl set-hostname ${undercloud_name}.${undercloud_suffix} 
        hostnamectl set-hostname --transient ${undercloud_name}.${undercloud_suffix}

    </div>

3.  <span id="jd0e41">Add the hostname to the `/etc/hosts` file. The
    following example assumes the management interface is eth0.</span>
    <div id="jd0e47" class="example" dir="ltr">

        undercloud_ip=`ip addr sh dev eth0 | grep "inet " | awk '{print $2}' | awk -F"/" '{print $1}'`
        echo ${undercloud_ip} ${undercloud_name}.${undercloud_suffix} ${undercloud_name} >> /etc/hosts

    </div>

4.  <span id="jd0e50">Set up the repositories.</span>

    RHEL

    <div id="jd0e55" class="example" dir="ltr">

        #Register with Satellite (can be done with CDN as well) 
        satellite_fqdn=device.example.net 
        act_key=xxx 
        org=example 
        yum localinstall -y http://${satellite_fqdn}/pub/katello-ca-consumer-latest.noarch.rpm 
        subscription-manager register --activationkey=${act_key} --org=${org}

    </div>

5.  <span id="jd0e68">Install the Tripleo client.</span>
    <div id="jd0e71" class="example" dir="ltr">

        yum install -y python-tripleoclient tmux

    </div>

6.  <span id="jd0e74">Copy the undercloud configuration file sample and
    modify the configuration as required. See [Red Hat
    documentation](https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/16.1/html/director_installation_and_usage/installing-the-undercloud#configuring-the-undercloud-with-environment-files)
    for information on how to modify that file.</span>
    <div id="jd0e80" class="example" dir="ltr">

        su - stack 
        cp /usr/share/python-tripleoclient/undercloud.conf.sample ~/undercloud.conf
        vi ~/undercloud.conf

    </div>

7.  <span id="jd0e85">Install the undercloud.</span>
    <div id="jd0e88" class="example" dir="ltr">

        openstack undercloud install 
        source stackrc

    </div>

## Perform Post-Install Configuration

1.  <span id="jd0e101">Configure a forwarding path between the
    provisioning network and the external network:</span>
    <div id="jd0e104" class="example" dir="ltr">

        sudo iptables -A FORWARD -i br-ctlplane -o eth0 -j ACCEPT 
        sudo iptables -A FORWARD -i eth0 -o br-ctlplane -m state --state RELATED,ESTABLISHED -j ACCEPT 
        sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

    </div>
2.  <span id="jd0e111">Add the external API interface:</span>
    <div id="jd0e114" class="example" dir="ltr">

        sudo ip link add name vlan720 link br-ctlplane type vlan id 720 
        sudo ip addr add 10.2.0.254/24 dev vlan720 
        sudo ip link set dev vlan720 up

    </div>
3.  <span id="jd0e121">Add the `stack` user to the docker group:</span>
    <div id="jd0e127" class="example" dir="ltr">

        newgrp docker 
        exit 
        su - stack 
        source stackrc

    </div>

 
