### Directory based vs ini file based inventory
inifile based inventory is easy to setup as you just have to handle one file. But this may get complicated when you have more parameters. It is recommended to use directory based inventory in those situations.

* Directory based inventory split the host list (added in hosts file), group_vars (variables for group) and possibly host_vars (variables for specific hosts) where in ini based file all of them are in a single file.
* Variables in directory based inventory are mentioned in yaml format which is more readable especially with complex variable structures like dictionaries

Please follow [Quickstart guide with ini file based inventory](https://github.com/Juniper/contrail-ansible/wiki/Quickstart-Guide-with-ini-file-based-inventory)

#### Step 0: Ensure Compute node has kernel header package available for running kernel(uname -r)
contrail-vrouter need kernel headers to get it compiled, so you have to make sure that compute node has yum/apt sources configured and kernel headers packages available to be installed for running kernel.

I noticed that in some situations, any of the repo sources configured in the compute node has any reference to the kernel headers package for running kernel because of the image being old, in which case you will have to install any available kernel and kernel headers that are available to make sure both of them match and reboot the node to make new kernel running. Note that this need to be run before you run ansible as this is not handled in contrail-ansible code.

* In redhat/centos systems

```
$ yum info kernel-headers | grep "Version\|Release"
Version     : 3.10.0
Release     : 514.10.2.el7

$ uname -r
3.10.0-327.el7.x86_64
```
Result of yum info should match kernel version that is running (uname -r). In above case it is not, so you would have to install both kernel, kernel-headers, and kernel-devel of same version and reboot the node to make sure new kernel version is running (confirm it with uname -r)

* In ubuntu systems

```
$ apt-get update
$ apt-cache search linux-headers | grep $(uname -r)
linux-headers-4.4.0-57-generic - Linux kernel headers for version 4.4.0 on 64 bit x86 SMP

```

In case above command fail - i.e linux headers are not available for running kernel, you will have to install the kernel and linux-headers packages with same version and reboot the node to make sure new kernel version is running (confirm with uname -r).

#### Step 1: Setup passwordless access to all hosts from ansible host
```
ssh-keygen -t rsa
ssh <user>@<host-ip> mkdir -p .ssh
ssh <user>@<host-ip> chmod 700 .ssh
cat .ssh/id_rsa.pub | ssh <user>@<host-ip> 'cat >> .ssh/authorized_keys'
Ensure ssh <user>@<host-ip> works fine.
```

#### Step 2: Install ansible on your OSX (mac) or any other machine. Version must be = 2.2.0. We only support released versions of ansible.
```
sudo easy_install pip
sudo pip install ansible==2.2.0
```

#### Step 3: Get code
```
git clone https://github.com/Juniper/contrail-ansible.git
```

#### step 4: Findout the contrail container versions available within the docker registry
Below example shows a registry on 10.84.34.155:5000 - your registry may be different

URL to see all containers available within the docker registry
http://10.84.5.71:5000/v2/_catalog

URL to see versions available for contrail-controller-u14.04 container in the registry
http://10.84.5.71:5000/v2/contrail-controller-ubuntu14.04/tags/list

#### Step 5: Update inventory file (my-inventory)


<b>Sample inventory has a file README.md which need to be removed before you run ansible.</b>

* Update all IP addresses in the file my-inventory
```
cd playbooks
vi inventory/my-inventory/hosts
```

* Set the contrail-repo to controller node ip in inventory/my-inventory/hosts ONLY when cloud_orchestrator = mesos
```
[contrail-repo]
192.168.0.72 
```

* Update inventory/my-inventory/group_vars/all.yml 
```
ansible_user: root  # The user name to connect to those nodes
contrail_version: 4.0.0.0-3013
vrouter_physical_interface: eth0 or interface name hosting the compute ip address
```
* Update contrail_compute_mode if you want to setup contrail-agent as containers

* Update docker_py_pkg_install_method to pip
```
docker_py_pkg_install_method: pip
``` 
* OPTIONAL - only required if you want to use ubuntu 16.04 containers for kube-manager, mesos-manager
  * Uncomment and Update inventory/my-inventory/group_vars/all.yml with following variables
    ```
      # custom image for kube-manager - image with ubuntu 16.04 and systemd
      # contrail_kube_manager_image: "10.84.34.155:5000/contrail-kube-manager-u14.04:4.0.0.0-3016"

      # custom image for mesos-manager - image with ubuntu 16.04 and systemd
      # contrail_mesos_manager_image: "10.84.34.155:5000/contrail-mesos-manager-u14.04:4.0.0.0-3016"

    ```
* OPTIONAL - Update os_release - in case you want to start containers based out of specific operating system - by default it is u14.04

```
 # os_release - operating system release - ubuntu 14.04 - u14.04, ubuntu 16.04 - u16.04, centos 7.1 - c7.1, centos 7.2 - c7.2
 os_release: u14.04
```
#### Step 6: Change webui port [Optional - used for Kubernetes]
* Update inventory/my-inventory/group_vars/all.yml

```
webui_config:
  http_listen_port: 8085
```

#### Step 7: Run ansible
```
cd playbooks
ansible-playbook -i inventory/my-inventory site.yml
```