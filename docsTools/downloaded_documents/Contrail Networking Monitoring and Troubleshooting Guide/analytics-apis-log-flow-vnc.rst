Log and Flow Information APIs
=============================

 

In Contrail, log and flow analytics information is collected and stored
using a horizontally scalable Contrail collector and NoSQL database. The
``analytics-api``\ server provides REST APIs to extract this information
using queries. The queries use well-known SQL syntax, hiding the
underlying complexity of the NoSQL tables.

HTTP GET APIs
-------------

Use the following GET APIs to identify tables and APIs available for
querying.

``/analytics/tables`` -- lists the SQL-type tables available for
querying, including the hrefs for each of the tables

``/analytics/table/<table>`` -- lists the APIs available to get
information for a given table

``/analytics/table/<table>/schema`` -- lists the schema for a given
table

HTTP POST API
-------------

Use the following POST API information to extract data from a table.

``/analytics/query`` -- format your query using the following SQL
syntax:

-  SELECT ``field1, field2`` ...

-  FROM ``table1``

-  WHERE ``field1`` = ``value1`` AND ``field2`` = ``value2`` ...

-  FILTER BY ...

-  SORT BY ...

-  LIMIT ``n``

Additionally, it is mandatory to include the start time and the end time
for the data range to define the time period for the query data. The
parameters of the query are passed through POST data, using the
following fields:

-  ``start_time`` — the start of the time period

-  ``end_time`` — the end of the time period

-  ``table`` — the table from which to extract data

-  ``select_fields`` — the columns to display in the extracted data

-  ``where`` — the list of match conditions

POST Data Format Example
------------------------

The POST data is in ``JSON`` format, stored in an ``idl`` file. A sample
file is displayed in the following.

**Note**

The result of the query API is also in ``JSON`` format.

.. raw:: html

   <div id="jd0e135" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   /*
   * Copyright (c) 2013 Juniper Networks, Inc. All rights reserved.
   */

   /*
   *  query_rest.idl
   *
   *  IDL definitions for query engine REST API
   *
   *  PLEASE NOTE: After updating this file, do update json_parse.h
   *
   */

   enum match_op {
       EQUAL = 1,
       NOT_EQUAL = 2,
       IN_RANGE = 3,
       NOT_IN_RANGE = 4,   // not supported currently
       // following are only for numerical column fields
       LEQ = 5, // column value is less than or equal to filter value
       GEQ = 6, // column value is greater than or equal to filter value
       PREFIX = 7, // column value has the "value" field as prefix
       REGEX_MATCH = 8 // for filters only
   }

   enum sort_op {
       ASCENDING = 1,
       DESCENDING = 2,
   }     
       
   struct match {
       1: string name;
       2: string value;
       3: match_op op;
       4: optional string value2;   // this is for only RANGE match
   }

   typedef list<match> term; (AND of match)  

   enum flow_dir_t {
        EGRESS = 0,
        INGRESS = 1 
   }
   struct query {
       1: string table; // Table to query (FlowSeriesTable, MessageTable, ObjectVNTable, ObjectVMTable, FlowRecordTable)
       2: i64 start_time; // Microseconds in UTC since Epoch
       3: i64 end_time; // Microseconds in UTC since Epoch
       4: list<string>> select_fields; // List of SELECT fields
       5: list<term> where; // WHERE (OR of terms)
       6: optional sort_op sort;
       7: optional list<string> sort_fields; 
       8: optional i32 limit;
       9: optional flow_dir_t dir; // direction of flows being queried
       10: optional list<match> filter; // filter the processed result by value
   }

   struct flow_series_result_entry {
       1: optional i64 T;  // Timestamp of the flow record
       2: optional string sourcevn;
       3: optional string sourceip;
       4: optional string destvn;
       5: optional string destip;
       6: optional i32 protocol;
       7: optional i32 sport;
       8: optional i32 dport;
       9: optional flow_dir_t direction_ing;
       10: optional i64 packets;  // mutually exclusive to 12,13
       11: optional i64 bytes; // mutually exclusive to 12,13
       12: optional i64 sum_packets; // represented as "sum(packets)" in JSON
       13: optional i64 sum_bytes; // represented as "sum(bytes)" in JSON
   };
   typedef list<flow_series_result_entry> flow_series_result;

