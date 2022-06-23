Creating Projects in OpenStack for Configuring Tenants in Tungsten Fabric
=========================================================================

:date: 2016-12-15

In Tungsten Fabric, a tenant configuration is called a project. A project is
created for each set of virtual machines (VMs) and virtual networks
(VNs) that are configured as a discrete entity for the tenant.

Projects are created, managed, and edited at the OpenStack :guilabel:`Projects`
page.

1. Click the :guilabel:`Admin` tab on the OpenStack dashboard, then click the
   :guilabel:`Projects` link to access the :guilabel:`Projects` page.

   |Figure 1: OpenStack Projects|

2. In the upper right, click the :guilabel:`Create Project` button to access the
   :guilabel:`Add Project` window.

   |Figure 2: Add Project|

3. In the :guilabel:`Add Project` window, on the :guilabel:`Project Info` tab, enter a
   :guilabel:`Name` and a :guilabel:`Description` for the new project, and select the
   :guilabel:`Enabled` check box to activate this project.

4. In the :guilabel:`Add Project` window, select the :guilabel:`Project Members` tab,
   and assign users to this project. Designate each user as :guilabel:`admin` or
   as :guilabel:`Member`.

   As a general rule, one person should be a super user in the :guilabel:`admin`
   role for all projects and a user with a :guilabel:`Member` role should be
   used for general configuration purposes.

5. Click :guilabel:`Finish` to create the project.

Refer to OpenStack documentation for more information about creating and
managing projects.

 

.. |Figure 1: OpenStack Projects| image:: images/s041521.gif
.. |Figure 2: Add Project| image:: images/s041522.gif
