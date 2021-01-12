# Setting Up the Undercloud

 

## Install the Undercloud

Use this example procedure to install the undercloud.

1.  <span id="jd0e20">Log in to the undercloud VM from the undercloud
    KVM host.</span>
    <div id="jd0e23" class="example" dir="ltr">

        ssh ${undercloud_ip}

    </div>
2.  <span id="jd0e26">Configure the hostname.</span>
    <div id="jd0e29" class="example" dir="ltr">

        undercloud_name=`hostname -s` 
        undercloud_suffix=`hostname -d` 
        hostnamectl set-hostname ${undercloud_name}.${undercloud_suffix} 
        hostnamectl set-hostname --transient ${undercloud_name}.${undercloud_suffix}

    </div>
3.  <span id="jd0e38">Add the hostname to the `/etc/hosts` file. The
    following example assumes the management interface is eth0.</span>
    <div id="jd0e44" class="example" dir="ltr">

        undercloud_ip=`ip addr sh dev eth0 | grep "inet " | awk '{print $2}' | awk -F"/" '{print $1}'`
        echo ${undercloud_ip} ${undercloud_name}.${undercloud_suffix} ${undercloud_name} >> /etc/hosts

    </div>
4.  <span id="jd0e47">Set up the repositories.</span>
    -   CentOS

        <div id="jd0e54" class="example" dir="ltr">

            tripleo_repos=`python -c 'import requests;r = requests.get("https://trunk.rdoproject.org/centos7-queens/current"); print r.text ' | grep python2-tripleo-repos|awk -F"href=\"" '{print $2}' | awk -F"\"" '{print $1}'` 
            yum install -y https://trunk.rdoproject.org/centos7-queens/current/${tripleo_repos} 
            tripleo-repos -b queens current

        </div>

    -   RHEL

        <div id="jd0e60" class="example" dir="ltr">

            #Register with Satellite (can be done with CDN as well) 
            satellite_fqdn=device.example.net 
            act_key=xxx 
            org=example 
            yum localinstall -y http://${satellite_fqdn}/pub/katello-ca-consumer-latest.noarch.rpm 
            subscription-manager register --activationkey=${act_key} --org=${org}

        </div>
5.  <span id="jd0e73">Install the Tripleo client.</span>
    <div id="jd0e76" class="example" dir="ltr">

        yum install -y python-tripleoclient tmux

    </div>
6.  <span id="jd0e79">Copy the undercloud configuration file sample and
    modify the configuration as required. See [Red Hat
    documentation](https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/13/html-single/director_installation_and_usage/)
    for information on how to modify that file.</span>
    <div id="jd0e85" class="example" dir="ltr">

        su - stack 
        cp /usr/share/instack-undercloud/undercloud.conf.sample ~/undercloud.conf
        vi ~/undercloud.conf

    </div>
7.  <span id="jd0e90">Install the undercloud.</span>
    <div id="jd0e93" class="example" dir="ltr">

        openstack undercloud install 
        source stackrc

    </div>

## Perform Post-Install Configuration

1.  <span id="jd0e106">Configure a forwarding path between the
    provisioning network and the external network:</span>
    <div id="jd0e109" class="example" dir="ltr">

        sudo iptables -A FORWARD -i br-ctlplane -o eth0 -j ACCEPT 
        sudo iptables -A FORWARD -i eth0 -o br-ctlplane -m state --state RELATED,ESTABLISHED -j ACCEPT 
        sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

    </div>
2.  <span id="jd0e116">Add the external API interface:</span>
    <div id="jd0e119" class="example" dir="ltr">

        sudo ip link add name vlan720 link br-ctlplane type vlan id 720 
        sudo ip addr add 10.2.0.254/24 dev vlan720 
        sudo ip link set dev vlan720 up

    </div>
3.  <span id="jd0e126">Add the `stack` user to the docker group:</span>
    <div id="jd0e132" class="example" dir="ltr">

        newgrp docker 
        exit 
        su - stack 
        source stackrc

    </div>

 
