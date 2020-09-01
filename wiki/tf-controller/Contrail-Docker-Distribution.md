# Contrail Docker Distributions

This Document explains about the distribution TGZ structure and the explains about its contents.  
Using an example release as 4.0.0.0 and Version as 3045.


#### Contrail Networking Roles:
Contrail Roles that are distributed as a part of Contrail Networking Distribution 

1) Vrouter
* contrail-vrouter-3.13.0-106-generic  (Based on Recommended Kernel version)  
* linux-image-4.4.0-34-generic (extra kernel for kernel upgrade support)
* contrail-vrouter-dkms  
* contrail-vrouter-dpdk  
* contrail-vrouter-dpdk-init  
* contrail-openstack-vrouter  

2) Contrail Neutron plugin
* neutron-plugin-contrail  

3) Misc packages
* Kernel Upgrade
* Docker/Ansible 
* Haproxy

#### Contrail Cloud Roles:
Contrail Cloud Roles included as a part of Contrail Cloud Distribution.
It includes all roles of Contrail Networking Roles as a part of contrail-networking-docker.tgz and along with below-listed roles

1) Openstack role   
2) Openstack HA role
3) Optional Packages - Ceilometer


## Networking Distribution Structure:
#### contrail-networking-docker_4.0.0.0-3045.tgz 

```
contrail-networking-docker_4.0.0.0-3045.tgz  (1)
    |---- contrail-docker-images_4.0.0.0-3045.tgz (2)
    |     |---- contrail-controller-u14.04-4.0.0.0-3045.tar.gz  
    |     |---- contrail-analytics-u14.04-4.0.0.0-3045.tar.gz
    |     |---- contrail-agent-u14.04-4.0.0.0-3045.tar.gz
    |     |---- contrail-lb-u14.04-4.0.0.0-3045.tar.gz
    |     |---- contrail-analyticsdb-u14.04-4.0.0.0-3045.tar.gz  
    |---- contrail-networking-tools_4.0.0.0-3045.tgz (3)
    |     |---- contrail-docker-tools-4.0.0.0-3045.tar.gz  (4)
    |     |---- contrail-ansible-4.0.0.0-6.tar.gz (5)
    |---- contrail-vrouter-packages_4.0.0.0-3045.tgz  (6)
    |     |---- contrail-vrouter-agent_4.0.0.0-3045_amd64.deb
    |     |---- contrail-vrouter-dkms_4.0.0.0-3045_amd64.deb
    |     |---- contrail-vrouter-dpdk_4.0.0.0-3045_all.deb
    |     |---- contrail-vrouter-source_4.0.0.0-3045_amd64.deb
    |     |---- contrail-vrouter-utils_4.0.0.0-3045_amd64.deb
    |     |---- python-contrail_4.0.0.0-3045_amd64.deb
    |     |---- python-contrail-vrouter-api_4.0.0.0-3045_amd64.deb
    |     |---- contrail-vrouter-3.13.0-106-generic_4.0.0.0-3045_all.deb
    |     |---- python-opencontrail-vrouter-netns_4.0.0.0-3045_amd64.deb
    |     |---- contrail-utils_4.0.0.0-3045_amd64.deb
    |     |---- contrail-lib_4.0.0.0-3045_amd64.deb
    |     |---- contrail-nova-vif_4.0.0.0-3045_all.deb
    |     |---- contrail-openstack-vrouter_4.0.0.0-3045_all.deb
    |     |---- contrail-setup_4.0.0.0-3045_all.deb
    |     |---- contrail-vrouter-common_4.0.0.0-3045_all.deb
    |     |---- contrail-vrouter-init_4.0.0.0-3045_all.deb
    |     |---- ...
    |---- contrail-networking-openstack-extra_4.0.0.0-3045.tgz (7)
    |     |---- openstack-extra-common_4.0.0.0-3045.tgz (8)
    |     |     |---- python-urllib3_1.13.1-2~cloud0_all.deb
    |     |     |---- libvirt-bin_1.3.1-1ubuntu10.1~cloud0+contrail1_amd64.deb
    |     |     |---- python-amqp_1.4.9-1~cloud0_all.deb
    |     |     |---- qemu-system-misc_2.5+dfsg-5ubuntu10.2~cloud0+contrail1_amd64.deb
    |     |     |---- ...
    |     |---- openstack-extra-<SKU>_4.0.0.0-3045.tgz (9)
    |     |     |---- contrail-openstack-dashboard_4.0.0.0-1_all.deb  
    |     |     |---- python-nova_2015.1.2-0ubuntu2~cloud0.1contrail1_all.deb 
    |     |     |---- nova-docker_0.0.0.post196-0contrail0_all.deb  
    |     |     |---- ...
    |---- contrail-neutron-plugin-packages_4.0.0.0-3045.tgz (10)
    |     |---- neutron-plugin-contrail_4.0.0.0-3045_all.deb
    |     |---- python-contrail_4.0.0.0-3048_amd64.deb
    |     |---- ...
    |---- contrail-networking-thirdparty_4.0.0.0-3045.tgz (11)
    |     |---- docker-engine_1.13.0-0~ubuntu-trusty_amd64.deb
    |     |---- ansible_2.2.0.0-1ppa~trusty_all.deb
    |     |---- ...  
    |---- contrail-networking-dependents_4.0.0.0-3045.tgz (12)
    |     |---- git-man_1%3a1.9.1-1ubuntu0.3_all.deb
    |     |---- libogg0_1.3.1-1ubuntu1_amd64.deb
    |     |---- ...  

```

