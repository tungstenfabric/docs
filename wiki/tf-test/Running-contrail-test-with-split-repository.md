We support two ways to run contrail-test

* With docker

  See [contrail-test-ci wiki](https://github.com/Juniper/contrail-test-ci/wiki/How-to-use-contrail-test-ci-container) for details

* Without docker

  1. Get install.sh script from appropriate branch like below
```
$ wget  https://raw.githubusercontent.com/Juniper/contrail-test-ci/master/install.sh
```

  2. Run install.sh with "install" argument

```
Install Contrail-test or contrail-test-ci

Usage: ./install.sh install [OPTIONS] (contrail-test|contrail-test-ci)

  -h|--help                     Print help message
  --test-repo REPO              Contrail-test git repo, Default: github.com/juniper/contrail-test-ci.git
  --test-ref REF                Contrail-test git reference - commit id, branch, tag, Default: master
  --fab-repo FAB_REPO           Contrail-fabric-utils git repo
  --fab-ref FAB_REF             Contrail-fabric-utils git reference (commit id, branch, or tag), Default: master
  --ci-repo CI_REPO	            Contrail-test-ci git repo, Default: github.com/juniper/contrail-test.git
  --ci-ref CI_REF               Contrail-test-ci reference (commit id, branch, or tag), Default: master
  --test-artifact ARTIFACT      Contrail test tar file - this tar file will be used instead of git source in case provided
  --ci-artifact CI_ARTICACT     Contrail test ci tar file
  --fab-artifact FAB_ARTIFACT   Contrail-fabric-utils tar file
  -i|--install-dir INSTALL_DIR  Install directory, Default: /opt/contrail-test
  -u|--package-url PACKAGE_URL  Contrail-install-packages deb package web url (http:// or https://) or scp path
                                (ssh://<server ip/name/< package path>), if url is provided, the
                                package will be installed and setup local repo.
                                In case of scp, user name and password will be read from environment variables
                                SSHUSER - user name to be used during scp, Default: current user
                                SSHPASS - user password to be used during scp

  positional arguments
    What to install             Valid options are contrail-test, contrail-test-ci

 Example:

  # Install contrail-test on a node which doesnt have contrail-install-packages setup (-u is required in this case)

  $ ./install.sh install --test-repo https://github.com/juniper/contrail-test --test-ref working
        --ci-repo https://github.com/juniper/contrail-test-ci
        -u http://nodei16/contrail-install-packages_2.21-105~juno_all.deb contrail-test

  # Install contrail-test-ci
  $ export SSHUSER=user1 SSHPASS=password
  $ ./install.sh install --test-repo https://github.com/juniper/contrail-test --test-ref working
     --ci-repo https://github.com/juniper/contrail-test-ci
     -u ssh://nodei16/var/cache/artifacts/contrail-install-packages_2.21-105~juno_all.deb contrail-test-ci

  # Install contrail-test under custom install directory and the machine already have contrail-install-packages setup.

  $ ./install.sh install -i /root/contrail-test contrail-test
```

Below command will install contrail-test under /root/contrail-test from the repo https://github.com/juniper/contrail-test on a machine which already have contrail-install-packages setup.

```
bash ./install.sh install -i /root/contrail-test/ contrail-test
```

Now you can run run_tests.sh from /root/contrail-test as before.