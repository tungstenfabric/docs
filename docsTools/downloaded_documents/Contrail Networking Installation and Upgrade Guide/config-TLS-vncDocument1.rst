Configuring Transport Layer Security-Based XMPP in Contrail
===========================================================

 

Overview: TLS-Based XMPP
------------------------

Transport Layer Security (TLS)-based XMPP can be used to secure all
Extensible Messaging and Presence Protocol (XMPP)-based communication
that occurs in the Contrail environment.

Secure XMPP is based on RFC 6120, Extensible Messaging and Presence
Protocol (XMPP): Core.

TLS XMPP in Contrail
~~~~~~~~~~~~~~~~~~~~

In the Contrail environment, the Transport Layer Security (TLS) protocol
is used for certificate exchange, mutual authentication, and negotiating
ciphers to secure the stream from potential tampering and eavesdropping.

The RFC 6120 highlights a basic stream message exchange format for TLS
negotiation between an XMPP server and an XMPP client.

**Note**

Simple Authentication and Security Layer (SASL) authentication is not
supported in the Contrail environment.

Configuring XMPP Client and Server in Contrail
----------------------------------------------

In the Contrail environment, XMPP based communications are used in
client and server exchanges, between the compute node (as the XMPP
client), and:

-  the control node (as the XMPP server)

-  the DNS server (as the XMPP server)

Configuring Control Node for XMPP Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable secure XMPP, the following parameters are configured at the
XMPP server.

| On the control node, enable the parameters in the configuration file:
| ``/etc/contrail/contrail-control.conf``.

.. raw:: html

   <table data-cellspacing="0" style="border-top:thin solid black;" width="99%">
   <colgroup>
   <col style="width: 33%" />
   <col style="width: 33%" />
   <col style="width: 33%" />
   </colgroup>
   <thead>
   <tr class="header">
   <th style="text-align: left;"><p>Parameter</p></th>
   <th style="text-align: left;"><p>Description</p></th>
   <th style="text-align: left;"><p>Default</p></th>
   </tr>
   </thead>
   <tbody>
   <tr class="odd">
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">xmpp_server_cert</code></p></td>
   <td style="text-align: left;"><p>Path to the node's public certificate</p></td>
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">/etc/contrail/ssl/certs/server.pem</code></p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">xmpp_server_key</code></p></td>
   <td style="text-align: left;"><p>Path to server's or node's private key</p></td>
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">/etc/contrail/ssl/private/server-privkey.pem</code></p></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">xmpp_ca_cert</code></p></td>
   <td style="text-align: left;"><p>Path to CA certificate</p></td>
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">/etc/contrail/ssl/certs/ca-cert.pem</code></p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">xmpp_auth_enable=true</code></p></td>
   <td style="text-align: left;"><p>Enables SSL based XMPP</p></td>
   <td style="text-align: left;"><p>Default is set to false, XMPP is disabled.</p>
   <p><strong>Note:</strong> The keyword <code class="inline" data-v-pre="">true</code> is case sensitive.</p></td>
   </tr>
   </tbody>
   </table>

Configuring DNS Server for XMPP Server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable secure XMPP, the following parameters are configured at the
XMPP DNS server.

| On the DNS server control node, enable the parameters in the
  configuration file:
| ``/etc/contrail/contrail-control.conf``

.. raw:: html

   <table data-cellspacing="0" style="border-top:thin solid black;" width="99%">
   <colgroup>
   <col style="width: 33%" />
   <col style="width: 33%" />
   <col style="width: 33%" />
   </colgroup>
   <thead>
   <tr class="header">
   <th style="text-align: left;"><p>Parameter</p></th>
   <th style="text-align: left;"><p>Description</p></th>
   <th style="text-align: left;"><p>Default</p></th>
   </tr>
   </thead>
   <tbody>
   <tr class="odd">
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">xmpp_server_cert</code></p></td>
   <td style="text-align: left;"><p>Path to the node's public certificate</p></td>
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">/etc/contrail/ssl/certs/server.pem</code></p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">xmpp_server_key</code></p></td>
   <td style="text-align: left;"><p>Path to server's/node's private key</p></td>
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">/etc/contrail/ssl/certs/server-privkey.pem</code></p></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">xmpp_ca_cert</code></p></td>
   <td style="text-align: left;"><p>Path to CA certificate</p></td>
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">/etc/contrail/ssl/certs/ca-cert.pem</code></p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">xmpp_dns_auth_enable=true</code></p></td>
   <td style="text-align: left;"><p>Enables SSL based XMPP</p></td>
   <td style="text-align: left;"><p>Default is set to false, XMPP is disabled.</p>
   <p><strong>Note:</strong> The keyword <code class="inline" data-v-pre="">true</code> is case sensitive.</p></td>
   </tr>
   </tbody>
   </table>

Configuring Control Node for XMPP Client
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To enable secure XMPP, the following parameters are configured at the
XMPP client.

| On the compute node, enable the parameters in the configuration file:
| ``/etc/contrail/contrail-vrouter-agent.conf``

.. raw:: html

   <table data-cellspacing="0" style="border-top:thin solid black;" width="99%">
   <colgroup>
   <col style="width: 33%" />
   <col style="width: 33%" />
   <col style="width: 33%" />
   </colgroup>
   <thead>
   <tr class="header">
   <th style="text-align: left;"><p>Parameter</p></th>
   <th style="text-align: left;"><p>Description</p></th>
   <th style="text-align: left;"><p>Default</p></th>
   </tr>
   </thead>
   <tbody>
   <tr class="odd">
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">xmpp_server_cert</code></p></td>
   <td style="text-align: left;"><p>Path to the node's public certificate</p></td>
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">/etc/contrail/ssl/certs/server.pem</code></p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">xmpp_server_key</code></p></td>
   <td style="text-align: left;"><p>Path to server's/node's private key</p></td>
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">/etc/contrail/ssl/private/server-privkey.pem</code></p></td>
   </tr>
   <tr class="odd">
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">xmpp_ca_cert</code></p></td>
   <td style="text-align: left;"><p>Path to CA certificate</p></td>
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">/etc/contrail/ssl/certs/ca-cert.pem</code></p></td>
   </tr>
   <tr class="even">
   <td style="text-align: left;"><p><code class="inline" data-v-pre="">xmpp_auth_enable=true  xmpp_dns_auth_enable=true</code></p></td>
   <td style="text-align: left;"><p>Enables SSL based XMPP</p></td>
   <td style="text-align: left;"><p>Default is set to false, XMPP is disabled.</p>
   <p><strong>Note:</strong> The keyword <code class="inline" data-v-pre="">true</code> is case sensitive.</p></td>
   </tr>
   </tbody>
   </table>

 
