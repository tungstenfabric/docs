1. Introduction

   Contrail integration with VMware runs contrail vrouter in a VM (ContrailVM) on 
   each of the ESXi hosts in the vcenter cluster. Today, the ContrailVM provisioned 
   and setup is like any other tenant VM running in the cluster.

2. Problem statement

   The problems tried to address here are:
   * auto-deploy the provisioning of ContrailVM
   * provide more privileges to ContrailVM 
   * manage and monitor ContrailVM

3. Proposed solution

   VMware provides a standard vCenter solution called vSphere ESX Agent Manager (EAM),
   this allows other solutions to deploy, monitor, and manage ESX Agents (VMs) on ESXi hosts.
   ESX Agent virtual machines are similar to services in Windows or Linux, making them more
   critical and privileged than other tenant VMs on the host.

   ESX Agent Manager performs the following functions:
   * Provisions ESX agent virtual machines for solutions.
   * Monitors changes to the ESX agent virtual machines and their scope in vCenter Server.
   * Reports configuration issues in the ESX agents to the solution.
   * Integrates agent virtual machines with vSphere features such as Distributed Resource Scheduler (DRS),
     Distributed Power Management (DPM), vSphere High Availability (HA), Maintenance mode, 
     and operations such as adding and removing hosts to and from clusters.

   The proposal is to use ESX Agent Manager to provision, manage and monitor ContrailVM that 
   run on ESXi host. 

   This involves the below:
   * Connect and authenticate with the ESX Agent Manager. Every vCenter Server instance contains 
     a running ESX Agent Manager, connect to this instance and authenticate.
   * Create an agency (ContrailVM-Agency) which acts as a container of all the ESX Agent VMs,
     and deploy ContrailVM on each of the ESXi hosts in the clusters.

   To integrate a solution with ESX Agent Manager, following are the requirements:
   * The user/solution must connect and authenticate with the ESX Agent Manager.
   * Use Open Virtualization Format (OVF) to package ESX agent virtual machines or vApps. 
     ESX Agent Manager only supports the deployment of virtual machines using OVF.
   * Use HTTP or HTTPS to publish OVF files to ESX Agent Manager.
   * Use vCenter Server Compute Resources to define the ESX agent scope. 
     This can be clusters or Standalone ESXi hosts.

   ESX Agent Manager (EAM) integration features:

   - Auto-deploy ContrailVMs on ESXi hosts in scope (clusters)

   - Manage and Monitor ContrailVMs through EAM in the vSphere web client
      - View ContrailVM-Agency and ContrailVMs status/events
      - Resolve issues from EAM
         - EAM warns when ContrailVM is powered off/deleted, and allows to proceed if warning is acknowledged
         - EAM reports when ContrailVM is powered off/deleted, the ContrailVM-Agency shows in “Alert” (red) state
         - EAM resolves issues with ContrailVM-Agency
            - Right-click on Agency and select “Resolve All Issues”
               - If ContrailVM is powered off, should power on
               - If ContrailVM is missing, deploys ContrailVM on the host and should power on                                            

   - AddHost
     - Add a host to cluster on which EAM deployed ContrailVMs, then ContrailVM is deployed on the new host
       Note: Requires "AgentVM Settings" to be updated for the new host, without that InstallAgent would fail
   
   - Maintenance Mode
     - If ESXi host enters maintenance mode, EAM powers off the ContrailVM
     - When ESXi host exits from maintenance mode, ContrailVM is powered on

   - vSphere DRS
     - EAM pins ContrailVM to the hosts on which they are running
       DRS does not move ContrailVMs between hosts in a cluster
     - EAM blocks DRS from moving tenant VMs to hosts in clusters where ContrailVM is not available

   - vSphere DPM
     - DPM can put a host into standby mode even when ContrailVM is present
     - DPM powers off ContrailVMs only after it has moved all tenant VMs to another host and put the host
       into standby mode.

   - VMWare HA
     - When a host restarts, VMWare HA restarts the ContrailVM before it restarts other VMs
     - If a host stops unexpectedly, VMWare HA does not start a ContrailVM on another host,
       unless failover policy is in use
     - ContrailVMs are not included in slot size for admission control calculations

3.1 Alternatives considered

3.2 API schema changes

3.3 User workflow impact

3.4 UI changes

3.5 Notification impact

4. Implementation

4.1 Work items

   - Deploy ContrailVM from ESX Agent Manager
     - Host ContrailVM ovf in an http/https server location
     - Connect to ESX Agent Manager and authenticate with session cookie
     - Deploy ContrailVM-Agency and ContrailVM on the ESXi hosts
   - Integrate with ESX Agent Manager supported vSphere features

   pyvmomi provides Eamobjects.py as an interface to the EAM API.
   Eamobjects.py is used to connect to EAM and deploy ContrailVM.

5. Performance and scaling impact

5.1 API and control plane

5.2 Forwarding performance

6. Upgrade

7. Deprecations

If this feature deprecates any older feature or API then list it here.

8. Dependencies

9. Testing

9.1 Unit tests

9.2 Dev tests

9.3 System tests

10. Documentation Impact

11. References

http://pubs.vmware.com/vsphere-6-5/index.jsp?topic=%2Fcom.vmware.vsphere.ext_solutions.doc%2FGUID-BCF564C0-3CCA-4067-99D1-5C90D86914B1.html
https://vdc-download.vmware.com/vmwb-repository/dcr-public/3d076a12-29a2-4d17-9269-cb8150b5a37f/8b5969e2-1a66-4425-af17-feff6d6f705d/SDK/eam/doc/index.html
