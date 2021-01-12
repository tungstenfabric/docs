Understanding Contrail Containers
=================================

 

.. raw:: html

   <div id="intro">

.. raw:: html

   <div class="mini-toc-intro">

Some subsystems of Contrail Networking solution are delivered as Docker
containers.

.. raw:: html

   </div>

.. raw:: html

   </div>

Contrail Containers
-------------------

The following are key features of the new architecture of Contrail
containers:

-  All of the Contrail containers are multiprocess Docker containers.

-  Each container has an INI-based configuration file that has the
   configurations for all of the applications running in that container.

-  Each container is self-contained, with minimal external orchestration
   needs.

-  A single tool, *Ansible*, is used for all levels of building,
   deploying, and provisioning the containers. The *Ansible* code for
   the Contrail system is named ``contrail-ansible`` and kept in a
   separate repository. The *Contrail Ansible* code is responsible for
   all aspects of Contrail container build, deployment, and basic
   container orchestration.

 