.. raw:: html

   </div>

.. raw:: html

   </div>

Query Types
-----------

The ``analytics-api``\ supports two types of queries. Both types use the
same POST parameters as described in POST API.

-  ``sync`` — Default query mode. The results are sent inline with the
   query processing.

-  ``async`` — To execute a query in async mode. The result is "202
   Accepted." This status code indicates the request has been accepted
   for processing but the processing has not been completed.

Examining Asynchronous Query Status
-----------------------------------

For an asynchronous query, the ``analytics-api`` responds with the code:
``202 Accepted``. The response contents are a status entity href URL of
the form: ``/analytics/query/<QueryID>``. The QueryID is assigned by the
``analytics-api``. To view the response contents, poll the status entity
by performing a GET action on the URL. The status entity has a variable
named ``progress``, with a number between 0 and 100, representing the
approximate percentage completion of the query. When progress is 100,
the query processing is complete.

Examining Query Chunks
----------------------

The status entity has an element named ``chunks`` that lists portions
(chunks) of query results. Each element of this list has three fields:
``start_time, end_time, href``. The ``analytics-api``\ determines how
many chunks to list to represent the query data. A chunk can include an
empty string ("") to indicate that the data query is not yet available.
If a partial result is available, the chunk href is of the form:
``/analytics/query/<QueryID>/chunk-partial/<chunk number>.`` When the
final result of a chunk is available, the href is of the form:
``/analytics/query/<QueryID>/chunk-final/<chunk number>``.

Example Queries for Log and Flow Data
-------------------------------------

The following example query lists the tables available for query.

.. raw:: html

   <div id="jd0e207" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   [root@host ~]# curl 127.0.0.1:8081/analytics/tables | python -mjson.tool
     % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
   100   846  100   846    0     0   509k      0 --:--:-- --:--:-- --:--:--  826k
   [
       {
           "href": "http://127.0.0.1:8081/analytics/table/MessageTable",
           "name": "MessageTable"
       },
       {
           "href": "http://127.0.0.1:8081/analytics/table/ObjectVNTable",
           "name": "ObjectVNTable"
       },
       {
           "href": "http://127.0.0.1:8081/analytics/table/ObjectVMTable",
           "name": "ObjectVMTable"
       },
       {
           "href": "http://127.0.0.1:8081/analytics/table/ObjectVRouter",
           "name": "ObjectVRouter"
       },
       {
           "href": "http://127.0.0.1:8081/analytics/table/ObjectBgpPeer",
           "name": "ObjectBgpPeer"
       },
       {
           "href": "http://127.0.0.1:8081/analytics/table/ObjectRoutingInstance",
           "name": "ObjectRoutingInstance"
       },
       {
           "href": "http://127.0.0.1:8081/analytics/table/ObjectXmppConnection",
           "name": "ObjectXmppConnection"
       },
       {
           "href": "http://127.0.0.1:8081/analytics/table/FlowRecordTable",
           "name": "FlowRecordTable"
       },
       {
           "href": "http://127.0.0.1:8081/analytics/table/FlowSeriesTable",
           "name": "FlowSeriesTable"
       }
   ]

.. raw:: html

   </div>

.. raw:: html

   </div>

The following example query lists details for the table named
``MessageTable``.

