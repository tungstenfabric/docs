# Introduction:

Debian related packages are available in debian/ directory. Making debian packages differ for a first time package creation and modifying an existing package. For debian packages we maintain ppa cache which builds the binary debian, based on the source (source.changes) pushed to it. We build the package with pdebuild mainly to capture dependencies before submitting to ppa. Once we are sure with the debian build directory, we make a source package and push to ppa. Following, lists procedure to make a debian directory and test with pdebuilder.

## Adding a new package:

Following are the steps to add new packages to the repo:

1. Get the original source tar.gz file 

2. Uncompress it

3. Make sure the **DEBEMAIL** and **DEBFULLNAME** environment variables are set
    in the shell

4. Debianize the package by going inside the source dir and issuing
    dh_make -f ../pkg-name.tar.gz
    The above command creates a debian folder inside the source and also 
    a orig.tar.gz file. Remove the orig.tar.gz file.
   [If this command complains please use -p <package-name> option to 
   override. For python packages this will be mandatory as they require
   python prefix to the package name.
   Eg., dh_make -p python-consistent-hash -f ../consistent-hash.tar.gz]
   [ For python packages after debianizing using dh_make, follow the links
     in https://wiki.debian.org/Python/Packaging to fix rules and control
     file in case of dependency errors]

5. To make the changes install a tool called quilt and follow setup 
   instructions:<br />
     `alias dquilt="quilt --quiltrc=${HOME}/.quiltrc-dpkg"`<br />
     `complete -F _quilt_completion $_quilt_complete_opt dquilt`<br />

    Create ~/.quiltrc-dpkg file with following instructions:<br />


         d=. ; while [ ! -d $d/debian -a `readlink -e $d` != / ]; do d=$d/..; done
         if [ -d $d/debian ] && [ -z $QUILT_PATCHES ]; then
             # if in Debian packaging tree with unset $QUILT_PATCHES
             QUILT_PATCHES="debian/patches"
             QUILT_PATCH_OPTS="--reject-format=unified"
             QUILT_DIFF_ARGS="-p ab --no-timestamps --no-index --color=auto"
             QUILT_REFRESH_ARGS="-p ab --no-timestamps --no-index"
             QUILT_COLORS="diff_hdr=1;32:diff_add=1;34:diff_rem=1;31:diff_hunk=1;33:diff_ctx=35:diff_cctx=33"
             if ! [ -d $d/debian/patches ]; then mkdir $d/debian/patches; fi
         fi

6. Making changes to the package using quilt at a high level involves,
     1. Creating debian/patches folder (if it does not exist)
     2. Create a new patch file using _"dquilt new patch-name.patch"_
     3. Add the file names that have to be modified using dquilt,
            _"dquilt add debian/rules"_
     4. Issue _"dquilt refresh"_ to capture all the changes in the patch
            file
     5. Describe the patch using _"dquilt header -e"_

7. After making the changes include the revision number 1contrail1
   by issuing _"dch -v version-revision"_ eg., "dch -v 1.3.1-1contrail1"

8. Include a target for this package in the Makefile. We use pbuilder
   to build the package in a chroot environment. Here is a overview of 
   steps in making the package:

       1. Copy the folder to BUILD directory outside the git repository
       2. Create orig.tar.gz file from the package directory after
          removing the patches folder inside the pkg_name/debian
       3. Invoke "sudo pdebuild --use-pdebuild-internal --debbuildopts -tc"
          to build the package.

9. Issue _"make target"_ to make sure the package 
   builds with your changes.
   If successful this generates the following:

       ~/BUILD/pkgname/pkg-name_version-revision.dsc (referred as the src pkg)<br />
       ~/BUILD/pkgname/pkg-name_version-revision.debian.tar.gz (just the debian folder)<br />
       ~/BUILD/pkgname/pkg-name_version-revision_arch.deb (binary)<br />
       ~/BUILD/pkgname/pkg-name_version-revision_arch.changes<br />

10. Commit the SB/upstream/debian/<pkg-name>/<pkg-name-version> folder to github

11. To push the package to ppa please refer to the packaging section. This is needed for
    contrail builds to pick your package. 

## Modifying an existing package:

1. check out the third party repo, and go to the **upstream/debian/package-name**

2. It should contain package-name-version folder

3. Follow step 6 in "Adding a new package section" to make the
   changes to the current package

4. After testing out the package change the revision of the 
   package by modifying the changelog file or by issuing 
       "dch -v <version-revision>"
       where version is the upstream version number
       and revision is the new revision viz., 1contrail2

5. Commit the SB/upstream/debian/<pkg-name>/<pkg-name-version> folder to github
   if make <target> succeeds.

## Uploading package to PPA:

When the newly created package is tested it has to be uploaded to ppa.Before uploading files to PPA create GPG certificate. 
Create a PGP key following this link https://help.ubuntu.com/community/GnuPrivacyGuardHowto
Set the shell variable, DEBSIGN_KEYID=Your_GPG_keyID </br>

First build the package using pbuilder to capture any dependencies involved. Directly doing a "debuild" will not capture dependecies. </br>

For the below step, its highly recommended to first test by pushing the source.changes file to your private PPA before attempting to push it to contrail-ppa [ppa requires each new push to it have a higher version than previous, hence the 
recommendation]

Here are the steps to upload a package:

1. Checkout the repository 
2. Issue _"make target"_.
3. If build is successful, files will be available in SB/../BUILD/target-name/ 
4. Extract the orig.tgz file and place the working debian directory inside it.
5. Build the source package by issuing following command inside the source directory, "debuild -S -sa"
6. The above step should ask you to sign the package. If successful it generates a <pkg-name>.source.changes file
   outside the directory. [Refer https://help.launchpad.net/Packaging/PPA/BuildingASourcePackage, for help]
7. upload the above source.changes to PPA, with
   dput ppa:opencontrail/ppa <source.changes>

## FAQ:
*  Patches don't work with quilt. However manually patching a diff works ?
   Try changing the debian/sources/format 3.0 native.(Its quilt alternative)
* Dependencies not available in the repo listed in sources.list of the builder venv?
   You can add a new repo from which the dependency can be downloaded. Try looking at
   the package built with ./utils/pbuilderrc-cloud. We add a new repo.