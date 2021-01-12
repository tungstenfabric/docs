Upgrading Contrail Networking using contrail-ansible Deployer
=============================================================

 **Note**

This procedure can be used for Contrail Networking upgrades to Contrail
Networking Release 2003 or earlier.

If you are upgrading to Contrail Networking Release 2005 or later using
the Ansible deployer, see `How to Perform a Zero Impact Contrail
Networking Upgrade using
Ansible <../installation/installing-contrail-ansible-ziu.html>`__.

Use the following procedure to upgrade Contrail Networking using
contrail-ansible deployer.

The procedure supports incremental model and you can use it to upgrade
from Contrail Networking Release ``N-1`` to ``N``.

Take snapshots of your current configurations before you proceed with
the upgrade process. For details, refer to `How to Backup and Restore
Contrail Databases in JSON
Format <../../concept/backup-using-json-50.html>`__.

1. Navigate to the directory where the
   ``contrail-ansible-deployer-<xxxx>.<NN>.tgz`` was untarred.

   See `Sample instances.yml
   File <../configuration/deploy-cluster-contrail-command-instances-yml.html#sample_instances_yml>`__.

   *Example using Contrail Networking Release 2003*:

   ``cd contrail-ansible-deployer-2003.33/contrail-ansible-deployer/config/``

   ``vi contrail-ansible-deployer-2003.33/contrail-ansible-deployer/config/instances.yaml``

   Sample ``instances.yaml`` files for various other deployments are
   available at the same directory.

2. Update ``CONTRAIL_VERSION`` and ``CONTRAIL_CONTAINER_TAG`` to the
   desired version tag in this ``instances.yml`` file.

   Access ``CONTRAIL_CONTAINER_TAG`` located at `README Access to
   Contrail Networking Registry
   20xx <https://www.juniper.net/documentation/en_US/contrail20/information-products/topic-collections/release-notes/readme-contrail-20.pdf>`__  .

   .. raw:: html

      <div id="jd0e77" class="sample" dir="ltr">

   For example:

   .. raw:: html

      <div class="output" dir="ltr">

   ::

      CONTRAIL_VERSION = 2003.33
      CONTRAIL_CONTAINER_TAG = 2003.33

   .. raw:: html

      </div>

   .. raw:: html

      </div>

3. Run the following commands from ``contrail-ansible-deployer``
   directory.

   -  For Contrail with OpenStack deployment:

      | ``cd contrail-ansible-deployer``
      | ``ansible-playbook -e orchestrator=openstack -i inventory/ playbooks/install_openstack.yml -v``
      | ``ansible-playbook -e orchestrator=openstack -i inventory/ playbooks/install_contrail.yml -v``

   -  For Contrail with Kubernetes deployment:

      | ``cd contrail-ansible-deployer``
      | ``ansible-playbook -e orchestrator=kubernetes -i inventory/ playbooks/install_k8s.yml -v``
      | ``ansible-playbook -e orchestrator=kubernetes -i inventory/ playbooks/install_contrail.yml -v``

The ansible playbook logs are available on the terminal during
execution. You can also access it at ``/var/log/ansible.log``.

 
