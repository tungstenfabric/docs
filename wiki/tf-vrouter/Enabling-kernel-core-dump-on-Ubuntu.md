To enable kernel core dumps on Ubuntu, the following package needs to be installed.

apt-get install linux-crashdump 

In systems with large amounts of memory, /etc/grub.d/10_linux might need to be modified to set crashkernel as below and then update-grub needs to be run.

crashkernel=384M-2G:64M,2G-16G:128M,16G-:256M

update-grub

