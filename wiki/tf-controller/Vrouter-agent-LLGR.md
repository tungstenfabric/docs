**Agent LLGR has been divided into two parts:**
- On agent restart or new config server selection, end-of-config is determined.
- Agent end-of-rib is computed on restart/channel flaps, new channel connection.
- Route retention from each peer (in old terms headless per peer).
 
**End of Config**
 
Trigger for determination of EOC -
  1) Restart and config channel selection
  2) Channel flaps resulting in selection of new channel as config - End of config is determined for new channel.
  3) New channel configured in agent.conf ( SIGHUP triggering new config to be taken) - New config channel is selected and for same EOC is determined.
      It may so happen same channel is present in new config and is again selected as config channel then agent will do nothing as EOC processing is done or may be in process for same.
 
How EOC is determined
Agent does not have any definite way to know that all config has been received from CN like EOC marker. So there is a heuristic determination of same.
On config channel after connection establishment agent starts a timer (EOC timer). This timer observes if channel is silent for 30 seconds. Silence means that no message is received on
config channel. Internally agent does not directly process any config messages. It enqueues the message to work queue to process it later. This silence observer, also checks if this work queue processing is silent for same period. In summary, channel should not get any message and work queue should remain idle to process EOC for agent.
Processing of EOC results in two operations:
- Stale config cleanup timer (100 seconds) initiated. This timer cleans stale config.
- Process of End of Rib determination
 
There is a fallback logic as well. In case a channel is seeing some incremental config periodically, then after a duration of 15 minutes (older agent stale config cleanup time) end of config is processed.
 
 
**End of RIB (originated from agent)**
 
Trigger - EOC identification.
 
In agent all the config received goes through dependency manager, config manager to create operdb entries. Once oper-db entries are active, then routes are generated. Controller module of agent listens to route update which is in-turn is published to CN. To identify EOR, agent has to wait for all locally generated routes to be published. Again these events in current state are not deterministic like dependency resolution, updates, notification are not ordered. To handle this another timer for EOR.
 
EOR timer:
This also works on silence observation. Here silence is checked for local route published to CN. If there is no local route published for 15 seconds then EOR is sent on this channel.
 
One alternative solution by Praveen is to insert a dummy config element and let it percolate to oper-db. On notification of same assume all oper-db entries are processed. Now start a walk across VRF and at end send EOR. However this or any other enhancement will be taken up later.
 
 
**Route retention**
 
Agent connects to two CN(say CN1 and CN2). If either of this channel or both goes down, agent will retain routes from that channel until channel comes back up and EOR from CN is seen from same. So there are two things to observe here -
- Track channel states
- EOR from CN
 
Stale identification:
Each channel maintains a sequence number. This is incremented whenever channel goes into Ready state. On going to not-ready state nothing is done. Routes received on CN are added as path and each path carries this sequence number. Path is said to be stale if channel sequence number is greater than path’s. Any route update on this channel will update sequence number of path for that peer.
 
Channel states:
Agent for two CN maintains two slots 0 and 1. Any of the channel from configuration can take up this slot. it can be that both these slots are occupied or only one is occupied (in case only one CN is provided).
 
Ready/Not-ready event handling
Whenever channel in occupied slot sees Ready event, it waits for EOR from CN and on receiving it starts a walk to release all stale. When Not-ready is seen agent cancels any stale walk(if in progress) and retains all route.
 
Timed-out event handling
On seeing this event agent pushes this channel to last and iterates over remaining channel to see for another channel. The new channel takes up the slot which was occupied by timed-out channel. In case no other channel is found (in case only 1/2 CN are provided) then timed-out channel continues to exist without flushing its routes. However if there are more than 2 CN there will be some other channel (CN3) selected for this slot. On connecting CN3, timed-out channel routes will be retained till EOR is seen from CN3. Even channel will be retained till EOR as it is the peer for path.
 
contrail-vrouter-agent.conf CN list changed
This will be treated similar to timed-out event. New channels will take up slots and old channels(with paths) for those slots will be retained till EOR is seen from both new channels.
 
**Bug under which feature is covered**
https://bugs.launchpad.net/juniperopenstack/+bug/1659187