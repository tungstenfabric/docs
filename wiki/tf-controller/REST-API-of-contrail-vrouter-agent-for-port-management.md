# 1 Port
## 1.1 Create/Update port

#### POST URL
http://<vrouter>:9091/port

JSON data
```
{
  "type": <(integer) 0: VMI, 1: Namespace port, 2: ESXi port>,
  "id": <(string) VMI UUID>,
  "instance-id": <(string) VM UUID>,
  "display-name": <(string) VM display name>,
  "ip-address": <(string) The IP address provided by DHCP or "0.0.0.0">,
  "ip6-address": <(string) IPv6 address or empty>,
  "rx-vlan-id": <(integer) RX VLAN ID for ESXi port or -1>,
  "tx-vlan-id": <(integer) TX VLAN ID for ESXi port or -1>,
  "vn-id": <(string) virtual network UUID>,
  "vm-project-id": <(string) VM's project UUID or empty>,
  "mac-address": <(string) MAC address>,
  "system-name": <(string) interface name on the host>
}
```

Here is an example for VM port.
```
{
  "type": 0,
  "id": "753a65ef-918a-4193-9266-dc23ed8a5982",
  "instance-id": "63bd1a8a-ba6a-4547-af8d-653dd8ff397e",
  "display-name": "vm1",
  "ip-address": "0.0.0.0",
  "ip6-address": "",
  "rx-vlan-id": -1,
  "tx-vlan-id": -1,
  "vn-id": "38ced7ff-fdfc-4f17-9547-17ff4fb45da9",
  "vm-project-id": "",
  "mac-address": "02:75:3a:65:ef:91",
  "system-name": "tab-1234"
}
```

Here is an example for ESXi port.
```
{
  "type": 2,
  "id": "753a65ef-918a-4193-9266-dc23ed8a5982",
  "instance-id": "63bd1a8a-ba6a-4547-af8d-653dd8ff397e",
  "display-name": "vm1",
  "ip-address": "11.0.0.11",
  "ip6-address": "None",
  "rx-vlan-id": 1999,
  "tx-vlan-id": 2000,
  "vn-id": "38ced7ff-fdfc-4f17-9547-17ff4fb45da9",
  "vm-project-id": "cb33cc2c-6fb8-4072-a112-77547c60d2b7",
  "mac-address": "02:75:3a:65:ef:91",
  "system-name": "753a65ef-918a-4193-9266-dc23ed8a5981"
}
```

Example with curl.
```
curl -X POST -H "Content-Type: application/json" -d '
{
  "ip-address": "11.0.0.11",
  "rx-vlan-id": 1999,
  "display-name": "vm1",
  "id": "753a65ef-918a-4193-9266-dc23ed8a5982",
  "instance-id": "63bd1a8a-ba6a-4547-af8d-653dd8ff397e",
  "ip6-address": "None",
  "tx-vlan-id": 2000,
  "vn-id": "38ced7ff-fdfc-4f17-9547-17ff4fb45da9",
  "vm-project-id": "cb33cc2c-6fb8-4072-a112-77547c60d2b7",
  "type": 2,
  "mac-address": "02:75:3a:65:ef:91",
  "system-name": "753a65ef-918a-4193-9266-dc23ed8a5981"
}'  http://localhost:9091/port
```

Multiple ports
```
[
  {
    ......
  },
  {
    ......
  }
]
```

## 1.2 Synchronize port

#### POST URL
http://<vrouter>:9091/syncports

This is used for syncing of ports between plug-in (REST client) and agent across plug-in restarts. Typically, when plug-in (client) restarts, it issues this command and then issues adds for ports using the above (item number 1) API. Agent, upon receiving this command starts a timer. It expects plug-in to replay all ports before the expiry of this timer.  On expiry of timer, agent will remove all ports which have not been added by plug-in after issue of syncports command.

The timeout value of this timer is configurable in contrail-vrouter-agent config file. The configration parameter is stale_interface_cleanup_timeout under DEFAULT section. The value is set in seconds.

Example
```
curl -X POST http://localhost:9091/syncports
```

## 1.3 Get port
 
#### GET URL
http://<vrouter>:9091/port/uuid

Example:
```
curl -X GET http://localhost:9091/port/753a65ef-918a-4193-9266-dc23ed8a5982
```

## 1.4 Delete port

#### DELETE URL
http://<vrouter>:9091/port/uuid

Example
```
curl -X DELETE http://localhost:9091/port/753a65ef-918a-4193-9266-dc23ed8a5982
```

# 2 VM
