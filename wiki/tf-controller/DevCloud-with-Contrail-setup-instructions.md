## DevCloud Components
There are three components that needs to be installed and provisioned to make DevCloud with Contrail work.
* Management Server - CloudStack (running in the Host machine)
* Compute Node - Xen with XCP and Contrail Networking component (DevCloud image running as a VM)
* Contrail Control Node (Ubuntu 12.04 VM)

For more details on the architecture and how these components interact together, visit http://www.opencontrail.org/deploying-opencontrail/

## Preparation
### CloudStack Dev Environment
In your host machine, use the instructions [here](https://cwiki.apache.org/confluence/display/CLOUDSTACK/Setting+up+CloudStack+Development+Environment) to setup a CloudStack development environment.

### Setting up VirtualBox 
* Install VirtualBox for your host environment from [here](https://www.virtualbox.org/wiki/Downloads).
* Create and config a "host-only" network in VirtualBox, if you don't have one (or have just installed VirtualBox).
    * To create a network, go to File -> Preferences -> Network -> "Add host only network", it would usually have a name like vboxnet0 etc. (Windows Only: You don't have to perform the Add host only network" step, move on to step 3.2)
    * To config the network created in step 3.1, right click and select "Edit host-only network", then uncheck "Enable server" in the "DHCP server" tab
    *(Windows only) Start Administrative Tools > Windows Firewall with Advanced Security. Click on the "Windows Firewall Properties" (central panel, possibly quite small print) and for each of the profiles (Domain, Private, Public) click on the Protected Network Connections "Customize..." button and uncheck the "Virtual Box Host only Network" so that the Windows Firewall does not block communications on that network.

### Xen Hypervisor with XCP 1.6 
* Download the DevCloud image for CloudStack 4.3 and above from [here] (http://people.apache.org/~sebgoa/devcloud2.ova)
* Import the image into VirtualBox. After VM boots up, login into VM with `username: root, password: password`

### Contrail Control Node
* Download any of the Ubuntu VirtualBox images from [here] (http://virtualboximages.com/Ubuntu+12.04.4+amd64+Desktop+VirtualBox+VDI). (This is a Desktop image, feel free to disable the XServer or choose a Ubuntu image of your choice. Instructions to disable XServer can be found [here] (http://askubuntu.com/questions/16371/how-do-i-disable-x-at-boot-time-so-that-the-system-boots-in-text-mode))
* Create two network interfaces for the VM. (Open "Settings" of the image and choose "Network" to create the interfaces)
    * Host-only network interface - Assign a new static IP address of 192.168.56.30 to this. (Add the following config to `/etc/network/interfaces`.)

            auto eth0
            iface eth0 inet static
                address 192.168.56.30
                netmask 255.255.255.0
                network 192.168.56.0
                broadcast 192.168.56.255
                gateway 192.168.56.1
     
    * NAT network interface - This interface is to connect to the internet.
* Import the image into VirtualBox. After VM boots up, login into VM with `username: adminuser, password: adminuser`
* Run `sudo passwd root` and set the root password to `adminuser` for the Ubuntu VM. 
* Install ssh if not already installed, `sudo apt-get update` and `sudo apt-get install openssh-server`
* Reboot the VM once and login as a `root` user.

## Building the code from Source
### Cloudstack
* [Checkout](https://cwiki.apache.org/confluence/display/CLOUDSTACK/Getting+the+Source+Code) the latest master code
* Code to enable Contrail Network offering in DevCloud is under code review in the CloudStack master branch. Till it is checked in, please patch [this] (https://reviews.apache.org/r/19892/diff/raw/) diff into the CloudStack code. 
    * Note: This instruction will be removed once the code is checked in.
* Build the  management server on your host machine (laptop)

         mvn -P developer,systemvm clean install

### Compute Node (Xen with XCP and Contrail Networking)
* **Note:** This section assumes that you have a valid Git account and you have setup the account for ssh access. If you have not, follow [these] (https://help.github.com/articles/generating-ssh-keys) instructions 
* In the DevCloud VM, clone the scripts which would build and install the Contrail bits.
         `git clone https://github.com/rranjeet/vrouter-xen-utils.git`
* Go to the directory, `cd vrouter-xen-utils/contrail-devcloud`
* Run `install_compute_dependencies.sh`
* And run `download_the_code.sh`. The shell script will prompt for your git password to download the Contrail code.
    * Sometimes, wget freezes while downloading some of the packages. If you see that the download is frozen for a long time, break in and restart the script.
* To build, run `build_copy.sh`. The build would take 60 minutes to complete.


### Contrail Control Node (Ubuntu Server)
* **Note:** This section assumes that you have a valid Git account and you have setup the account for ssh access. If you have not, follow [these] (https://help.github.com/articles/generating-ssh-keys) instructions 

* Install git, `apt-get install git`
* In the Ubuntu VM, clone the scripts which would build and install the Contrail Control Node bits.
         `git clone https://github.com/rranjeet/vrouter-xen-utils.git`
* Go to the directory, `cd vrouter-xen-utils/contrail-devcloud`
* Run `install_control_dependencies.sh`
* And run `download_the_code.sh`. The shell script will prompt for your git password to download the Contrail code.
    * Sometimes, wget freezes while downloading some of the packages. If you see that the download is frozen for a long time, break in and restart the script.
* Run `build_control.sh`. This will build all the Contrail Control components. It will take close to 60 minutes.

## Provisioning/Starting the setup
### CloudStack
* Create a file with name `contrail.properties` in path `client/target/generated-webapp/WEB-INF/classes/contrail.properties` and add the following text into it.

        api.hostname = 192.168.56.30
        api.port = 8082

* Drop the existing Cloudstack state (if any) and set up the database clean.

        mvn -P developer -pl developer,tools/devcloud -Ddeploydb

* Start the management Server

        mvn -pl :cloud-client-ui jetty:run
  Wait till the management server is up and running.
* Run CloudStack provisioning in a new terminal

        cd tools/devcloud
        python ../marvin/marvin/deployDataCenter.py -i devcloud-advanced_juniper-contrail.cfg
  
### Control Node (Ubuntu Server)
* Run `copy_control_binaries.sh` which will copy all the files in the relevant directories.
* Run `install_control_components.sh` which will install Cassandra, ZooKeeper and the IFMap Server
* Run `start_control_node.sh` which will start all the required services.
    * All the services are started using the `screen` command.
    * To monitor the different services, `screen -r contrail` and once inside the screen, use `Ctrl A + "` to list the different services that are running.

### Compute Node (XenServer)
* To setup, run `xen_setup.sh`.
* Restart the VM.

Note: Restart the Cloudstack Management server once again. (Break into the terminal which is running the CS management server and rerun `mvn -pl :cloud-client-ui jetty:run`.

## And Finally...
After all these steps, you should be able to
* login to the CS management server with `192.168.56.1:8080/client`. Credentials are `admin, password`.
* In Infrastructure tab, you should see the hosts, primary storage, secondary storage and two System VMs running.
* The Templates tab should show templates to launch the VMs as ready.
* In the Network tab, you should be able to create a Juniper Network offering.
* Once the network offering is created, you should be able to create new instances of the "Tiny Linux" template.