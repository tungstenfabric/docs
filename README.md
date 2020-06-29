# Working with the docs

The documentation is delivered via a Read The Docs (RTD) website.  

TF uses the Linux Foundation's implementation for publishing to RTD, which is [documented here](https://docs.releng.linuxfoundation.org/projects/lfdocs-conf/en/latest/).

I have not formally documented the usage requirements other than the commands to run to build and lint the docs.  In general, the build process uses the `sphinx-build` command behind the scenes.  Please consider creating a pull request to improve this README if/when you start contributing to this documentation.  Thanks...

## Building the docs

Build the docs static site.
```
$ tox -e docs
```
This command will populate a static website under the folder `_build/html`.


## Running the linter

In addition to building, we can and should run a linter against the content.
```
$ tox -e docs-linkcheck
```
