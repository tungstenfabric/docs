Encryption Between Analytics API Servers and Client Servers
===========================================================

 

Contrail Networking Release 1910 supports SSL encryption for the
connection between Analytics API servers and Client servers. The Client
servers are Service Monitor and Contrail Command, which connects to the
Analytics API server through the REST API Port. In releases prior to
release 1910, the connection between Analytics API servers and the
Client servers was not encrypted, which could pose a security threat.

SSL encryption is supported in Contrail Networking Release 1910 only
when Contrail Networking is deployed with Red Hat OpenStack Platform
(RHOSP). In the RHOSP deployment, a global flag is added, which
determines the status of the SSL encryption.

If the global flag is enabled:

-  You do not have to modify the configuration files as SSL encryption
   is automatically enabled.

-  You must modify the configuration files if you want to disable SSL
   encryption.

If the global flag is disabled:

-  You do not have to modify the configuration files as SSL encryption
   is automatically disabled.

-  You cannot enable SSL encryption, even if you modify the
   configuration files. The certificates are not generated during
   deployment as the global flag is disabled.

The configuration files are contrail-analytics-api.conf,
contrail-svc-monitor.conf, and command_servers.yml. In the configuration
files, modify the following parameters in the
`Table 1 <encrypting-connection-analytics-server-and-client-server.html#ssl-parameter>`__
below to enable or disable SSL based encryption:

Table 1: SSL Encryption Parameters

.. raw:: html

   <table data-cellspacing="0" style="border-top:thin solid black;" width="99%">
   <colgroup>
   <col style="width: 33%" />
   <col style="width: 33%" />
   <col style="width: 33%" />
   </colgroup>
   <thead>
   <tr class="header">
   <th style="text-align: left;"><p>Parameters</p></th>
   <th style="text-align: left;"><p>Description</p></th>
   <th style="text-align: left;"><p>Default</p></th>
   </tr>
   </thead>
   <tbody>
   <tr class="odd">
   <td style="text-align: left;"><p>analytics_api_ssl_enable</p></td>
   <td style="text-align: left;"><p>Enables or disables support for SSL encryption between Analytics API server and Client server.</p></td>
   <td style="text-align: left;"><p>If the value is assigned <kbd class="user-typing" data-v-pre="">TRUE</kbd>: Support for SSL encryption is enabled.</p>
   <p>If the value is assigned <kbd class="user-typing" data-v-pre="">FALSE</kbd>: Support for SSL encryption is not enabled and the Analytics API server does not accept HTTPS requests.</p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p>analytics_api_insecure_enable</p></td>
   <td style="text-align: left;"><p>Enables or disables support for required certificates in HTTPS requests.</p></td>
   <td style="text-align: left;"><p>If the value is assigned <kbd class="user-typing" data-v-pre="">TRUE</kbd>: HTTPS connection is supported without the certificates.</p>
   <p>If the value is assigned <kbd class="user-typing" data-v-pre="">FALSE</kbd>: HTTPS connection is not supported without the certificates.</p></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p>analytics_api_ssl_keyfile</p></td>
   <td style="text-align: left;"><p>Path to the node’s private key.</p></td>
   <td style="text-align: left;"><p><code class="filepath">/etc/contrail/ssl/private/server-privkey.pem</code></p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p>analytics_api_ssl_certfile</p></td>
   <td style="text-align: left;"><p>Path to the node's public certificate.</p></td>
   <td style="text-align: left;"><p><code class="filepath">/etc/contrail/ssl/certs/server.pem</code></p></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p>analytics_api_ssl_ca_cert</p></td>
   <td style="text-align: left;"><p>Path to the CA certificate</p></td>
   <td style="text-align: left;"><p><code class="filepath">/etc/ipa/ca.crt</code></p></td>
   </tr>
   </tbody>
   </table>

Once these parameters are configured, the Analytics API server starts
using SSL certificates, which enables SSL encryption support for
connection between Analytics API servers and Client servers.

.. raw:: html

   <div class="table">

.. raw:: html

   <div class="caption">

Release History Table

.. raw:: html

   </div>

.. raw:: html

   <div class="table-row table-head">

.. raw:: html

   <div class="table-cell">

Release

.. raw:: html

   </div>

.. raw:: html

   <div class="table-cell">

Description

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="table-row">

.. raw:: html

   <div class="table-cell">

`1910 <#jd0e10>`__

.. raw:: html

   </div>

.. raw:: html

   <div class="table-cell">

Contrail Networking Release 1910 supports SSL encryption for the
connection between Analytics API servers and Client servers.

.. raw:: html

   </div>

.. raw:: html

   </div>

.. raw:: html

   </div>

 
