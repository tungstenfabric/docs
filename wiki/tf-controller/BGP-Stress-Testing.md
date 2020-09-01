scons -u --optimization=production src/bgp:bgp_stress_test

build/production/test/bgp_stress_test -help

**BgpStressTest**

Use this test to stress test control-node in unit-test environment by feeding various test events randomly.

Many events are supported such as add bgp route, add xmpp route, bring up/down bgp/xmpp peer, etc.

By default, test feeds events randomly. To reproduce crashes, events can be fed through a file (- for stdin). Simply grep "Feed " from the test output, and feed those lines back to replay the events.

Events can be retrieved from core-file generated from bgp_stress_test using this bash function.

```
get_events () { # Input is the core file
   gdb --batch --eval-command="print BgpStressTestEvent::d_events_played_list_" build/debug/bgp/test/bgp_stress_test $1 | \grep \$1 | sed 's/",\?/\n/g' | \grep Feed
}
Those events can be played back as shown below.
    get_events() <core-file> | build/debug/bgp/test/bgp_stress_test --feed-events -
```
Scaling
=======
Tweak nagents, npeers, nroutes, ninstances, ntargets as desired
```
Use --no-agents-updates-processing option
Tune following environment variables: e.g.
TCP_SESSION_SOCKET_BUFFER_SIZE=65536 CONCURRENCY_CHECK_DISABLE=TRUE BGP_KEEPALIVE_SECONDS=30000 XMPP_KEEPALIVE_SECONDS=30000 CONTRAIL_UT_TEST_TIMEOUT=3000 WAIT_FOR_IDLE=320 TASK_UTIL_WAIT_TIME=10000 TASK_UTIL_RETRY_COUNT=250000 BGP_STRESS_TEST_SUITE=1 NO_HEAPCHECK=TRUE LOG_DISABLE=TRUE
Usage:
  --help                                produce help message
  --db-walker-wait-usecs arg (=0)       set usecs delay in walker cb
  --close-from-control-node             Initiate xmpp session close from 
                                        control-node
  --event-proportion arg (=0)           Proportion of objects for event feed, 
                                        such as 0.10
  --feed-events arg                     Input file with a list of events to 
                                        feed, Use - for stdin
  --http-port arg                       set http introspect server port number
  --instance-name arg                   set instance name string start
  --log-category arg                    set log category
  --log-disable                         Disable logging
  --log-file arg (=<stdout>)            Filename for the logs to be written to
  --log-file-index arg (=10)            Maximum log file roll over index
  --log-file-uniquefy                   Use pid to make log-file name unique
  --log-file-size arg (=1073741824)     Maximum size of the log file
  --log-level arg (=SYS_DEBUG)          set log level 
  --log-local-disable                   Disable local logging
  --log-trace-enable                    Enable logging traces
  --nagents arg (=1)                    set number of xmpp agents
  --nevents arg (=50)                   set number of random events to feed, 0 
                                        for infinity
  --ninstances arg (=1)                 set number of routing instances
  --npeers arg (=1)                     set number of bgp peers
  --nroutes arg (=1)                    set number of routes
  --ntargets arg (=1)                   set number of route targets (minium 1)
  --nvms arg (=0)                       set number of VMs (for configuration 
                                        download)
  --no-multicast                        Do not add multicast routes
  --no-inet6                            Do not add ipv6 routes
  --no-verify-routes                    Do not verify routes
  --no-agents-updates-processing        Do not store updates received by the 
                                        mock agents
  --no-agents-messages-processing       Do not process messages received by the
                                        mock agents
  --no-sandesh-server                   Do not add multicast routes
  --pause                               Pause after initial setup, before 
                                        injecting events
  --profile-heap                        Profile heap memory
  --routes-send-trigger arg             File whose presence triggers the start 
                                        of routes sending process
  --wait-for-idle-time arg (=30)        WaitForIdle() wait time, 0 for no wait
  --weight-add-bgp-route arg (=50)      Set ADD_BGP_ROUTE event weight
  --weight-delete-bgp-route arg (=50)   Set DELETE_BGP_ROUTE event weight
  --weight-add-xmpp-routE arg (=70)     Set ADD_XMPP_ROUTE event weight
  --weight-delete-xmpp-route arg (=70)  Set DELETE_XMPP_ROUTE event weight
  --weight-bring-up-xmpp-agent arg (=20)
                                        Set BRING_UP_XMPP_AGENT event weight
  --weight-bring-down-xmpp-agent arg (=20)
                                        Set BRING_DOWN_XMPP_AGENT event weight
  --weight-clear-xmpp-agent arg (=20)   Set CLEAR_XMPP_AGENT event weight
  --weight-subscribe-routing-instance arg (=20)
                                        Set SUBSCRIBE_ROUTING_INSTANCE event 
                                        weight
  --weight-unsubscribe-routing-instance arg (=20)
                                        Set UNSUBSCRIBE_ROUTING_INSTANCE event 
                                        weight
  --weight-subscribe-configuration arg (=20)
                                        Set SUBSCRIBE_CONFIGURATION event 
                                        weight
  --weight-unsubscribe-configuration arg (=20)
                                        Set UNSUBSCRIBE_CONFIGURATION event 
                                        weight
  --weight-add-bgp-peer arg (=10)       Set ADD_BGP_PEER event weight
  --weight-delete-bgp-peer arg (=10)    Set DELETE_BGP_PEER event weight
  --weight-clear-bgp-peer arg (=20)     Set CLEAR_BGP_PEER event weight
  --weight-add-routing-instance arg (=30)
                                        Set ADD_ROUTING_INSTANCE event weight
  --weight-delete-routing-instance arg (=30)
                                        Set DELETE_ROUTING_INSTANCE event 
                                        weight
  --weight-add-route-target arg (=10)   Set ADD_ROUTE_TARGET event weight
  --weight-delete-route-target arg (=10)
                                        Set DELETE_ROUTE_TARGET event weight
  --weight-change-socket-buffer-size arg (=10)
                                        Set CHANGE_SOCKET_BUFFER_SIZE event 
                                        weight
  --weight-show-all-routes arg (=10)    Set SHOW_ALL_ROUTES event weight
  --test-id arg (=0)                    set start xmpp agent id <0 - 15>
  --xmpp-nexthop arg                    set xmpp route nexthop IP address
  --xmpp-nexthop-vary                   Vary nexthop advertised for each route
  --xmpp-port arg                       set xmpp server port number
  --xmpp-prefix arg                     set xmpp route IP prefix start
  --xmpp-prefix-format-large            Support large number routes per agent 
                                        (4K - 1), 1024 otherwise
  --xmpp-server arg (=127.0.0.1)        set xmpp server IP address
  --xmpp-source arg (=127.0.0.1)        set xmpp connection source IP address
  --xmpp-auth-enabled                   Enable/Disable Xmpp Authentication
```
## Notes from performance/scale testing
1. Majority of the time, CPU cycles were spent either during xml generation at control-node or received xml parsing in mock agents (Verified by gprof)
2. Most of the xml parsing cycles in boost/pugi xml and regex parse code
3. If generated xml is not parsed (--no-agents-updates-processing), tests run almost 10 times faster. Since one bgp_stress_test process simultes 100s of agents on a single system, they are starved for CPUs (Confirmed by top output, most of the CPUs were running at more than 70%)
4. Since this test only scenario, one can use --no-agents-updates-processing and get around this bottle-neck backtrace at random times initially indicated lot of time spent in MergeUpdate(). After test was modified to first subscribe, wait and then start advertising, this went away, though the time taken for the entire test remained roughly the same.
5. As gprof indicated, most of the time is spent in crunching either generating xmls or parsing received xml. More of the latter, as number of routes received is O(nagents^2)
6. Also ran the test under valgrind (with lesser scale) and did not find any issue or memory leak
7. Ran with larger socket buffer (64K) which resulted in 5% or so improvement only (Default sizes are in /proc/sys/net/ipv4/tcp_rmem and /proc/sys/net/ipv4/tcp_wmem)

