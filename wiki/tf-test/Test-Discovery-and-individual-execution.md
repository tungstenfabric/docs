Following commands can be used to list all tests:

    pip install nose testrepository junos-eznc tabulate pyvmomi

    cd contrail-test
    PYTHONPATH=$PATH:$PWD:$PWD/serial_scripts:$PWD:fixtures nosetests -v --collect-only

To find tests matching a pattern:

    cd contrail-test
    PYTHONPATH=$PATH:$PWD:$PWD/serial_scripts:$PWD:fixtures nosetests -v --collect-only 2>&1 | grep <pattern>

To execute a particular test:

    cd contrail-test
    PYTHONPATH=$PATH:$PWD:$PWD/scripts:$PWD/fixtures python -m testtools.run <dot-separated-path> 
    for e.g.
    PYTHONPATH=$PATH:$PWD:$PWD/scripts:$PWD/fixtures python -m testtools.run scripts.vpc.test_vpc.VpcSanityTests2.test_subnet_create_delete

To find all 'tagged' tests:

    cd contrail-test
    PYTHONPATH=$PATH:$PWD:$PWD/serial_scripts:$PWD:fixtures nosetests -v --collect-only 2>&1 | grep "\[.*\]"