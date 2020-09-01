Every 24 hours (at 11pm PST / 7am UTC) we run full build and publish containers to [DockerHub](https://hub.docker.com/u/opencontrailnightly/). Build usually takes less than 3 hours (~1h for packaging, ~1h for container build and 30-50 minutes for container publishing to Dockerhub).

## Tags
Every container is tagged as following:
`$branch-$operatingsystem-$openstackversion-bld-$buildnumber` e.g. `master-centos7-ocata-bld-5`.

## Logs
Logs for every periodic build are available [here](http://logs.opencontrail.org/periodic-nightly/) and are created for every consecutive build.

## Manifest.xml
For every build, we generate static `manifest.xml` file with commit-id of every repo used for build. `manifest.xml` is available in packaging job (e.g. `contrail-vnc-build-package-centos74-nightly`) in `zuul-info` directory. Take a look [here](http://logs.opencontrail.org/periodic-nightly/13/contrail-vnc-build-package-centos74-nightly/zuul-info/manifest.xml).