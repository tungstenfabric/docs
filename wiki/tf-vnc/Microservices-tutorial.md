(Credits to original author of the writeup: Nitish)

Since I have been working on creating and deploying a new Contrail Containerized Micro-Service and I couldn’t find a single all-in-one guide to do this, I have collected some information here.

Hopefully it can be of use to you and others in future.

As this information was collected from different people with different areas of expertise, I might have made a few mistakes, or left out some key information.

Please feel free to add/modify to the below or make a Wiki out of it.

Broadly, the changes needed for this Generic task are in 4 parts:
1. Service Code
2. Packaging Code
3. Containerization Code
4. Deployment Code

There are also two Important Wikis for building and testing that I have mentioned at the end.

# Service Code

The new service that I wrote is called ironic-notification-manager (INM) and is a lightweight python daemon that processes and forwards Openstack Ironic notifications and node details to Contrail Analytics.

If you are creating a new service your code will probably go into contrail-controller repo (https://github.com/Juniper/contrail-controller )

You will have to create a dir to put your service code into like this: https://github.com/Juniper/contrail-controller/tree/master/src/config/ironic-notification-manager

Please note: these are the main files that you will have to focus on for your service:

setup.py – code to setup dependent packages for your service and specify the entry-point for the service binary – it is the sdist “setup script”

SConscript – to build and install python library for your service and any Sandesh (Analytics) libraries as well. Also has code to install config and systemd service files.

requirements.txt – dependent python libraries are listed here. The python binary that gets run on package install will check if these modules/versions are available before service code runs.

MANIFEST.in – Manifest template file to package extra files with your package

<service>.sandesh – To specify the structures and objects for creating Sandesh UVEs – this is your data model file for communicating with Contrail Analytics

Please see this link for further details: https://docs.python.org/2/distutils/sourcedist.html

You can see my Service code check-ins here:

https://github.com/Juniper/contrail-controller/commit/f5e8b31f7af2ffbd2a06df350632b563d31f79a9

https://github.com/Juniper/contrail-controller/commit/ba65a06dfc8826ef006b8074d74ac481f0b9b252

https://github.com/Juniper/contrail-controller/commit/1204c78cfa7af4ebcaf1c48e47971770b7379676

# Packaging Code

The packaging code to create an RPM or DEBIAN package in in contrail-packaging repo (https://github.com/Juniper/contrail-packaging )

If you are creating an RPM, you will have to create a spec file here:

https://github.com/Juniper/contrail-packaging/tree/master/common/rpm

There are many online guides for RPM spec file creation but please pay attention to Requires section (which has to match your requirements.txt above)

In addition, you will want your new RPM/Debian to be autobuilt and available in the “CI Repo”

To do that, you will need to make a check-in to contrail-project-config repo (https://github.com/Juniper/contrail-project-config)

The packages are built with Ansible tasks like in this file:
https://github.com/Juniper/contrail-project-config/blob/master/roles/packaging-build-el/tasks/main.yaml

My Packaging code check-ins are here:

https://github.com/Juniper/contrail-packaging/commit/52130c7183a66978cdc6361359948a6b720cec60

https://github.com/Juniper/contrail-project-config/commit/a1e81d4f19686603f9811279f06e9be3513edd35

# Containerization Code

The code to create a container based on your service will go into contrail-container-builder repo (https://github.com/Juniper/contrail-container-builder )

You will probably have to define your Service parameter defaults here:

containers/base/common.sh

You will need to main files for your container:

* Dockerfile – To setup a base container to modify, install your built package and load entrypoint script and command to run in container
* entrypoint.sh – Docker entrypoint script to setup conf files before your service runs

You can see my Containerization Code check-ins here:
https://review.opencontrail.org/#/c/39473/

# Deployment Code

There are two main repos which hold the deployment code.

Both are based on Ansible (There are Kubernetes Helm charts as well but I haven’t worked with K8s or Helm):

Contrail-kolla-ansible (https://github.com/Juniper/contrail-kolla-ansible ) holds deployment code for Openstack upstream containers and openstack related containers built by us. It is a fork of upstream kolla-ansible repo and has SKU-based branches.

If your service is Openstack related, the deployment code will go here.

You will probably have to create a new role as I have done in my check-in.

Contrail-ansible-deployer (https://github.com/Juniper/contrail-ansible-deployer ) holds deployment code for Contrail containers.

You will have to specify code to deploy your container based on the role under:

* Playbooks/roles/create_containers/tasks/<role>.yml - For pulling the container
* Playbooks/roles/create_containers/templates/<role>.yaml.j2 – For deploying container

You can see my deployment code check-in here:

https://review.opencontrail.org/#/c/39700/ (to kolla-ansible) 

https://review.opencontrail.org/#/c/39607/ (sample for contrail-ansible-deployer – abandoned change)

# Testing

Please build your container using the contrail-dev-env wiki:
https://github.com/Juniper/contrail-dev-env/blob/master/README.md

This will build containers and host them in a docker registry on your build machine

Please deploy your container using the ansible-deployer wiki:
https://github.com/Juniper/contrail-ansible-deployer/wiki/Contrail-all-in-one-setup-with-Openstack-Kolla-Ocata

Please note: You will have to modify the container_hosts.yml file to point to your build machine instead of upstream/default registry

Hope this is useful.

Credits to Ignatious, Nagendra, Michael Henkel, Andrey Pavlov, Alex Levine, Jarek Lukow, Pawel Rusak and Ramprakash for their help.

Thanks,
Nitish