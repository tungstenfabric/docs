# Instructions for debugging contrail code in contrail containers

Contrail, in release 5.0, introduces the micro services architecture for deploying contrail config, control, agent and its dependencies as docker containers. The light weight container form factor for contrail components makes it easier for packaging, provisioning and records faster application (contrail component) and cluster boot up times. 

# Entrypoint

Contrail containers have entrypoint that is set in the image. This provides the required configuration for the application and registers the application and some services with contrail-config.

There is also a command (CMD), which runs the command to start the application. This application is identified as the respective docker container. Running state of the application determines the state of docker container.

# Packages

Contrail source is made of python modules and binaries (C++). Python modules are packaged with the source code since it is part of opencontrail, open source software, [licensed](https://github.com/Juniper/contrail-controller/blob/master/LICENSE) under Apache 2.0. The binaries are packaged along with the dependent libraries.

List of contrail components that are python sources:

1-> Controller <br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a. contrail-api <br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b. contrail-svc-monitor<br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;c. contrail-schema<br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;d. contrail-device-manager<br />

2-> Node manager<br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a. contrailconfig_nodemgr<br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b. contrailconfigdatabase_nodemgr<br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;c. contrailcontrol_nodemgr<br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;d. contrailanalytics_nodemgr<br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;e. contrailvrouter_nodemgr<br />

3-> Analytics<br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a. alarm-gen<br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b. contrail-analytics-api<br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;c. contrail-snmp-collector<br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;d. contrail-topology<br />
       
List of contrail components that are C++ sources, deployed with dependent libraries that are dynamically linked.

1-> Controller<br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a. contrail-control<br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;b. contrail-dns<br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;c. contrail-named<br />

2-> Vrouter<br />
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;a. contrail-vrouter-agent<br />

# Source code debugging of contrail

There is a way to debug the programming logic of the contrail source code in an environment where there is a need. "It works on my machine" is no escape route for contrail and we do acknowledge the fact that great software needs even greater and smart debugging capabilities to ensure developers can quickly debug and fix issues in an environment where it is found. 

## Python modules

Contrail components that are python modules can be debugged by using "python pdb". Here is one of the option that developers can use:

1-> Look at the contrail logs<br />
2-> Get a high level understanding of the code flow for a given problematic scenario<br />
3-> Understand the code path<br />
4-> Enter the docker container to access the contrail component<br />
5-> In the respective contrail container, go to the source code under "/usr/lib/python2.7/(site/dist)-packages/(contrail-python-module)"<br />
6-> Edit the file and add the following lines:<br />
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;import pdb; pdb.set_trace()<br />
7-> Exit the container<br />
8-> Restart the docker container<br />
9-> Attach to the docker container<br />
10-> Get the pdb shell<br />
11-> Debug the source code.<br /> 

Example:  

Scenario:  openstack network list - Failure

Troubleshooting Steps:
======================
    1-> Check the openstack neutron api logs
    2-> Check keystone logs
    3-> Check neutron server logs
    4-> Check contrail-api logs

If issue is in the neutron server (contrail core plugin) then do the following for source code debugging.

    1-> docker ps --filter "name=contrailconfig_api"
    2-> docker exec -it contrailconfig_api_1
    3-> edit the file /usr/lib/python2.7/site-packages/vnc_openstack/neutron_plugin_db.py
    4-> go to the function _virtual_network_list

             def _virtual_network_list(self, parent_id=None, obj_uuids=None,
                              fields=None, detail=False, count=False,
                              filters=None):
    5-> Add the pdb set_trace

              import pdb; pdb.set_trace()
     
    6-> restart docker container 
               
                docker restart contrailconfig_api_1

    7-> docker attach contrailconfig_api_1

    8-> run command "openstack neutron list"

    9-> pdb shell should show up in the terminal session running "docker attach contrailconfig_api_1"

**Note: "docker attach" - attaches to a running container to get ongoing output (stdout) and control it interactively.

    10-> To disconnect from the debugging session, please make sure to use control+P and control+Q. If you exit the container or control+D in the pdb shell, then the docker container exits. 

## C++ modules

Contrail containers that are running contrail binaries can use GNU gdb to debug the programing logic. 

For contrail C++ modules, copy the debug binary with symbols to the contrail container running the contrail binary, stop and override the entrypoint to start the gdb. 

Here are the steps:

     1-> Get the docker name of the contrail component running contrail binary
     2-> Copy the debug binary to contrail container that is running the contrail binary
     3-> Stop the docker container
     4-> Run the docker container with override command to launch gdb
     5-> Debug contrail binary with gdb

Example:

Scenario: Debug contrail-control

    1-> docker ps --filter "name=contrailcontrol_control" --no-trunc
    2-> docker cp /root/debug/contrail-control contrailcontrol_control_1:/usr/bin/
    3-> docker stop contrailcontrol_control_1
    4-> docker run -it --entrypoint /entrypoint.sh opencontrailnightly/contrail-controller-control-control:master-20180205104813-centos7-ocata gdb /usr/bin/contrail-control OR
        
        docker run --entrypoint /entrypoint.sh opencontrailnightly/contrail-controller-control-control:master-20180205104813-centos7-ocata gdb /usr/bin/contrail-control

     The first command opens a tty session with GDB. For the second command you will have to use docker attach.

     **Note: In the above command we are overriding the entrypoint command "/entrypoint.sh /usr/bin/contrail-control" with "gdb /usr/bin/contrail-control". We need the /entrypoint.sh as it sets the config params.

   5-> Continue debugging in gdb. 
   
Above method is the most convenient way to debug contrail components running in docker containers.

            

 

 

 