## Future considerations
1. If deemed necessary, optimize xml parsing code in production code
2. Tweak scheduler policy to better parallelization across mock agents' IO and xmpp_state_machine tasks
3. Apply info gained here in Becca's scale test (which is now already under QA) In there, multiple bgp_stress_test instances can be run in different test server systems

## Test enhancements (TODO, Not prioritized)
1. Add more features to get more coverage
    1. Static routes
    2. Service Chanining
    3. Feed config through ifmap (Code is there)
    4. EVPN
    5. Multicast, etc.
2. Treshold to test data set to avoid it getting too low (Though adds and deletes are generated randomly)
3. Do not advertise every agent route to every other agent, by not subscribing every agent to every instance. Use a configurable percentag instead

## gperf analysis
```
time   seconds   seconds    calls  ms/call  ms/call  name
 25.76      0.34     0.34  3080544     0.00     0.00  pugi::impl::(anonymous namespace)::append_node(pugi::xml_node_struct*, pugi::impl::(anonymous namespace)::xml_allocator&, pugi::xml_node_type)
  8.71      0.46     0.12    27635     0.00     0.01  boost::re_detail::perl_matcher<__gnu_cxx::__normal_iterator<char const*, std::string>, std::allocator<boost::sub_match<__gnu_cxx::__normal_iterator<char const*, std::string> > >, boost::regex_traits<char, boost::cpp_regex_traits<char> > >::find_restart_any()
  5.30      0.53     0.07     5619     0.01     0.07  pugi::xml_document::load_buffer_impl(void*, unsigned long, unsigned int, pugi::xml_encoding, bool, bool)
  3.79      0.58     0.05 10010160     0.00     0.00  boost::re_detail::perl_matcher<__gnu_cxx::__normal_iterator<char const*, std::string>, std::allocator<boost::sub_match<__gnu_cxx::__normal_iterator<char const*, std::string> > >, boost::regex_traits<char, boost::cpp_regex_traits<char> > >::match_all_states()
  3.79      0.63     0.05    64467     0.00     0.00  autogen::EntryType::XmlParse(pugi::xml_node const&)
  3.79      0.68     0.05    26594     0.00     0.01  XmppSession::Match(boost::asio::const_buffer, int*, bool)
  3.03      0.72     0.04   157975     0.00     0.00  autogen::NextHopType::XmlParse(pugi::xml_node const&)
  2.27      0.75     0.03    64502     0.00     0.00  autogen::NextHopListType::XmlParse(pugi::xml_node const&)
  2.27      0.78     0.03     4507     0.01     0.01  UpdateQueue::Enqueue(RouteUpdate*)
  1.89      0.80     0.03 10031767     0.00     0.00  boost::re_detail::perl_matcher<__gnu_cxx::__normal_iterator<char const*, std::string>, std::allocator<boost::sub_match<__gnu_cxx::__normal_iterator<char const*, std::string> > >, boost::regex_traits<char, boost::cpp_regex_traits<char> > >::match_startmark()
  1.52      0.82     0.02 10030374     0.00     0.00  boost::re_detail::perl_matcher<__gnu_cxx::__normal_iterator<char const*, std::string>, std::allocator<boost::sub_match<__gnu_cxx::__normal_iterator<char const*, std::string> > >, boost::regex_traits<char, boost::cpp_regex_traits<char> > >::match_literal()
  1.52      0.84     0.02 10008249     0.00     0.00  boost::re_detail::perl_matcher<__gnu_cxx::__normal_iterator<char const*, std::string>, std::allocator<boost::sub_match<__gnu_cxx::__normal_iterator<char const*, std::string> > >, boost::regex_traits<char, boost::cpp_regex_traits<char> > >::match_prefix()
  1.52      0.86     0.02  6981105     0.00     0.00  pugi::xml_node::next_sibling() const
  1.52      0.88     0.02   158205     0.00     0.00  autogen::TunnelEncapsulationListType::XmlParse(pugi::xml_node const&)
[..clipped..]
```

