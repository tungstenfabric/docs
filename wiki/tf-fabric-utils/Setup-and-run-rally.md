One can provision rally on a VM/BM node which can be either separate node or one of the cluster node. Once provision and setup rally, then we can run rally tasks/scenarios to do performance testing and benchmarking. 

Note that the code to setup rally is still under review process (https://review.opencontrail.org/#/c/15762/), so not got merged till yet.

## Steps
1. setup testbed.py with below details (refer testbeds/testbed_with_rally_example.py)

```
# Add a new role for rally

env.roledefs = {
    'all': [host1, host2, host3, host4, host5, host6, host7, host8, host9, host10],
    'cfgm': [host1, host2, host3],
    'openstack': [host1],
    'control': [host1, host2, host3],
    'compute': [host4, host5, host6, host7, host8, host9, host10],
    'collector': [host1, host2, host3],
    'webui': [host1],
    'database': [host1, host2, host3],
    'build': [host_build],
    'storage-master': [host1],
    'storage-compute': [host4, host5, host6, host7, host8, host9, host10],
    __'rally': [host1]__
}

# Add rally specific params as below

# OPTIONAL RALLY CONFIGURATION
# =======================================
# Rally is installed from github source, with default to be github.com/openstack/rally.git.
# There are two params can be added here to control any different repo to be used,
# rally_git_url - the git url from which source can be cloned (git or https url can be provided)
# rally_git_branch - branch name to be used, default to master.
#        Since we customized couple of rally plugin code, we should provide these parameters with appropriate git repo
# rally_task_args - rally task arguments  - a hash of arguments taken by scenarios.yaml jinja2 template
##
rally_git_url = 'https://github.com/hkumarmk/rally'
rally_git_branch = 'network_plus'
rally_task_args = {'cxt_tenants': 1, 'cxt_users_per_tenant': 4, 'cxt_network': True, 'base_network_load_objects': 20000, 'load_type': 'constant', 'times': 2}

```

2. install rally by running "fab install_rally"
3. Configure rally with current openstack cluster by running "fab setup_rally"
4. Now one can run rally 
  * either with the task args provided in the testbed by running "fab run_rally"
  * or with different task args by populate the arguments in a file and provide file name as argument to run_rally  - run "fab run_rally:/tmp/args.yaml", where /tmp/args.yaml contain task args like " {cxt_tenants: 1, cxt_users_per_tenant: 4, cxt_network: true, base_network_load_objects: 20, load_type: serial, times: 1, scenario_args: { random: {image_id: 54e959d5-7632-4689-93d3-87c9eb5807a4, flavor_id: 1 }}}"

Please refer https://github.com/hkumarmk/rally/tree/network_plus/samples/tasks/scenarios/custom for more details about task parameters.

