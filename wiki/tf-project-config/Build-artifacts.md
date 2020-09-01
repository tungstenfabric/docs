For every review (verified by Zuulv3), there are artefacts available in the internal network.

## Packages
Packages are available at [ci-repo](http://ci-repo.englab.juniper.net/pulp/repos/). Every review creates a directory in format `$review_id-$patchset_no` (e.g. `37779-10`) which includes `Packages` dir. All packages are listed alphabetically and you can download them manually. You can also use full URL as yum repo:
```
[opencontrail]
name=opencontrail
baseurl=http://ci-repo.englab.juniper.net/pulp/repos/37779-10/
enabled=1
gpgcheck=0
```

## Containers (microservices)
Containers are hosted on ci-repo too, however every review sets up a separate docker registry on custom port. 

To verify what port was used for your review, go to the logs for container build job and then `ara` directory. There'll be a playbook called `setup-docker-registry.yaml` which contains task `setup-docker-registry : get registry port`. Click on `CHANGED` next to the task to get port number from stdout field (e.g. 32987). When you combine ci-repo url with port (e.g. `http://ci-repo.englab.juniper.net:32987`), you can provide the URL for [contrail-ansible-deployer](http://github.com/Juniper/contrail-ansible-deployer/) to use with. 

To verify if Docker registry is still there (we clean them up automatically, regardless of the job result), use your combined URL and append `/v2/_catalog` suffix to it (e.g. `http://ci-repo.englab.juniper.net:32987/v2/_catalog`). You should get HTTP 200 response from Docker Registry API with list of existing repositories (containers).

Note: our Docker Registry doesn't use https, so you need to configure it as `insecure registry`. Please take a look [here](https://docs.docker.com/registry/insecure/) to see how do it.