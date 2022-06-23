.. _Understanding TF Containers:

Understanding TF Containers
===========================

:date: 2019-05-23

Some subsystems of Tungsten Fabric solution are delivered as Docker
containers.

TF Containers
-------------

The following are key features of the new architecture of TF
containers:

-  All of the TF containers are multiprocess Docker containers.

-  Each container has an INI-based configuration file that has the
   configurations for all of the applications running in that container.

-  Each container is self-contained, with minimal external orchestration
   needs.

-  A single tool, *Ansible*, is used for all levels of building,
   deploying, and provisioning the containers. The *Ansible* code for
   the TF system is named ``tf-ansible`` and kept in a
   separate repository. The *TF Ansible* code is responsible for
   all aspects of TF container build, deployment, and basic
   container orchestration.

 