### Sample Usage for xmpp peering with external control-node

```
Steps for installing and running bgp stress test from docker.

1. docker pull opencontrail/bgp_stress_test:ubuntu_14.04.5_R4.1

2. Add secondary ip address on data/control interface based on the
xmpp_source parameter which will be passed for running bgp_stress_test ,
If nagents is 5 as shown in example below , need to add secondary address
on the host data/ctrl interface for (xmpp-source : 117.0.0.1/2/3/4/5)

3. Networks with name block1_n1 , block1_n2 , block1_n3 , block1_n4 ,
block1_n5 needs to be created under default-project:admin prior to
executing docker run command

4. docker run -it --privileged --net=host
opencontrail/bgp_stress_test:ubuntu_14.04.5_R4.1 --no-multicast
--xmpp-port=5269 --xmpp-server=5.5.5.129 --xmpp-source=117.0.0.1
--ninstances=5 --instance-name=block1_n --test-id=2 --nagents=5
--nroutes=10 --xmpp-nexthop=192.168.200.8
--no-agents-messages-processing --no-agents-updates-processing
--log-level=SYS_EMERG --log-local --no-verify-routes --no-sandesh-server
--nvms=0 --nevents=-1 --pause --log-file=logs/bgp_stress_6350.log.1

Or with auth-enabled, use this

docker run -v /root/server.pem:/controller/src/xmpp/testdata/server-build02.pem 
-v /root/server-privkey.pem:/controller/src/xmpp/testdata/server-build02.key -it
--privileged --net=host opencontrail/bgp_stress_test:ubuntu_14.04.5_R4.1 --no-multicast
--xmpp-port=5269 --xmpp-server=10.183.10.11 --xmpp-source=192.168.10.1 --ninstances=1
--instance-name=block1_n --test-id=2 --nagents=1 --nroutes=1000 --xmpp-nexthop=192.168.200.8
--no-agents-messages-processing --no-agents-updates-processing --log-level=SYS_EMERG
--log-local --no-verify-routes --no-sandesh-server --nvms=0 --nevents=-1 --pause
--xmpp-auth-enabled  --log-file=logs/bgp_stress_6350.log.1



Above example creates 5 agents having 5 routing instances each and
advertising 10 prefixes for each routing instances , in total 250 routes
will be advertised .

Another docker needs to be launched if more than 60 agents needs to
configured.

Parameters can be varied to get more scale numbers .

```