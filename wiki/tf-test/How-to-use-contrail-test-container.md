Use Contrail-test container
===========================
## Table of contents
* [Use Contrail-test Container](#use-contrail-test-container)
  * [Using testrunner.sh](#using-testrunnersh)
  * [Few testrunner.sh sample commands](#sample-testrunnersh-commands)
  * [Manually using docker commands](#manually-run-contrail-test-using-docker-commands)
* [Other Tools](#other-tools)
  * [tools/tenent_cleaner.py](#toolstenent_cleanerpy)


## Use Contrail-test Container

Before using the container, one must install docker on the host. Please refer the docker installation document for docker install instructions (https://docs.docker.com/engine/installation/).

### Using testrunner.sh
This is a helper script to manage (run/rebuild/list) contrail-test container. 

* Get testrunner.sh from github

```
$ wget https://raw.githubusercontent.com/Juniper/contrail-test/master/testrunner.sh
$ chmod +x ./testrunner.sh

$ ./testrunner.sh -h

Usage: ./testrunner.sh <Subcommand> [OPTIONS|-h]
Run Contrail test suite in docker container

Subcommands:
  run 	 Run contrail-test container
  rebuild  Rebuild the container provided
  list   List contrail-test containers
  load 	 Load the container image from the filepath provided (tar, tar.gz, tar.bz2)
  pull 	 pull the test container image from the repository

Run ./testrunner.sh <Subcommand> -h|--help to get subcommand specific help 

```
* Pull container image

```
# ./testrunner.sh pull -h

Usage: ./testrunner.sh pull RemoteRegistry/image:tag
download the docker image to local system from remote registry

Possitional Parameters:

  <image>        remote image
                eg: ./testrunner.sh pull myregistry.local:5000/contrail-test-test:4.1.0.0-6

```
* Load container images

```
# ./testrunner.sh load -h

Usage: ./testrunner.sh load DOCKER-IMAGE-URL
Load the docker image to local system

Possitional Parameters:

  <docker-image-url>        Docker image tar.gz url. Supports three modes:
                           http[s] url: example, http://myrepo/contrail-test-images/docker-image-contrail-test-kilo-3.0-2709.tar.gz
                           file path: example  /root/docker-image-contrail-test-kilo-3.0-2709.tar.gz

```

Load docker image from http url

```
# ./testrunner.sh load http://nodei16/docker-image-contrail-test-juno-3.0-2709.tar.gz
--2016-02-26 16:18:26--  http://nodei16/docker-image-contrail-test-juno-3.0-2709.tar.gz
Resolving nodei16 (nodei16)... 127.0.0.1, 10.204.217.128
Connecting to nodei16 (nodei16)|127.0.0.1|:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 425768269 (406M) [application/x-gzip]
Saving to: ‘/tmp/tmp.x7SNNIHMdL/docker-image.tar.gz’

100%[================================================================================================================================================================>] 425,768,269  448MB/s   in 0.9s   

2016-02-26 16:18:27 (448 MB/s) - ‘/tmp/tmp.x7SNNIHMdL/docker-image.tar.gz’ saved [425768269/425768269]

Loading the image
Successfully Loaded the image http://nodei16/docker-image-contrail-test-juno-3.0-2709.tar.gz

```
* Run contrail-test using testrunner

This will help running the contrail-test containers without learning docker commands. Also this script will help to save the data out of the contrail-test into the host. It saves logs, reports, testbed.py, and contrail-test code itself out of contrail-test container to said directory (provided using --run-path).

```

# ./testrunner.sh run -h

Usage: ./testrunner.sh run [OPTIONS] (<image_tag>)
Run Contrail test suite in docker container

  -p, --run-path RUNPATH           Directory path on the host, in which contrail-test save all the
                                            results and other data. Default: /root/contrail-test-runs/
  -s, --shell                      Do not run tests, but leave a shell, this is useful for debugging.
  -S, --scenarios SCENARIOS        list of scenarios that need to run as part rally tests. If empty ,
                                            runs all the tests under ./rally/scenarios
  -i, --use-ci-image               Use ci image, by default it will use the image name "cirros",
                                   One may override this by setting the environment variable $CI_IMAGE
  -r, --rm	                   Remove the container on container exit, Default: Container will be kept.
  -b, --background                 run the container in background
  -n, --no-color                   Disable output coloring
  -z, --tempest_dir TEMPEST DIR            Path to the tempest , where it is cloned
  -t, --testbed TESTBED            Path to testbed file in the host,
                                            Default: /opt/contrail/utils/fabfile/testbeds/testbed.py
  -k, --ssh-key FILE_PATH          ssh key file path - in case of using key based ssh to cluster nodes.
                                                  Default: /root/.ssh/id_rsa
  -K, --ssh-public-key FILE_PATH   ssh public key file path. Default: <ssh-key provided>.pub
  -P, --params-file PARAMS_FILE    Contrail test input yaml file
  -f, --feature FEATURE            Features or Tags to test - valid options are sanity, quick_sanity,
                                            ci_sanity, ci_sanity_WIP, ci_svc_sanity, upgrade, webui_sanity,
                                            ci_webui_sanity, devstack_sanity, upgrade_only. Default: sanity
                                            NOTE: this is only valid for Full contrail-test suite.
 -T, --test-tags TEST_TAGS         test tags to run specific tests
 -c, --testcase TESTCASE           testcase to execute
 -m, --mount_local path           mount a local folder which has contrail-test
NOTE: Either testbed.py (-t) or test-input-yaml-file (-P) required

Possitional Parameters:

  <image_tag>        Docker image tag to run (Run "./testrunner.sh list -i" to list all images available)

$ ./testrunner.sh list -i

=========== Images =============
IMAGE                                              IMAGE ID             VIRTUAL SIZE
opencontrailnightly/contrail-test-test:ocata-master-1 294fc58b3cd4         1.48 GB

# ./testrunner.sh run  contrail-test-juno:2.21-105 

```

The above testrun may create below directory structure under run_path directory in the host

```
# ls ~/contrail-test-runs/
  2016_02_26_16_17_43

# ls ~/contrail-test-runs/2016_02_26_16_17_43
contrail-test  logs  reports

```

* Run contrail-test container with a shell instead of running contrail-test. This would be helpful to login to the container and do some debugging

```
# ./testrunner.sh run  -s contrail-test-juno:2.21-105 

root@80132b7c05a0:/# 
```

* Run with testbed.py in non-standard location (by default it takes from /opt/contrail/utils/fabfile/testbeds/testbed.py)

```
# ./testrunner.sh run  -t /tmp/testbed.py contrail-test-juno:2.21-105 

```

* List running contrail-test containers

```
# ./testrunner.sh list
CONTAINER ID        IMAGE                            COMMAND             CREATED             STATUS              PORTS               NAMES
9664fea32bd3        contrail-test-juno:2.21-105   "/entrypoint.sh"    7 minutes ago       Up 7 minutes                            contrail_test_egueqpcv

``` 

* List all contrail-test containers (including all running as well as finished containers)

```
# ./testrunner.sh list -a
CONTAINER ID        IMAGE                            COMMAND             CREATED             STATUS                      PORTS               NAMES
80132b7c05a0        contrail-test-juno:2.21-105   "/bin/bash"         5 minutes ago       Exited (0) 3 minutes ago                        contrail_test_kkqrdrcn
9664fea32bd3        contrail-test-juno:2.21-105   "/entrypoint.sh"    8 minutes ago       Up 8 minutes                                    contrail_test_egueqpcv
```

* Rebuild existing container (running or non-running container)

```
# ./testrunner.sh rebuild -h

Usage: ./testrunner.sh rebuild [OPTIONS] <container id/name>
Rebuild contrail-test containers

  -p, --run-path RUNPATH           Directory path on the host, in which contrail-test save all the
                                            results and other data. Default: /root/contrail-test-runs/
  -s, --shell                      Do not run tests, but leave a shell, this is useful for debugging.
  -r, --rm	                     Remove the container on container exit, Default: Container will be kept.
  -b, --background                 run the container in background
  -n, --no-color                   Disable output coloring
  -t, --testbed TESTBED            Path to testbed file in the host,
                                            Default: /opt/contrail/utils/fabfile/testbeds/testbed.py
  -T, --testbed-json TESTBED_JSON  Optional testbed json file.
  -P, --params-file PARAMS_FILE    Optional Sanity Params ini file
  -f, --feature FEATURE            Features or Tags to test - valid options are sanity, quick_sanity,
                                            ci_sanity, ci_sanity_WIP, ci_svc_sanity, upgrade, webui_sanity,
                                            ci_webui_sanity, devstack_sanity, upgrade_only. Default: sanity
                                            NOTE: this is only valid for Full contrail-test suite.

NOTE: Either testbed.py (-t) or both testbed-json and params-file required

Possitional Parameters:

  <container id/name>        The container ID or name ( "./testrunner.sh list -ca" to list all containers)

```

Below code will rebuild an exited container

```

# ./testrunner.sh rebuild contrail_test_eqsjwxar
 rebuilding container - contrail_test_eqsjwxar
 This process will create an image with the container contrail_test_eqsjwxar
 Creating the image img_contrail_test_eqsjwxar
b9fc87f3dc4b7da716f98ed83ba456ba1b3990df737e55f6cbcabeac8d13e578

```

### Manually run contrail-test using docker commands

- Load docker image from /export/docker/contrail-test/contrail-test-juno-2.21-105.tar.gz

```
$ docker load < /export/docker/contrail-test/contrail-test-juno-2.21-105.tar.gz

```
- Execute docker container
  
  it run contrail-test tests and log the console. The console output may be captured at later point by running
  "docker logs [-f] <container id>".

```
$ docker run -v /opt/contrail/utils/fabfile/testbeds/testbed.py:/opt/contrail/utils/fabfile/testbeds/testbed.py -t contrail-test-juno:2.21-105
```
- Execute the container with logs saved in specific location

  The logs will be saved under /export/logs/contrail-test/ on docker host.

```
  $ docker run -v /opt/contrail/utils/fabfile/testbeds/testbed.py:/opt/contrail/utils/fabfile/testbeds/testbed.py -v /export/logs/contrail-test/:/contrail-test/logs -t contrail-test-juno:2.21-105
```

### Sample testrunner.sh commands
- Execute all tests with a specific tag (-T) (below example executes k8s_sanity tagged tests)
```
./testrunner.sh run -P contrail_test_input.yaml -T k8s_sanity opencontrailnightly/contrail-test-test:ocata-master-1
```
- Execute a specific feature (-f) (below example executes all tests part of ci_sanity)
```
./testrunner.sh run -P contrail_test_input.yaml -f ci_sanity opencontrailnightly/contrail-test-test:ocata-master-1
```
- Execute a specific testcase (-c) (below example executes a single testcase test_project_add_delete)
```
./testrunner.sh run -P contrail_test_input.yaml -c test_project_add_delete opencontrailnightly/contrail-test-test:ocata-master-1
```
- Run tests with passwordless login to the cluster-nodes
```
./testrunner.sh run -P contrail_test_input.yaml -k ~/.ssh/id_rsa opencontrailnightly/contrail-test-test:ocata-master-1
```

## Other Tools

### tools/tenent_cleaner.py

This script can be used to cleanup tenant data. This can be run after testrun to make sure tenant is clean.
```
    $ ./tenant_cleaner.py -h
    usage: tenant_cleaner.py [-h] [--user USER] [--password PASSWORD]
                             [--auth-url AUTH_URL] [--auth-tenant AUTH_TENANT]
                             [--ip IP] [--port PORT]
                             tenant [tenant ...]

    Cleanup provided tenants by removing all objects in it.It expect openstack
    credentials from OS_ environment variables in openrc format.The credentials
    can be provided as commandline arguments also

    positional arguments:
      tenant                List of tenants to be cleaned up Note that, the user
                            must have access to the tenants listed

    optional arguments:
      -h, --help            show this help message and exit
      --user USER           Openstack user, if not provided, try to get it from
                            environment variable "OS_USERNAME" with default user
                            as "admin"
      --password PASSWORD   Openstack password
      --auth-url AUTH_URL   Openstack auth url, by default try to get from
                            environment variableOS_AUTH_URL with default of
                            http://127.0.0.1:5000/v2.0/
      --auth-tenant AUTH_TENANT
                            Openstack tenant to connect to
      --ip IP               IP Address of the controller
      --port PORT           Port of the controller

    $ ./tenant_cleaner.py --ip 10.204.217.88 tenant1 tenant2 tenant3
    No objects found in tenant tenant1
    No objects found in tenant tenant2
    Deleted: http://10.204.217.88:8082/security-group/f633163c-2c96-4722-94b2-3a125e981492
    No nova objects found in tenant tenant3
```