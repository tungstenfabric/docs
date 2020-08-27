# Nova Docker Support

Nova docker is a docker driver for Openstack Nova used to launch docker containers instead of Virtual machines. This section describes how to set up Contrail options for nova docker support.

For more details about docker refer https://wiki.openstack.org/wiki/Docker

Nova docker support in contrail release 2.20 and greater in Ubuntu-12-04/Icehouse, Ubuntu 14-04/Icehouse and Ubuntu 14-04/Juno

## Deploying OpenStack Nova docker in contrail cluster

To deploy a compute node in contrail cluster with Nova DockerDriver instead of default LibvirtDriver, env.hypervisor dictionary needs to be populated in the testbed.py.  

### Example:
Say env.roledefs dictionary in testbed.py lists the compute nodes as below,

    env.roledefs = {
        ‘compute’ : [host5, host6, host7],
    }

And to deploy nova DockerDriver in host7 and deploy the host6 and host7 with default LibvirtDriver, env.hypervisor needs to be populated as below,

    env.hypervisor = {
        host7 : ‘docker’,
    }

With this settings in testbed.py follow the steps in [Contrail installation and Provisioning](https://github.com/Juniper/contrail-fabric-utils/wiki/contrail-Installation-and-Provisioning), to get the compute7 deployed with Nova DockerDriver.

## Saving docker images to glance
Docker images needs to be pulled and added to the glance from the compute node (host7) which is deployed with DockerDriver.

    host7$ source /etc/contrail/openstackrc
    host7$ docker pull cirros
    host7$ docker save cirros | glance image-create --is-public=True --container-format=docker --disk-format=raw --name cirros

## Launching docker containers 
Contrail will create separate nova availability zone (nova/docker) for compute nodes deployed with DockerDriver. So to launch docker container using nova command need to use –availability-zone option in nova command as below,

    host7$ source /etc/contrail/openstackrc
    host7$ nova boot --flavor 1 --nic net-id=<netId> --image <imageId> --availability-zone nova/docker <dockerContainerName>


## FAQS
1. Why the docker containers VNC console is not accessible?

   Console access is not supported in nova docker, Refer https://bugs.launchpad.net/nova-docker/+bug/1321818

2. Why am I not able to launch docker container when the image name mismatch between ‘docker images’ and ‘glance image-list’?

   Docker images needs to be saved in glance in the same name as it is listed in the ‘docker images’ command,
   because the nova docker will  get the image name from glance and will actually use it from the image saved in 
   the docker, mismatch in names will cause failure in launching docker containers.

