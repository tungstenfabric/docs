Sample Network Configuration for Devices for Simple Tiered Web Application
==========================================================================

 

This section shows sample device configurations that can be used to
create the `Example: Deploying a Multi-Tier Web
Application <../task/configuration/web-use-case-vnc.html>`__.
Configurations are shown for Juniper Networks devices: two MX80s and one
EX4200.

*MX80-1 Configuration*

.. raw:: html

   <div id="jd0e24" class="example" dir="ltr">

.. raw:: html

   <div class="statement" style="display:block;">

version 12.2R1.3;

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

system {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

root-authentication {

.. raw:: html

   </div>

encrypted-password "xxxxxxxxxx"; ## SECRET-DATA

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

services {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

ssh {

.. raw:: html

   </div>

root-login allow;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

syslog {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

user \* {

.. raw:: html

   </div>

any emergency;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

file messages {

.. raw:: html

   </div>

any notice;authorization info;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

chassis {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

fpc 1 {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

pic 0 {

.. raw:: html

   </div>

tunnel-services;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

interfaces {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

ge-1/0/0 {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

unit 0 {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

family inet {

.. raw:: html

   </div>

address 10.84.11.253/24;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

ge-1/1/0 {

.. raw:: html

   </div>

description "IP Fabric interface";

.. raw:: html

   <div class="statement" style="display:block;">

unit 0 {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

family inet {

.. raw:: html

   </div>

address 10.84.45.1/24;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

lo0 {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

unit 0 {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

family inet {

.. raw:: html

   </div>

address 127.0.0.1/32;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

routing-options {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

static {

.. raw:: html

   </div>

route 0.0.0.0/0 next-hop 10.84.45.254;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

route-distinguisher-id 10.84.11.253;autonomous-system 64512;

.. raw:: html

   <div class="statement" style="display:block;">

dynamic-tunnels {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

setup1 {

.. raw:: html

   </div>

source-address 10.84.11.253;gre;

.. raw:: html

   <div class="statement" style="display:block;">

destination-networks {

.. raw:: html

   </div>

10.84.11.0/24;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

protocols {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

bgp {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

group mx {

.. raw:: html

   </div>

type internal;local-address 10.84.11.253;

.. raw:: html

   <div class="statement" style="display:block;">

family inet-vpn {

.. raw:: html

   </div>

unicast;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

neighbor 10.84.11.252;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

group contrail-controller {

.. raw:: html

   </div>

type internal;local-address 10.84.11.253;

.. raw:: html

   <div class="statement" style="display:block;">

family inet-vpn {

.. raw:: html

   </div>

unicast;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

neighbor 10.84.11.101;neighbor 10.84.11.102;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

routing-instances {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

customer-public {

.. raw:: html

   </div>

instance-type vrf;interface ge-1/1/0.0;vrf-target target:64512:10000;

.. raw:: html

   <div class="statement" style="display:block;">

routing-options {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

static {

.. raw:: html

   </div>

route 0.0.0.0/0 next-hop 10.84.45.254;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   </div>

*MX80-2 Configuration*

.. raw:: html

   <div id="jd0e265" class="example" dir="ltr">

.. raw:: html

   <div class="statement" style="display:block;">

version 12.2R1.3;

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

system {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

root-authentication {

.. raw:: html

   </div>

encrypted-password "xxxxxxxxx"; ## SECRET-DATA

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

services {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

ssh {

.. raw:: html

   </div>

root-login allow;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

syslog {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

user \* {

.. raw:: html

   </div>

any emergency;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

file messages {

.. raw:: html

   </div>

any notice;authorization info;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

chassis {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

fpc 1 {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

pic 0 {

.. raw:: html

   </div>

tunnel-services;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

interfaces {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

ge-1/0/0 {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

unit 0 {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

family inet {

.. raw:: html

   </div>

address 10.84.11.252/24;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

ge-1/1/0 {

.. raw:: html

   </div>

description "IP Fabric interface";

.. raw:: html

   <div class="statement" style="display:block;">

unit 0 {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

family inet {

.. raw:: html

   </div>

address 10.84.45.2/24;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

lo0 {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

unit 0 {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

family inet {

.. raw:: html

   </div>

address 127.0.0.1/32;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

routing-options {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

static {

.. raw:: html

   </div>

route 0.0.0.0/0 next-hop 10.84.45.254;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

route-distinguisher-id 10.84.11.252;autonomous-system 64512;

.. raw:: html

   <div class="statement" style="display:block;">

dynamic-tunnels {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

setup1 {

.. raw:: html

   </div>

source-address 10.84.11.252;gre;

.. raw:: html

   <div class="statement" style="display:block;">

destination-networks {

.. raw:: html

   </div>

10.84.11.0/24;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

protocols {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

bgp {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

group mx {

.. raw:: html

   </div>

type internal;local-address 10.84.11.252;

.. raw:: html

   <div class="statement" style="display:block;">

family inet-vpn {

.. raw:: html

   </div>

unicast;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

neighbor 10.84.11.253;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

group contrail-controller {

.. raw:: html

   </div>

type internal;local-address 10.84.11.252;

.. raw:: html

   <div class="statement" style="display:block;">

family inet-vpn {

.. raw:: html

   </div>

unicast;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

neighbor 10.84.11.101;neighbor 10.84.11.102;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

routing-instances {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

customer-public {

.. raw:: html

   </div>

instance-type vrf;interface ge-1/1/0.0;vrf-target target:64512:10000;

.. raw:: html

   <div class="statement" style="display:block;">

routing-options {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

static {

.. raw:: html

   </div>

route 0.0.0.0/0 next-hop 10.84.45.254;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   </div>

*EX4200 Configuration*

.. raw:: html

   <div id="jd0e508" class="example" dir="ltr">

.. raw:: html

   <div class="statement" style="display:block;">

system {

.. raw:: html

   </div>

host-name EX4200;time-zone America/Los_Angeles;

.. raw:: html

   <div class="statement" style="display:block;">

root-authentication {

.. raw:: html

   </div>

encrypted-password "xxxxxxxxxxxxx"; ## SECRET-DATA

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

login {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

class read {

.. raw:: html

   </div>

permissions [ clear interface view view-configuration ];

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

user admin {

.. raw:: html

   </div>

uid 2000;class super-user;

.. raw:: html

   <div class="statement" style="display:block;">

authentication {

.. raw:: html

   </div>

encrypted-password "xxxxxxxxxxxx"; ## SECRET-DATA

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

user user1 {

.. raw:: html

   </div>

uid 2002;class read;

.. raw:: html

   <div class="statement" style="display:block;">

authentication {

.. raw:: html

   </div>

encrypted-password "xxxxxxxxxxxxxx"; ## SECRET-DATA

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

services {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

ssh {

.. raw:: html

   </div>

root-login allow;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

telnet;

.. raw:: html

   <div class="statement" style="display:block;">

netconf {

.. raw:: html

   </div>

ssh;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

web-management {

.. raw:: html

   </div>

http;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

syslog {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

user \* {

.. raw:: html

   </div>

any emergency;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

file messages {

.. raw:: html

   </div>

any notice;authorization info;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

file interactive-commands {

.. raw:: html

   </div>

interactive-commands any;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

chassis {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

aggregated-devices {

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

ethernet {

.. raw:: html

   </div>

device-count 64;

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   <div class="statement" style="display:block;">

}

.. raw:: html

   </div>

.. raw:: html

   </div>

 