## Cloud Distribution Structure:
#### contrail-cloud-docker_4.0.0.0-3045-mitaka.tgz (13)

```
contrail-cloud-docker_4.0.0.0-3045-mitaka.tgz
    |---- contrail-cloud-tools-4.0.0.0-3048-mitaka.tar.gz (14)
    |     |---- contrail-puppet-4.0.0.0-3048-mitaka.tar.gz (15)
    |---- contrail-networking-docker_4.0.0.0-3045.tgz (1)
    |---- contrail-cloud-thirdparty_4.0.0.0-3045.tgz (16)
    |     |---- docker-engine_1.13.0-0~ubuntu-trusty_amd64.deb
    |     |---- ansible_2.2.0.0-1ppa~trusty_all.deb
    |     |---- ...
    |---- contrail-openstack-packages_4.0.0.0-3045-mitaka.tgz (17)
    |     |---- python-neutron_2%3a8.3.0-0ubuntu1.1~cloud0_all.deb
    |     |---- python-nova_13.0.0-0ubuntu2~cloud0.1contrail1_all.deb
    |     |---- nova-api_13.0.0-0ubuntu2~cloud0.1contrail1_all.deb
    |     |---- ...
    |---- contrail-cloud-dependents_4.0.0.0-3045.tgz (18)
    |     |---- git-man_1%3a1.9.1-1ubuntu0.3_all.deb
    |     |---- libogg0_1.3.1-1ubuntu1_amd64.deb
    |     |---- ...  

```


## Kubernetes Distribution Structure:
#### contrail-kubernetes-docker_4.0.0.0-3045.tgz  
```
contrail-kubernetes-docker_4.0.0.0-3045.tgz (19)
    |---- contrail-kubernetes-docker-images_4.0.0.0-3045.tgz   (20)
    |     |---- contrail-kube-manager-ubuntu16.04-4.0.0.0-6.tar.gz 
    |     |---- contrail-controller-ubuntu16.04-4.0.0.0-3045.tar.gz
    |     |---- contrail-analytics-ubuntu16.04-4.0.0.0-3045.tar.gz
    |     |---- contrail-agent-ubuntu16.04-4.0.0.0-3045.tar.gz
    |     |---- contrail-lb-ubuntu14.06-4.0.0.0-3045.tar.gz
    |     |---- contrail-analyticsdb-ubuntu16.04-4.0.0.0-3045.tar.gz  
    |---- contrail-networking-tools_4.0.0.0-3045.tgz
    |     |---- contrail-docker-tools-4.0.0.0-3045.tar.gz
    |     |---- contrail-ansible-4.0.0.0-6.tar.gz
    |---- contrail-vrouter-packages_4.0.0.0-3045.tgz
    |     |---- contrail-vrouter-agent_4.0.0.0-3045_amd64.deb
    |     |---- contrail-vrouter-dkms_4.0.0.0-3045_amd64.deb
    |     |---- contrail-vrouter-dpdk_4.0.0.0-3045_all.deb
    |     |---- contrail-vrouter-source_4.0.0.0-3045_amd64.deb
    |     |---- contrail-vrouter-utils_4.0.0.0-3045_amd64.deb
    |     |---- python-contrail_4.0.0.0-3045_amd64.deb
    |     |---- python-contrail-vrouter-api_4.0.0.0-3045_amd64.deb
    |     |---- contrail-vrouter-3.13.0-106-generic_4.0.0.0-3045_all.deb
    |     |---- python-opencontrail-vrouter-netns_4.0.0.0-3045_amd64.deb
    |     |---- contrail-utils_4.0.0.0-3045_amd64.deb
    |     |---- contrail-lib_4.0.0.0-3045_amd64.deb
    |     |---- contrail-nova-vif_4.0.0.0-3045_all.deb
    |     |---- contrail-openstack-vrouter_4.0.0.0-3045_all.deb
    |     |---- contrail-setup_4.0.0.0-3045_all.deb
    |     |---- contrail-vrouter-common_4.0.0.0-3045_all.deb
    |     |---- contrail-vrouter-init_4.0.0.0-3045_all.deb
    |     |---- ...
    |----- contrail-kubernetes-packages_4.0.0.0-12.tgz  (21)
    |     |---- contrail-kube-manager_4.0.0.0-12_amd64.deb
    |     |---- contrail-k8s-cni_4.0.0.0-12_amd64.deb
    |     |---- python-contrail_4.0.0.0-12_amd64.deb  
    |---- contrail-networking-thirdparty_4.0.0.0-3045.tgz
    |     |---- docker-engine_1.13.0-0~ubuntu-trusty_amd64.deb
    |     |---- ansible_2.2.0.0-1ppa~trusty_all.deb
    |     |---- ...  
    |---- contrail-kubernetes-dependents_4.0.0.0-3045.tgz (22)
    |     |---- git-man_1%3a1.9.1-1ubuntu0.3_all.deb
    |     |---- libogg0_1.3.1-1ubuntu1_amd64.deb
    |     |---- ...  

```