.. raw:: html

   <div id="jd0e215" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   [root@host ~]# curl 127.0.0.1:8081/analytics/table/MessageTable | python -mjson.tool
     % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
   100   192  100   192    0     0   102k      0 --:--:-- --:--:-- --:--:--  187k
   [
       {
           "href": "http://127.0.0.1:8081/analytics/table/MessageTable/schema",
           "name": "schema"
       },
       {
           "href": "http://127.0.0.1:8081/analytics/table/MessageTable/column-values",
           "name": "column-values"
       }
   ]

.. raw:: html

   </div>

.. raw:: html

   </div>

The following example query lists the schema for the table named
MessageTable.

.. raw:: html

   <div id="jd0e220" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   [root@host ~]# curl 127.0.0.1:8081/analytics/table/MessageTable/schema | python -mjson.tool
     % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
   100   630  100   630    0     0   275k      0 --:--:-- --:--:-- --:--:--  307k
   {
       "columns": [
           {
               "datatype": "int",
               "index": "False",
               "name": "MessageTS"
           },
           {
               "datatype": "string",
               "index": "True",
               "name": "Source"
           },
           {
               "datatype": "string",
               "index": "True",
               "name": "ModuleId"
           },
           {
               "datatype": "string",
               "index": "True",
               "name": "Category"
           },
           {
               "datatype": "int",
               "index": "True",
               "name": "Level"
           },
           {
               "datatype": "int",
               "index": "False",
               "name": "Type"
           },
           {
               "datatype": "string",
               "index": "True",
               "name": "Messagetype"
           },
           {
               "datatype": "int",
               "index": "False",
               "name": "SequenceNum"
           },
           {
               "datatype": "string",
               "index": "False",
               "name": "Context"
           },
           {
               "datatype": "string",
               "index": "False",
               "name": "Xmlmessage"
           }
       ],
       "type": "LOG"
   }

.. raw:: html

   </div>

.. raw:: html

   </div>

The following set of example queries explore a message table.

.. raw:: html

   <div id="jd0e225" class="sample" dir="ltr">

.. raw:: html

   <div class="output" dir="ltr">

::

   root@a6s45:~# cat filename
   { "end_time": "now" , "select_fields": ["MessageTS", "Source", "ModuleId", "Category", "Messagetype", "SequenceNum", "Xmlmessage", "Type", "Level", "NodeType", "InstanceId"] , "sort": 1 , "sort_fields": ["MessageTS"] , "start_time": "now-10m" , "table": "MessageTable" , "where": {"name": "ModuleId", "value": "contrail-control", "op": 1, "suffix": null, "value2": null}, {"name": "Messagetype", "value": "BGPRouterInfo", "op": 1, "suffix": null, "value2": null} }

   root@a6s45:~#
   root@a6s45:~# curl -X POST --data @filename 127.0.0.1:8081/analytics/query --header "Content-Type:application/json" | python -mjson.tool
     % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
   100  9765    0  9297  100   468   9168    461  0:00:01  0:00:01 --:--:--  9177
   {
       "value": [
           {
               "Category": null,
               "InstanceId": "0",
               "Level": 2147483647,
               "MessageTS": 1428442589947392,
               "Messagetype": "BGPRouterInfo",
               "ModuleId": "contrail-control",
               "NodeType": "Control",
               "SequenceNum": 1302,
               "Source": "a6s45",
               "Type": 6,
               "Xmlmessage": "<BGPRouterInfo type=""><data type=""><BgpRouterState><name type=""
   >a6s45</name><cpu_info type=""><CpuLoadInfo><num_cpu type="">4</num_cpu
   ><meminfo type=""><MemInfo><virt type="">438436</virt><peakvirt type=""
   >561048</peakvirt><res type="">12016</res></MemInfo></meminfo><cpu_share
   type="">0.0416667</cpu_share></CpuLoadInfo></cpu_info><cpu_share type=""
   >0.0416667</cpu_share></BgpRouterState></data></BGPRouterInfo>"        },
           {
               "Category": null,
               "InstanceId": "0",
               "Level": 2147483647,

   ...

.. raw:: html

   </div>

.. raw:: html

   </div>

 
