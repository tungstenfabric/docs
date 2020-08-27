Additional neutron API support is added from R1.10 onwards. 

To run tests for these : 
 
    git clone https://github.com/bhushana/contrail-test
    git checkout master

 
Refer sanity_params.ini.sample and sanity_testbed.json.sample to create sanity_params.ini and sanity_testbed.json OR
do the following:

    git clone https://github.com/bhushana/contrail-fabric-utils
    cd contrail-fabric-utils
    echo "test_repo_dir=/path/to/contrail-test" >> fabrc
    fab -c fabrc setup_test_env
 
Then

    cd contrail-test
    export OS_TEST_PATH=./scripts/neutron
    ./run_tests -t

To run all tests of neutron : 

    cd contrail-test
    ./run_tests -F neutron -m -U 

The corresponding tests would be located in contrail-test/scripts/neutron and contrail-test/serial_scripts/neutron

    -m : Send the test results to mail id mentioned in sanity_params.ini
    -U : Upload the logs to webserver in sanity_params.ini

To run a specific test : 
 
    ./run_tests.sh  -- test_routers.TestRouters.test_basic_router_behavior

Optionally(-m option), the html report generated can be e-mailed 

To discover and run scripts using testtools or subunit independently, 

    cd contrail-test
    export PYTHONPATH=$PATH:$PWD:$PWD/scripts:$PWD/fixtures
    export TEST_CONFIG_FILE=sanity_params.ini
    python -m testtools.run discover -s scripts/neutron/ -l

For any help, send a mail to vjoshi@juniper.net or ask-contrail@juniper.net