#### 1) contrail-networking-docker_4.0.0.0-3045.tgz:  
Wrapper TGZ Containing below tgzs  
* contrail-vrouter-packages_4.0.0.0-3045.tgz
* contrail-neutron-plugin-packages_4.0.0.0-3045.tgz
* contrail-docker-images_4.0.0.0-3045.tgz
* contrail-networking-dependencies_4.0.0.0-3045.tgz
* contrail-networking-thirdparty_4.0.0.0-3045.tgz
* contrail-networking-openstack-extra_4.0.0.0-3045.tgz

#### 2) contrail-docker-images_4.0.0.0-3045.tgz   
Contains below docker images for each contrail role    
* contrail-controller-ubuntu14.04-4.0.0.0-3045.tar.gz  
* contrail-analytics-ubuntu14.04-4.0.0.0-3045.tar.gz  
* contrail-agent-ubuntu14.04-4.0.0.0-3045.tar.gz   
* contrail-lb-ubuntu14.04-4.0.0.0-3045.tar.gz  
* contrail-analyticsdb-ubuntu14.04-4.0.0.0-3045.tar.gz  

#### 3) contrail-networking-tools_4.0.0.0-3045.tgz  
Contrail tools used to provision docker, vrouter etc and utility scripts for logs, status, upgrade
Contains  
* contrail-ansible-4.0.0.0-3045.tar.gz  
* contrail-docker-tools_4.0.0.0-6_all.deb  

#### 4) contrail-docker-tools_4.0.0.0-6_all.deb
Contains utility scripts for logs, status, upgrade scripts.  

#### 5) contrail-ansible-4.0.0.0-3045.tar.gz  
Contains ansible playbooks and related code to provision docker containers  

#### 6) contrail-vrouter-packages_4.0.0.0-3045.tgz  
Contains contrail packages required to install below provided list of packages  
* contrail-vrouter-3.13.0-106-generic  (Based on Recommended Kernel version)  
* linux-image-4.4.0-34-generic (extra kernel for kernel upgrade support)
* contrail-vrouter-dkms  
* contrail-vrouter-dpdk  
* contrail-vrouter-dpdk-init  
* contrail-openstack-vrouter  

#### 7) contrail-networking-openstack-extra_4.0.0.0-3045.tgz
Contains dependent packages from Openstack Repo which are required to install contrail vrouter role, contrail network plugin etc of all SKUs (eg mitaka, liberty...) in multiple TGZ files.  
* openstack-extra-common_4.0.0.0-3045.tgz 
* openstack-extra-<SKU>_4.0.0.0-3045.tgz

#### 8) openstack-extra-common_4.0.0.0-3045.tgz  
Dependent packages from Openstack Repo (not SKU specific) which are required to installing contrail vrouter, neutron-plugin etc

#### 9) openstack-extra-<SKU>_4.0.0.0-3045.tgz
Dependent packages from corresponding Openstack SKU Repo ie newton, mitaka, kilo etc which are required for installing contrail vrouter, neutron-plugin etc 

#### 10) contrail-neutron-plugin-packages_4.0.0.0-3045.tgz
Contains contrail packages required to install contrail neutron plugin role

