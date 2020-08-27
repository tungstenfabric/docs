We have a unit test framework for contrail-ansible-internal which cover only configurations that made by contrail-ansible-internal. Please refer https://github.com/Juniper/contrail-docker/blob/master/specs/ansible-unit-test-implementation.md for more details.

In order to setup unit test please follow below steps

NOTE: You may setup python virtualenv to setup test environment.

1. Install dependencies. Following python modules are required for unit test
  * ansible=2.2.0.0
  * setuptools=>13.0.0
  * tabulate
2. Install python-contrailctl
  2.1 Get the code - python-contrailctl is in https://github.com/Juniper/contrail-docker/tree/master/tools/python-contrailctl do a git clone that code
  2.2 Install it - run python setup.py install from within python-contrailctl directory
3. Get contrail-ansible-internal (https://github.com/Juniper/contrail-ansible-internal)
4. Run tests
```
$ cd contrail-ansible-internal
$ python test.py
```