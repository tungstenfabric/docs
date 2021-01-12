# Sample Network Configuration for Devices for Simple Tiered Web Application

 

This section shows sample device configurations that can be used to
create the [Example: Deploying a Multi-Tier Web
Application](../task/configuration/web-use-case-vnc.html).
Configurations are shown for Juniper Networks devices: two MX80s and one
EX4200.

*MX80-1 Configuration*

<div id="jd0e24" class="example" dir="ltr">

<div class="statement" style="display:block;">

version 12.2R1.3;

</div>

<div class="statement" style="display:block;">

system {

</div>

<div class="statement" style="display:block;">

root-authentication {

</div>

encrypted-password "xxxxxxxxxx"; \#\# SECRET-DATA

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

services {

</div>

<div class="statement" style="display:block;">

ssh {

</div>

root-login allow;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

syslog {

</div>

<div class="statement" style="display:block;">

user \* {

</div>

any emergency;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

file messages {

</div>

any notice;authorization info;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

chassis {

</div>

<div class="statement" style="display:block;">

fpc 1 {

</div>

<div class="statement" style="display:block;">

pic 0 {

</div>

tunnel-services;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

interfaces {

</div>

<div class="statement" style="display:block;">

ge-1/0/0 {

</div>

<div class="statement" style="display:block;">

unit 0 {

</div>

<div class="statement" style="display:block;">

family inet {

</div>

address 10.84.11.253/24;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

ge-1/1/0 {

</div>

description "IP Fabric interface";

<div class="statement" style="display:block;">

unit 0 {

</div>

<div class="statement" style="display:block;">

family inet {

</div>

address 10.84.45.1/24;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

lo0 {

</div>

<div class="statement" style="display:block;">

unit 0 {

</div>

<div class="statement" style="display:block;">

family inet {

</div>

address 127.0.0.1/32;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

routing-options {

</div>

<div class="statement" style="display:block;">

static {

</div>

route 0.0.0.0/0 next-hop 10.84.45.254;

<div class="statement" style="display:block;">

}

</div>

route-distinguisher-id 10.84.11.253;autonomous-system 64512;

<div class="statement" style="display:block;">

dynamic-tunnels {

</div>

<div class="statement" style="display:block;">

setup1 {

</div>

source-address 10.84.11.253;gre;

<div class="statement" style="display:block;">

destination-networks {

</div>

10.84.11.0/24;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

protocols {

</div>

<div class="statement" style="display:block;">

bgp {

</div>

<div class="statement" style="display:block;">

group mx {

</div>

type internal;local-address 10.84.11.253;

<div class="statement" style="display:block;">

family inet-vpn {

</div>

unicast;

<div class="statement" style="display:block;">

}

</div>

neighbor 10.84.11.252;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

group contrail-controller {

</div>

type internal;local-address 10.84.11.253;

<div class="statement" style="display:block;">

family inet-vpn {

</div>

unicast;

<div class="statement" style="display:block;">

}

</div>

neighbor 10.84.11.101;neighbor 10.84.11.102;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

routing-instances {

</div>

<div class="statement" style="display:block;">

customer-public {

</div>

instance-type vrf;interface ge-1/1/0.0;vrf-target target:64512:10000;

<div class="statement" style="display:block;">

routing-options {

</div>

<div class="statement" style="display:block;">

static {

</div>

route 0.0.0.0/0 next-hop 10.84.45.254;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

</div>

*MX80-2 Configuration*

<div id="jd0e265" class="example" dir="ltr">

<div class="statement" style="display:block;">

version 12.2R1.3;

</div>

<div class="statement" style="display:block;">

system {

</div>

<div class="statement" style="display:block;">

root-authentication {

</div>

encrypted-password "xxxxxxxxx"; \#\# SECRET-DATA

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

services {

</div>

<div class="statement" style="display:block;">

ssh {

</div>

root-login allow;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

syslog {

</div>

<div class="statement" style="display:block;">

user \* {

</div>

any emergency;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

file messages {

</div>

any notice;authorization info;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

chassis {

</div>

<div class="statement" style="display:block;">

fpc 1 {

</div>

<div class="statement" style="display:block;">

pic 0 {

</div>

tunnel-services;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

interfaces {

</div>

<div class="statement" style="display:block;">

ge-1/0/0 {

</div>

<div class="statement" style="display:block;">

unit 0 {

</div>

<div class="statement" style="display:block;">

family inet {

</div>

address 10.84.11.252/24;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

ge-1/1/0 {

</div>

description "IP Fabric interface";

<div class="statement" style="display:block;">

unit 0 {

</div>

<div class="statement" style="display:block;">

family inet {

</div>

address 10.84.45.2/24;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

lo0 {

</div>

<div class="statement" style="display:block;">

unit 0 {

</div>

<div class="statement" style="display:block;">

family inet {

</div>

address 127.0.0.1/32;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

routing-options {

</div>

<div class="statement" style="display:block;">

static {

</div>

route 0.0.0.0/0 next-hop 10.84.45.254;

<div class="statement" style="display:block;">

}

</div>

route-distinguisher-id 10.84.11.252;autonomous-system 64512;

<div class="statement" style="display:block;">

dynamic-tunnels {

</div>

<div class="statement" style="display:block;">

setup1 {

</div>

source-address 10.84.11.252;gre;

<div class="statement" style="display:block;">

destination-networks {

</div>

10.84.11.0/24;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

protocols {

</div>

<div class="statement" style="display:block;">

bgp {

</div>

<div class="statement" style="display:block;">

group mx {

</div>

type internal;local-address 10.84.11.252;

<div class="statement" style="display:block;">

family inet-vpn {

</div>

unicast;

<div class="statement" style="display:block;">

}

</div>

neighbor 10.84.11.253;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

group contrail-controller {

</div>

type internal;local-address 10.84.11.252;

<div class="statement" style="display:block;">

family inet-vpn {

</div>

unicast;

<div class="statement" style="display:block;">

}

</div>

neighbor 10.84.11.101;neighbor 10.84.11.102;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

routing-instances {

</div>

<div class="statement" style="display:block;">

customer-public {

</div>

instance-type vrf;interface ge-1/1/0.0;vrf-target target:64512:10000;

<div class="statement" style="display:block;">

routing-options {

</div>

<div class="statement" style="display:block;">

static {

</div>

route 0.0.0.0/0 next-hop 10.84.45.254;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

</div>

*EX4200 Configuration*

<div id="jd0e508" class="example" dir="ltr">

<div class="statement" style="display:block;">

system {

</div>

host-name EX4200;time-zone America/Los\_Angeles;

<div class="statement" style="display:block;">

root-authentication {

</div>

encrypted-password "xxxxxxxxxxxxx"; \#\# SECRET-DATA

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

login {

</div>

<div class="statement" style="display:block;">

class read {

</div>

permissions \[ clear interface view view-configuration \];

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

user admin {

</div>

uid 2000;class super-user;

<div class="statement" style="display:block;">

authentication {

</div>

encrypted-password "xxxxxxxxxxxx"; \#\# SECRET-DATA

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

user user1 {

</div>

uid 2002;class read;

<div class="statement" style="display:block;">

authentication {

</div>

encrypted-password "xxxxxxxxxxxxxx"; \#\# SECRET-DATA

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

services {

</div>

<div class="statement" style="display:block;">

ssh {

</div>

root-login allow;

<div class="statement" style="display:block;">

}

</div>

telnet;

<div class="statement" style="display:block;">

netconf {

</div>

ssh;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

web-management {

</div>

http;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

syslog {

</div>

<div class="statement" style="display:block;">

user \* {

</div>

any emergency;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

file messages {

</div>

any notice;authorization info;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

file interactive-commands {

</div>

interactive-commands any;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

chassis {

</div>

<div class="statement" style="display:block;">

aggregated-devices {

</div>

<div class="statement" style="display:block;">

ethernet {

</div>

device-count 64;

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

<div class="statement" style="display:block;">

}

</div>

</div>

 