#### 11) contrail-networking-thirdparty_4.0.0.0-3045.tgz  
Thirparty packages required to install [Contrail Networking Roles](https://github.com/Juniper/contrail-controller/wiki/Contrail-Docker-Distribution#contrail-networking-roles)

#### 12) contrail-networking-dependents_4.0.0.0-3045.tgz
Dependent packages from Ubuntu upstream repos (trusty, trusty-updates, trusty-security or corresponding to give CODENAME) required for installing [Contrail Networking Roles](https://github.com/Juniper/contrail-controller/wiki/Contrail-Docker-Distribution#contrail-networking-roles)

#### 13) contrail-cloud-docker_4.0.0.0-3045-mitaka.tgz  
Wrapper TGZ containing  
contrail-networking-docker_4.0.0.0-12.tgz
contrail-openstack-packages_4.0.0.0-12-mitaka.tgz
contrail-storage-packages_4.0.0.0-12.tgz
contrail-cloud-tools_4.0.0.0-12-mitaka.tgz
contrail-cloud-thirdparty_4.0.0.0-12.tgz
contrail-cloud-docker-images_4.0.0.0-12.tgz
contrail-cloud-dependents_4.0.0.0-12.tgz
This TGZ is tagged with SKU name to represent it's a Mitaka distribution  

#### 14) contrail-cloud-tools-4.0.0.0-3048-mitaka.tar.gz 
Contrail tools required to provision Docker, Vrouter, Openstack role etc...  
Contains  
contrail-puppet-4.0.0.0-3048-mitaka.tar.gz  

#### 15) contrail-puppet-4.0.0.0-3048-mitaka.tar.gz  
Puppet Code used by SM to provision Openstack Role  
This TGZ is tagged with SKU name as it contains code for relevant SKU. In this case, it contains puppet code required to bring Openstack Mitaka

#### 16) contrail-cloud-thirdparty_4.0.0.0-3045.tgz  
Thirparty packages required to install [Contrail Cloud Roles](https://github.com/Juniper/contrail-controller/wiki/Contrail-Docker-Distribution#contrail-cloud-roles)

#### 17) contrail-openstack-packages_4.0.0.0-3045-mitaka.tgz  
Packages from Openstack repo needed to install Openstack role  
This TGZ is tagged with SKU name as it contains packages from relevant SKU. In this case, it contains packages from Openstack Mitaka repo  

#### 18) contrail-cloud-dependents_4.0.0.0-3045.tgz  
Dependent packages from Ubuntu upstream repos (trusty, trusty-updates, trusty-security) required for installing [Contrail Cloud Roles](https://github.com/Juniper/contrail-controller/wiki/Contrail-Docker-Distribution#contrail-cloud-roles)

#### 19) contrail-kubernetes-docker_4.0.0.0-3045.tgz  
Wrapper TGZ containing
contrail-kubernetes-dependents_4.0.0.0-12.tgz
contrail-kubernetes-packages_4.0.0.0-12.tgz
contrail-networking-thirdparty_4.0.0.0-12.tgz
contrail-vrouter-packages_4.0.0.0-12.tgz
contrail-kubernetes-docker-images_4.0.0.0-12.tgz
contrail-networking-tools_4.0.0.0-12.tgz  

#### 20) contrail-kubernetes-docker-images_4.0.0.0-3045.tgz  
Docker images supplied in Kubernetes distribution
* contrail-analytics-ubuntu16.04-4.0.0.0-12.tar.gz
* contrail-lb-ubuntu16.04-4.0.0.0-12.tar.gz
* contrail-controller-ubuntu16.04-4.0.0.0-12.tar.gz
* contrail-kube-manager-ubuntu16.04-4.0.0.0-12.tar.gz
* contrail-agent-ubuntu16.04-4.0.0.0-12.tar.gz
* contrail-analyticsdb-ubuntu16.04-4.0.0.0-12.tar.gz

#### 21) contrail-kubernetes-packages_4.0.0.0-12.tgz  
Contrail packages required to install Kube manager and CNI

#### 22) contrail-kubernetes-dependents_4.0.0.0-3045.tgz  
Dependent packages from Ubuntu upstream repos (trusty, trusty-updates, trusty-security or corresponding to give CODENAME) required for installing [Contrail Networking Roles](https://github.com/Juniper/contrail-controller/wiki/Contrail-Docker-Distribution#contrail-networking-roles) and [Contrail Kubernetes packages](https://github.com/Juniper/contrail-controller/wiki/Contrail-Docker-Distribution#21-contrail-kubernetes-packages_4000-12tgz)