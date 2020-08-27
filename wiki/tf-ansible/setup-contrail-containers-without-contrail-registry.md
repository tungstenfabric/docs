* Refer [Quickstart guide](https://github.com/Juniper/contrail-ansible/wiki/Quickstart-Guide-with-ini-file-based-inventory) for basic setup
* Edit inventory and remove/comment out variables "docker_registry" and "docker_registry_insecure"
* Copy container tar.gz files under playbooks/container_images/ directory
```
$ ls contrail-ansible/playbooks/container_images/
contrail-agent-u14.04-4.0.0.0-3042.tar.gz        contrail-analytics-u14.04-4.0.0.0-3042.tar.gz   contrail-kube-manager-u14.04-4.0.0.0-3042.tar.gz  contrail-vrouter-compiler-c7.1-4.0.0.0-3042.tar.gz
contrail-analyticsdb-u14.04-4.0.0.0-3042.tar.gz  contrail-controller-u14.04-4.0.0.0-3042.tar.gz  contrail-repo-c7.1-4.0.0.0-3042.tar.gz

```
* Run ansible-playbook

```
$ ansible-playbook -i <inventory file path>  site.yml 

$ ansible-playbook -i single-controller-centos-inventory  site.yml 
```

* Sample inventory file shown below (without any commented lines)

```
[contrail-controllers]
192.168.0.24

[contrail-analyticsdb]
192.168.0.24

[contrail-analytics]
192.168.0.24

[contrail-kubernetes]
192.168.0.24

[contrail-compute]
192.168.0.25
192.168.0.26

[all:vars]
docker_install_method=package
ansible_user=root
ansible_connection=ssh
ansible_become=true
os_release = u14.04
controller_ip=192.168.0.24
contrail_version=4.0.0.0-3011
cloud_orchestrator=kubernetes
vrouter_physical_interface=eth0
```