## 1. Install Docker

Install Docker on the base host. Installation steps for CentOS and Ubuntu are given below:

### CentOS

```
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum install -y docker-ce-18.03.1.ce
systemctl start docker
```
**Reference:** https://docs.docker.com/install/linux/docker-ce/centos/

### Ubuntu

```
apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
apt-add-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-get install docker-ce=18.03.1~ce-0~ubuntu
```
**Reference:** https://docs.docker.com/install/linux/docker-ce/ubuntu/

## 2. Pull and Start Contrail-Kolla-Ansible-Deployer Container

Nightly builds for container can be accessed from [Docker Hub](https://hub.docker.com/r/opencontrailnightly/contrail-kolla-ansible-deployer/tags)

**Set Container Details**

```
export CAD_IMAGE=opencontrailnightly/contrail-kolla-ansible-deployer:master-<BUILD_NO>
```

**Start Docker Container**
```
docker run -td --net host --name contrail_kolla_ansible_deployer $CAD_IMAGE
```

## 3. Copy Configuration files to Container

[instances.yaml](https://github.com/Juniper/contrail-ansible-deployer/wiki/Contrail-with-Openstack-Kolla#13-configure-necessary-parameters-configinstancesyaml-under-appropriate-parameters): Template file for configuring contrail cluster. Read [here](https://github.com/Juniper/contrail-ansible-deployer/blob/master/README.md#configuration) to get more information on how to configure all available parameters in that file.

Modify this configuration file according to your setup and copy this file to the deployer container.

```
export INSTANCES_FILE=<ABSOLUTE_PATH_OF_INSTANCES_YML_FILE>
docker cp $INSTANCES_FILE contrail_kolla_ansible_deployer:/root/contrail-ansible-deployer/config/instances.yaml
```

## 4. Run the Container

```
docker exec -it contrail_kolla_ansible_deployer bash
cd /root/contrail-ansible-deployer
```

Once you are inside the container, run the following commands to deploy OpenStack cluster with Contrail.

1. Configure deployment nodes
```
ansible-playbook -i inventory/ -e orchestrator=openstack playbooks/configure_instances.yml
```

2. Install OpenStack
```
ansible-playbook -i inventory/ -e orchestrator=openstack playbooks/install_openstack.yml
```

3. Install Contrail
```
ansible-playbook -i inventory/ -e orchestrator=openstack playbooks/install_contrail.yml

```
