Caveat: These steps only works from systems from within Juniper Networks, Inc.

```
# Use local disk space e.g. /build/$USER
BUILD=/build/$USER/sandbox
rm -rf $BUILD
mkdir -p $BUILD
cd $BUILD
/cs-shared/tools/bin/repo init --quiet --repo-url=https://github.com/opencontrail-ci-admin/git-repo.git -u git@github.com:Juniper/contrail-vnc-private -m R3.1/ubuntu-14-04/manifest-mitaka.xml
/cs-shared/tools/bin/repo sync
python third_party/fetch_packages.py 
scons -uj8 --optimization=production control-node [contrail-vrouter-agent agent:contrail-tor-agent]
ls -al build/production/control-node/contrail-control build/production/vnsw/agent/contrail/contrail-vrouter-agent build/production/vnsw/agent/ovs_tor_agent/contrail-tor-agent
```

FAQ:
1) /cs-shared/tools/bin/repo init failed with "error: could not verify the tag 'v1.12.14'",
   then check the following:
   a) ssh git@github.com
      If successful, the above command should display your "user_id".
      For e.g: 
      .. Hi nkarjala! You've successfully authenticated, but GitHub does not provide shell access.
   b) move your existing ~/.repoconfig to ~/repoconfig and re-run repo init
 