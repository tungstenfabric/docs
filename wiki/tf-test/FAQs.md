### **1) How to reuse the test container ?**

Use the below commands to re-use an existing test-container which has been originally started from test-suite run.
    
    ./testrunner.sh list -a
    docker restart <test-container-id>; docker exec <test-container-id> kill -19 bash; docker exec -it <test-container-id>

### 2) How to start a test manually inside a container ?

    The test code will be under /contrail-test inside the container
    
    Export the below env variable 
    export PYTHONPATH=./:./scripts/:./fixtures/
    
    You can list the test case you want to run with the below command
    [root@25802eefcd00 contrail-test]# testr list-tests | grep project_add_delete
     scripts.project.test_projects_basic.TestProjectBasic.test_project_add_delete[cb_sanity,ci_sanity,sanity,suite1,vcenter_compute]

    Run the test case
    [root@25802eefcd00 contrail-test]# test run scripts.project.test_projects_basic.TestProjectBasic.test_project_add_delete

### 3) Test code organization

     The test code is organized under the following directories

     a. fixtures          - Contains all the necessary fixtures (eg. For creating virtual_network, security_group , etc)
     b. scripts           - Contains all the test scripts organized based on features which can be run simultaneously.
     c. serial_scripts    - Contains all the test scripts organized based on features which can be run not be run simultaneously.
     h. common            - Contains common infra code which can be used for common activities like parsing the test topo, etc.
     d. tcutils           - Contains utils code which can be used by multiple test cases.
     e. tools             - Contains tools code which is used to for tasks like report creation, uploading reports to webserver, collecting cores , etc.
     f. logs              - Contains logs from test run
     g. reports           - Contains report from test run

### 4) What test infrastructure tools are used.

    a. testtools
    b. test repository

### 5) How to manually upload the report

After the test has run , the report details file (report_details_<<timestamp>>.ini) and the junit-noframes.html files will be generated.
    
With the above files and contrail_test_input.yaml , which has the test config parameters we can upload the reports using the below mentioned script.
 
    export PYTHONPATH=$PATH:$PWD/fixtures:$PWD/scripts:$PWD  
    python tools/upload_to_webserver.py contrail_test_input.yaml  report_details_2018_04_21_23_09_16.ini /contrail-test/report/junit-noframes.html  

                            