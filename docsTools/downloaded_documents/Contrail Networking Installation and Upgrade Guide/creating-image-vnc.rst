Creating an Image for a Project in OpenStack Contrail
=====================================================

 

To specify an image to upload to the Image Service for a project in your
system by using the OpenStack dashboard:

1. In OpenStack, select **Project > Compute > Images**. The Images
   window is displayed. See
   `Figure 1 <creating-image-vnc.html#images>`__.

   |Figure 1: OpenStack Images Window|

2. Make sure you have selected the correct project to which you are
   associating an image.

3. Click **Create Image**.

   The **Create An Image** window is displayed. See
   `Figure 2 <creating-image-vnc.html#create-image>`__.

   |Figure 2: OpenStack Create An Image Window|

4. Complete the fields to specify your image.
   `Table 1 <creating-image-vnc.html#images-fields>`__ describes each of
   the fields on the window.\ **Note**\ 

   Only images available through an HTTP URL are supported, and the
   image location must be accessible to the Image Service. Compressed
   image binaries are supported (``*.zip`` and ``*.tar.gz``).

   Table 1: Create an Image Fields

   .. raw:: html

      <table data-cellspacing="0" style="border-top:thin solid black;" width="99%">
      <colgroup>
      <col style="width: 50%" />
      <col style="width: 50%" />
      </colgroup>
      <thead>
      <tr class="header">
      <th style="text-align: left;"><p>Field</p></th>
      <th style="text-align: left;"><p>Description</p></th>
      </tr>
      </thead>
      <tbody>
      <tr class="odd">
      <td style="text-align: left;"><p><strong>Name</strong></p></td>
      <td style="text-align: left;"><p>Enter a name for this image.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p><strong>Description</strong></p></td>
      <td style="text-align: left;"><p>Enter a description for the image.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p><strong>Image Source</strong></p></td>
      <td style="text-align: left;"><p>Select <strong>Image File</strong> or <strong>Image Location</strong>.</p>
      <p>If you select <strong>Image File</strong>, you are prompted to browse to the local location of the file.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p><strong>Image Location</strong></p></td>
      <td style="text-align: left;"><p>Enter an external HTTP URL from which to load the image. The URL must be a valid and direct URL to the image binary. URLs that redirect or serve error pages result in unusable images.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p><strong>Format</strong></p></td>
      <td style="text-align: left;"><p>Required field. Select the format of the image from a list:<br />
      AKI– Amazon Kernel Image<br />
      AMI– Amazon Machine Image<br />
      ARI– Amazon Ramdisk Image<br />
      ISO– Optical Disk Image<br />
      QCOW2– QEMU Emulator<br />
      Raw– An unstructured image format<br />
      VDI– Virtual Disk Imade<br />
      VHD– Virtual Hard Disk<br />
      VMDK– Virtual Machine Disk<br />
      </p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p><strong>Architecture</strong></p></td>
      <td style="text-align: left;"><p>Enter the architecture.</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p><strong>Minimum Disk (GB)</strong></p></td>
      <td style="text-align: left;"><p>Enter the minimum disk size required to boot the image. If you do not specify a size, the default is 0 (no minimum).</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p><strong>Minimum Ram (MB)</strong></p></td>
      <td style="text-align: left;"><p>Enter the minimum RAM required to boot the image. If you do not specify a size, the default is 0 (no minimum).</p></td>
      </tr>
      <tr class="odd">
      <td style="text-align: left;"><p><strong>Public</strong></p></td>
      <td style="text-align: left;"><p>Select this check box if this is a public image. Leave unselected for a private image.</p></td>
      </tr>
      <tr class="even">
      <td style="text-align: left;"><p><strong>Protected</strong></p></td>
      <td style="text-align: left;"><p>Select this check box for a protected image.</p></td>
      </tr>
      </tbody>
      </table>

5. When you are finished, click **Create Image**.

 

.. |Figure 1: OpenStack Images Window| image:: images/s018516.png
.. |Figure 2: OpenStack Create An Image Window| image:: images/s018515.png
