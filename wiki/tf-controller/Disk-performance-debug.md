## Get Disk Details 
### Installation
* Install smartmontools -  
\# _apt-get install smartmontools_  

### Run application
* Run the smartctl command for the disk  
\# _smartctl -i /dev/sda_   
=== START OF INFORMATION SECTION ===  
Model Family:     Western Digital RE4  
Device Model:     WDC WD1003FBYX-01Y7B1  
Serial Number:    WD-WCAW36246960  
LU WWN Device Id: 5 0014ee 25e1a9182  
Firmware Version: 01.01V02  
User Capacity:    1,000,204,886,016 bytes [1.00 TB]  
Sector Size:      512 bytes logical/physical  
Rotation Rate:    7200 rpm  
Device is:        In smartctl database [for details use: -P show]  
ATA Version is:   ATA8-ACS (minor revision not indicated)  
SATA Version is:  SATA 3.0, 3.0 Gb/s (current: 3.0 Gb/s)  
Local Time is:    Wed Apr 20 13:47:30 2016 PDT  
SMART support is: Available - device has SMART capability.  
SMART support is: Enabled  

* This will provide disk details including make, model number etc. which can be used to cross check whether the device is an SSD or a rotation harddisk.
  
## Disk Performance
### Installation
* Install fio tool - 
\# _apt-get install fio_

### Test Preparation
* Create a test directory /data on the disk where the test to be run

* Create a configuration file for a read or write profile, sample write 4K write configuration below.  
_# Configuration file - randwrite-2M_  
[global]  
directory=/data/  
size=16G  
filesize=16G  
end_fsync=0  
thread  
numjobs=4  
direct=1  
ioengine=libaio  
invalidate=1  
iodepth=32  
norandommap  
time_based  
group_reporting  
runtime=120  
[rw-2M]  
bs=2M  
rw=randwrite

* Currently the configuration file is set to write 16G files with 4 threads, So 64G of free space is required.

* For small size write load reduce the block size from 2M to desired value such as 4K or 32K etc.

* For longer run increase the runtime from 120 (seconds) to the desired value.

* Use rand/seq for random read/sequential read in the rw option instead of randwrite.

### Run Test - 
* Run the test with the fio command as below  
\# fio ranwrite-2M  
The command will trigger the test, currently set to run for 120 seconds, which will give the final output similar to below. 
The output of the command will give the average throughput, IOPs, latency etc.  
Jobs: 4 (f=4): [wwww] [8.8% done] [0KB/16384KB/0KB /s] [0/8/0 iops] [eta 21m:05s]  
rw-2M: (groupid=0, jobs=4): err= 0: pid=31810: Wed Apr 20 12:50:16 2016  
&nbsp;&nbsp;write: io=6948.0MB, bw=58599KB/s, iops=28, runt=121414msec  
&nbsp;&nbsp;&nbsp;&nbsp;slat (usec): min=157, max=2760.6K, avg=139253.59, stdev=382096.14  
&nbsp;&nbsp;&nbsp;&nbsp;clat (msec): min=445, max=10750, avg=4304.73, stdev=1408.87  
&nbsp;&nbsp;&nbsp;&nbsp;lat (msec): min=866, max=10750, avg=4443.98, stdev=1448.41  
&nbsp;&nbsp;&nbsp;&nbsp;clat percentiles (msec):  
&nbsp;&nbsp;&nbsp;&nbsp;|  1.00th=[ 1582],  5.00th=[ 2212], 10.00th=[ 2606], 20.00th=[ 3130],  
&nbsp;&nbsp;&nbsp;&nbsp;| 30.00th=[ 3490], 40.00th=[ 3818], 50.00th=[ 4146], 60.00th=[ 4555],  
&nbsp;&nbsp;&nbsp;&nbsp;| 70.00th=[ 4883], 80.00th=[ 5473], 90.00th=[ 6194], 95.00th=[ 6915],  
&nbsp;&nbsp;&nbsp;&nbsp;| 99.00th=[ 8029], 99.50th=[ 8455], 99.90th=[ 9634], 99.95th=[ 9634],  
&nbsp;&nbsp;&nbsp;&nbsp;| 99.99th=[10814]  
&nbsp;&nbsp;&nbsp;&nbsp;bw (KB  /s): min=  656, max=65536, per=26.83%, avg=15725.03, stdev=9210.85  
&nbsp;&nbsp;&nbsp;&nbsp;lat (msec) : 500=0.12%, 1000=0.09%, 2000=3.60%, >=2000=96.20%  
&nbsp;&nbsp;cpu          : usr=0.10%, sys=0.18%, ctx=661, majf=0, minf=4  
&nbsp;&nbsp;IO depths    : 1=0.1%, 2=0.2%, 4=0.5%, 8=0.9%, 16=1.8%, 32=96.4%, >=64=0.0%  
&nbsp;&nbsp;&nbsp;&nbsp;submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%  
&nbsp;&nbsp;&nbsp;&nbsp;complete  : 0=0.0%, 4=99.9%, 8=0.0%, 16=0.0%, 32=0.1%, 64=0.0%, >=64=0.0%  
&nbsp;&nbsp;&nbsp;&nbsp;issued    : total=r=0/w=3474/d=0, short=r=0/w=0/d=0  
Run status group 0 (all jobs):  
&nbsp;&nbsp;WRITE: io=6948.0MB, aggrb=58599KB/s, minb=58599KB/s, maxb=58599KB/s, mint=121414msec, maxt=121414msec  
Disk stats (read/write):  
&nbsp;&nbsp;&nbsp;&nbsp;dm-0: ios=159/19673, merge=0/0, ticks=159348/22323000, in_queue=22523992, util=100.00%, aggrios=136/16205,  aggrmerge=17/3502, aggrticks=41948/18731944, aggrin_queue=18773972, aggrutil=100.00%  
&nbsp;&nbsp;sda: ios=136/16205, merge=17/3502, ticks=41948/18731944, in_queue=18773972, util=100.00%  

* The bandwidth will give the average disk throughput seen. For Harddisk, it will be around 45-100MB/sec depending upon SATA/SCSI and the rotation speed. For SSD it will be >200MB/sec 
* With the IOPs test, you will see in the order of 100s for Harddisk and for SSD it will be >5000, newer SSDs will have 20K-40K IOPs.
  