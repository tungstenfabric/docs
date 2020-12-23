import yaml
import json
import urllib.request
from urllib.parse import urlparse
import os
import argparse, textwrap
import re 
from bs4 import BeautifulSoup
import yaml
import pypandoc
import pprint


def read_input_file():
    with open(args.input) as input:
        print("Opened yaml")
        return yaml.safe_load(input)
            


class AllDocuments(object):
    def __init__(self, documents_dict):
        #self.config = config
        # set of DOCUMENTS with dictionaries of PAGES 
        self.newDocuments = []
        self.generateDocuments(documents_dict)

    def generateDocuments(self, documents):
        test_html_docs="""<?xml version="1.0" encoding="UTF-8"?>

<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v-on="http://www.w3.org/1999/xhtml" xmlns:v-bind="http://www.w3.org/1999/xhtml" xmlns:doceng="com.juniper.doceng.util.XSLTExtentions">
<head>
    <meta charset="utf-8">
    </meta>
    <meta http-equiv="X-UA-Compatible" content="IE=Edge">
    </meta>
    <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=0">
    </meta>
    <title>Security Policy Features - TechLibrary - Juniper Networks</title>
    <meta name="description" content="Overview of Existing Network Policy and Security Groups in Contrail, Security Policy Enhancements, Using Tags and Configuration Objects to Enhance Security Policy, Predefined Tags, Custom Tags, Example Tag Usage, Tagging Objects, Policy Application, Configuration Objects, Configuration Object Tag Object, Tag APIs, Label, Local and Global Tags, Analytics, Control Node , Agent, Address-Group Configuration Object, Configuration, Agent, Analytics, Service-Group Configuration Object, Application-policy-set Configuration Object, Policy-management Configuration Object, Firewall-policy Configuration Object, Firewall-rule Configuration Object, Compilation of Rules, Using the Contrail Web User Interface to Manage Security Policies, Adding Security Policies, Managing Policy Tags, Viewing Global Policies, Visualizing Traffic Groups">
    </meta>
    <meta name="feature" content="[]">
    </meta>
    <meta name="branchId" content="100">
    </meta>
    <meta name="topicid" content="122570">
    </meta>
    <meta name="relatedtopics" content="134522;">
    </meta>
    <meta name="supportedlist" content="true">
    </meta>
    <meta name="release" content="contrail 20">
    </meta>
    <link rel="preload" href="https://www.juniper.net/assets/styles/global-nav.css" as="style">
    <link rel="preload" href="https://www.juniper.net/assets/scripts/global-nav.js" as="script">
    <link rel="preload" href="/documentation/webstatic/fonts/swmaterialicon.woff" as="font" crossorigin="anonymous">
    <link href="/documentation/webstatic/css/topic.e48adf0fff25e0e348ce85f087fe2df1.css" rel="stylesheet">
    <link href="https://www.juniper.net/assets/styles/custom/juniper-survey.css" rel="stylesheet" type="text/css">
    <!--IXF: JavaScript begin-->
    <script>
    /*
        --LICENSE--
        Access to and use of BrightEdge Link Equity Manager is governed by the 
        Infrastructure Product Terms located at: www.brightedge.com/infrastructure-product-terms. 
        Customer acknowledges and agrees it has read, understands and agrees to be bound by the 
        Infrastructure Product Terms.
        */

    function startBESDK() {
        var be_sdk_options = {
            'api.endpoint': 'https://ixf2-api.bc0a.com',
            'sdk.account': 'f00000000063367',
            'requestparameters.caseinsensitive': true,
            'whitelist.parameter.list': 'ixf'
        };
        BEJSSDK.construct(be_sdk_options);
    }
    (function() {
        var sdkjs = document.createElement('script');
        sdkjs.type = 'text/javascript';
        sdkjs.async = true;
        sdkjs.src = document.location.protocol + '//cdn.bc0a.com/be_ixf_js_sdk.js';
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(sdkjs, s);
        if (document.addEventListener) {
            sdkjs.addEventListener('load', startBESDK);
        } else {
            sdkjs.onreadystatechange = startBESDK;
        }
    })();
    </script>
    <!--IXF: JavaScript end-->
    <script>
    function insertcanonical() {
        var canonicalexists = !!document.querySelector("link[rel='canonical']");
        if (!canonicalexists) {
            var tag = document.createElement("link");
            var pathname = location.pathname;
            var pattern = /(\/index.html)$/;
            if (pattern.test(pathname)) {
                pathname = pathname.replace(pattern, "/");
            }
            // check if last character is slash else add / to be consistent
            pathname = /(\/|\.html)$/.test(pathname) ? pathname : pathname + "/";
            var href = "https://www.juniper.net" + pathname;
            tag.setAttribute("rel", "canonical");
            tag.setAttribute("href", href);
            document.head.appendChild(tag);
        }
    }
    insertcanonical();
    </script>
    <link rel="preload" as="script" href="/documentation/webstatic/js/manifest.3b5eaa58cfd451fc08ad.js">
    <link rel="preload" as="script" href="/documentation/webstatic/js/vendor.ed74aebf5dabf03fc698.js">
    <link rel="preload" as="script" href="/documentation/webstatic/js/topic.200c1024fdcb210913b8.js">
    <script src="https://assets.adobedtm.com/998b2d6d4944658536fe36266a249b07e626b86d/satelliteLib-6d05b7c7a99e1cbbdcac4fcfe7005e6bee80a0e9.js"></script>
</head>
<body style="visibility:hidden;">
    <!--[if lte IE 9]>
    	<div class="message-warning"> You are using unsupported version of Internet Explorer. Please upgrade your browser to latest version.</div>
    <![endif]-->
    <!-- Google Tag Manager -->
    <noscript>
        <iframe style="display:none;visibility:hidden" width="0" height="0" src="https://www.googletagmanager.com/ns.html?id=GTM-MHNPL3"></iframe>
    </noscript>
    <script>
    (function(w, d, s, l, i) {
        w[l] = w[l] || [];
        w[l].push({
            'gtm.start': new Date().getTime(),
            event: 'gtm.js'
        });
        var f = d.getElementsByTagName(s)[0],
            j = d.createElement(s),
            dl = l != 'dataLayer' ? '&l=' + l : '';
        j.async = true;
        j.src =
        'https://www.googletagmanager.com/gtm.js?id=' + i + dl;
        f.parentNode.insertBefore(j, f);
    })(window, document, 'script', 'dataLayer', 'GTM-MHNPL3');
    </script>
    <!-- End Google Tag Manager -->

    <!-- Start survey script MaritzCX -->
    <script type="text/javascript" src="https://siteintercept.allegiancetech.com/dist/jn1si001/MCX_Juniper2.js"></script>
    <script src="https://siteintercept.allegiancetech.com/InterceptScripts/mcxSiteIntercept-1.9.1.js" type="text/javascript"></script>
    <div id="mcxInvitationModal">
        <div id="mcxFloating">
            <div id="mcxInfo2">
                <div id="mcxNoButton">
                    <button id="mcxNo" onclick="McxSiteInterceptOnExit.declineSurvey();mcxDisplay();">X</button>
                </div>
                <div id="mcxLogos">
                    <img src="https://junipernetworks.allegiancetech.com/surveys/images/MRVCXM/juniper_logo.jpg">
                </div>
                <div class="clearfix">
                    <p id="mcxHeading">Help us improve your experience.</p>
                    <p id="mcxText1">Let us know what you think. </p>
                    <p id="mcxText2">Do you have time for a two-minute survey?</p>
                </div>
                <div id="mcxYesButton" onClick="McxSiteInterceptOnExit.acceptSurvey();mcxDisplay();" class="clearfix">
                    <button id="mcxYes">Yes</button>
                </div>
                <div>
                    <button id="noLater" onclick="McxSiteInterceptOnExit.declineSurvey();mcxDisplay();">Maybe Later</button>
                </div>
            </div>
        </div>
    </div>
    <script>
    window.addEventListener('message', function(e) {
        var key = e.message ? 'message' : 'data';
        var data = e[key];
        console.log(data); // show message recieved from iframe in browser console
        if (data === 'MaritzCX Survey Close') {
            McxSiteInterceptOnExit.closeSurveyModal(); //close iframe
        }
    }, false);
    </script>
    <!-- End survey script MaritzCX -->
    <script type="application/ld+json">
      { "@context" : "http://schema.org",
      "@type" : "Organization",
      "name" : "Juniper Networks",
      "url" : "https://www.juniper.net/us/en/",
      "logo": "https://www.juniper.net/assets/svg/jnpr-logo.svg",
      "sameAs" : ["https://en.wikipedia.org/wiki/Juniper_Networks",
          "https://www.facebook.com/JuniperNetworks/",
          "https://twitter.com/JuniperNetworks/",
          "https://www.linkedin.com/company/juniper-networks",
          "https://www.youtube.com/junipernetworks",
          "https://www.instagram.com/junipernetworks/"]}
    </script>

    <script type="application/ld+json">
    { "@context": "http://schema.org",
    "@id": "https://www.juniper.net/us/en/#website",
    "@type": "WebSite",
    "url": "https://www.juniper.net/us/en/",
    "name": "Juniper Networks",
    "alternateName": "Juniper, Juniper Networks Inc.",
    "publisher": {"@type": "Corporation",
    "name": "Juniper Networks"}
    </script>
    <div id="app">
        <sw-app inline-template="">
            <div v-bind:class="{_fixed: isfixed}">
                <sw-header></sw-header>
                <sw-change-widget v-bind:scroll="fixcw"></sw-change-widget>
                <section class="main wrapper">
                    <sw-leftnav v-bind:data-height="leftnavheight" v-bind:data-top="leftnavtop" v-on:menucollapse="menucollapse"></sw-leftnav>
                    <sw-rightnav>
                        <div class="minitoc desktop-only">
                            <h5>ON THIS PAGE</h5>
                            <ul v-scrollspy="">
                                <li style="">
                                    <p>
                                        <a href="security-policy-enhancements.html#jd0e12">Overview of Existing Network Policy and Security Groups in Contrail</a>
                                    </p>
                                </li>
                                <li style="">
                                    <p>
                                        <a href="security-policy-enhancements.html#jd0e39">Security Policy Enhancements</a>
                                    </p>
                                </li>
                                <li style="">
                                    <p>
                                        <a href="security-policy-enhancements.html#jd0e61">Using Tags and Configuration Objects to Enhance Security Policy</a>
                                    </p>
                                </li>
                                <li style="">
                                    <p>
                                        <a href="security-policy-enhancements.html#jd0e118">Configuration Objects</a>
                                    </p>
                                </li>
                                <li style="">
                                    <p>
                                        <a href="security-policy-enhancements.html#jd0e416">Using the Contrail Web User Interface to Manage Security Policies</a>
                                    </p>
                                </li>
                            </ul>
                        </div>
                    </sw-rightnav>
                    <div class="l-body" v-bind:style="{'min-height':bodyheight+'px'}" v-bind:class="{'collapsed':isleftnavcollapsed}">
                        <nav class="page-options clearfix">
                            <sw-breadcrumb>&nbsp;</sw-breadcrumb>
                        </nav>
                        <div class="topicBody">
                            <div id="topic-content">
                                <h1 id="jd0e2">Security Policy Features</h1>
                                <sw-topic-details date="2019-04-16">&nbsp;</sw-topic-details>
                                <div style="">
                                    <p></p>
                                </div>
                                <h2 id="jd0e12">Overview of Existing Network Policy and Security Groups in Contrail</h2>
                                <p>Contrail virtual networks are isolated by default. Workloads
                                in a virtual network cannot communicate with workloads in other virtual
                                networks, by default. A Contrail network policy may be used
                                to connect two virtual networks. In addition, Contrail network policy
                                also provides security between two virtual networks by allowing or
                                denying specified traffic.</p>
                                <p>In modern cloud environments, workloads are moving from one
                                server to another, one rack to another and so on. Therefore, users
                                must rely less on using IP addresses or other network coordinates
                                to identify the endpoints to be protected. Instead users must leverage
                                application attributes to author policies, so that the policies don't
                                need to be updated on account of workload mobility. </p>
                                <div style="">
                                    <p>You might want to segregate traffic based on the different categories
                                    of data origination, such as: </p>
                                </div>
                                <ul>
                                    <li style="">
                                        <p>Protecting the application itself</p>
                                    </li>
                                    <li style="">
                                        <p>Segregating traffic for specific component tiers within
                                        the application</p>
                                    </li>
                                    <li style="">
                                        <p>Segregating traffic based on the deployment environment
                                        for the application instance</p>
                                    </li>
                                    <li style="">
                                        <p>Segregating traffic based on the specific geographic location
                                        where the application is deployed</p>
                                    </li>
                                </ul>
                                <p>There are many other possible scenarios where traffic needs
                                to be segregated.</p>
                                <p>Additionally, you might need to group workloads based on combinations
                                of tags. These intents are hard to express with existing network policy
                                constructs or Security Group constructs. Besides, existing policy
                                constructs leveraging the network coordinates, must continually be
                                rewritten or updated each time workloads move and their associated
                                network coordinates change. </p>
                                <h2 id="jd0e39">Security Policy Enhancements</h2>
                                <p>As the Contrail environment has grown and become more complex,
                                it has become harder to achieve desired security results with the
                                existing network policy and security group constructs. The Contrail
                                network policies have been tied to routing, making it difficult to
                                express security policies for environments such as cross sectioning
                                between categories, or having a multi-tier application supporting
                                development and production environment workloads with no cross environment
                                traffic.</p>
                                <p>Starting with Contrail Release 4.1, limitations of the current
                                network policy and security group constructs are addressed by supporting
                                decoupling of routing from security policies, multidimension segmentation,
                                and policy portability. This release also enhances user visibility
                                and analytics functions for security.</p>
                                <p>Contrail Release 4.1 introduces new firewall security policy
                                objects, including the following enhancements:</p>
                                <ul>
                                    <li style="">
                                        <p>Routing and policy decoupling&#8212;introducing new firewall
                                        policy objects, which decouples policy from routing.</p>
                                    </li>
                                    <li style="">
                                        <p>Multidimension segmentation&#8212;segment traffic and
                                        add security features, based on multiple dimensions of entities, such
                                        as application, tier, deployment, site, usergroup, and so on.</p>
                                    </li>
                                    <li style="">
                                        <p>Policy portability&#8212;security policies can be ported
                                        to different environments, such as &#8216;from development to production&#8217;,
                                        &#8216;from pci-complaint to production&#8217;, &#8216;to bare metal
                                        environment&#8217; and &#8216;to container environment&#8217;. </p>
                                    </li>
                                    <li style="">
                                        <p>Visibility and analytics</p>
                                    </li>
                                </ul>
                                <h2 id="jd0e61">Using Tags and Configuration Objects to Enhance Security Policy</h2>
                                <p>Starting with Contrail Release 4.1, tags and configuration objects
                                are used to create new firewall policy objects that decouple routing
                                and network policies, enabling multidimension segmentation and policy
                                portability.</p>
                                <p>Multidimension traffic segmentation helps you segment traffic
                                based on dimensions such as application, tier, deployment, site, and
                                usergroup. </p>
                                <p>
                                    You can also port security policies to different environments.
                                    Portability of policies are enabled by providing match conditions
                                    for tags. Match tags must be added to the policy rule to match tag
                                    values of source and destination workloads without mentioning tag
                                    values. For example, in order for the 
                                    <code class="inline" v-pre="">&#8216;allow protocol
                                    tcp source application-tier=web destination application-tier=application
                                    match application and site&#8217;</code>
                                     rule to take effect,
                                    the application and site values must match. 
                                </p>
                                <h3 id="jd0e73">Predefined Tags</h3>
                                <p>You can choose predefined tags based on the environment and
                                deployment requirements. </p>
                                <div style="">
                                    <p>Predefined tags include:</p>
                                </div>
                                <ul>
                                    <li style="">
                                        <p>application</p>
                                    </li>
                                    <li style="">
                                        <p>application-tier </p>
                                    </li>
                                    <li style="">
                                        <p>deployment</p>
                                    </li>
                                    <li style="">
                                        <p>site </p>
                                    </li>
                                    <li style="">
                                        <p>label (a special tag that allows the user to label objects)</p>
                                    </li>
                                </ul>
                                <h4 id="jd0e97">Custom Tags</h4>
                                <p>You can also define custom tags for a Kubernetes environment.
                                You can define tags in the UI or upload configurations in JSON format.</p>
                                <h4 id="jd0e102">Example Tag Usage</h4>
                                <p>
                                    <code class="inline" v-pre="">application = HRApp application-tier = Web site
                                    = USA</code>
                                </p>
                                <h3 id="jd0e108">Tagging Objects</h3>
                                <p>A user can tag the objects project, VN, VM, and VMI with tags
                                and values to map their security requirements. Tags follow the hierarchy
                                of project, VN, VM and VMI and are inherited in that order. This gives
                                an option for the user to provide default settings for any tags at
                                any level. Policies can specify their security in terms of tagged
                                endpoints, in addition to expressing in terms of ip prefix, network,
                                and address groups endpoints.</p>
                                <h3 id="jd0e113">Policy Application</h3>
                                <p>Policy application is a new object, implemented by means of
                                the application tag. The user can create a list of policies per application
                                to be applied during the flow acceptance evaluation. Introducing global
                                scoped policies and project scoped policies. There are global scoped
                                policies, which can be applied globally for all projects, and project
                                scoped policies, which are applied to specific projects. </p>
                                <h2 id="jd0e118">Configuration Objects</h2>
                                <div style="">
                                    <p>The following are the configuration objects for the new security
                                    features.</p>
                                </div>
                                <ul>
                                    <li style="">
                                        <p>firewall-policy</p>
                                    </li>
                                    <li style="">
                                        <p>firewall-rule </p>
                                    </li>
                                    <li style="">
                                        <p>policy-management</p>
                                    </li>
                                    <li style="">
                                        <p>application-policy </p>
                                    </li>
                                    <li style="">
                                        <p>service-group</p>
                                    </li>
                                    <li style="">
                                        <p>address-group</p>
                                    </li>
                                    <li style="">
                                        <p>tag</p>
                                    </li>
                                    <li style="">
                                        <p>global-application-policy</p>
                                    </li>
                                </ul>
                                <h3 id="jd0e149">Configuration Object Tag Object</h3>
                                <div style="">
                                    <p>Each configuration object tag object contains:</p>
                                </div>
                                <ul>
                                    <li style="">
                                        <p>tag: one of the defined tag types, stored as string and
                                        a 32-bit ID. </p>
                                    </li>
                                    <li style="">
                                        <p>tag type: Contains the type string and ID (the first 16
                                        bits of the tag) and references to the tag resource type</p>
                                    </li>
                                </ul>
                                <p>Each value entered by the user creates a unique ID that is set
                                in the tag_id field. The system can have up to 64 million tag values.
                                On average, each tag can have up to 2k values, but there are no restrictions
                                per tag. </p>
                                <p>Tags and labels can be attached to any object, for example,
                                project, VN, VM, VMI, and policy, and these objects have a tag reference
                                list to support multiple tags. </p>
                                <p>RBAC controls the users allowed to modify or remove attached
                                tags. Some tags (typically facts) are attached by the system by default
                                or by means of introspection.</p>
                                <h4 id="jd0e168">Tag APIs</h4>
                                <p>Tag APIs are used to give RBAC per tag in any object (VMI, VM,
                                Project &#8230;.). </p>
                                <ul>
                                    <li style="">
                                        <p>
                                            REST: 
                                            <code class="inline" v-pre="">HTTP POST to /set_tag_&lt;tag_type&gt;/&lt;obj_uuid&gt;</code>
                                        </p>
                                    </li>
                                    <li style="">
                                        <p>
                                            Python: 
                                            <code class="inline" v-pre="">set_tag_&lt;tag_type&gt; (object_type,
                                            object_uuid, tag_value) </code>
                                        </p>
                                    </li>
                                </ul>
                                <p>Configuration also supports the following APIs:</p>
                                <ul>
                                    <li style="">
                                        <p>tag query</p>
                                    </li>
                                    <li style="">
                                        <p>tags (policy)</p>
                                    </li>
                                    <li style="">
                                        <p>tags (application tag) </p>
                                    </li>
                                    <li style="">
                                        <p>object query</p>
                                    </li>
                                    <li style="">
                                        <p>tags (object) </p>
                                    </li>
                                    <li style="">
                                        <p>tags (type, value) </p>
                                    </li>
                                </ul>
                                <h4 id="jd0e205">Label</h4>
                                <p>Label is special tag type, used to assign labels for objects.
                                All of the tag constructs are valid, except that tag type is &#8216;label'.
                                One difference from other tags is that an object can have any number
                                of labels. All other tag types are restricted to one tag per object. </p>
                                <h4 id="jd0e210">Local and Global Tags</h4>
                                <p>Tags can be defined globally or locally under a project; tag
                                objects are children of either config-root or a project. An object
                                can be tagged with a tag in its project or with a globally-scoped
                                tag. </p>
                                <h4 id="jd0e215">Analytics</h4>
                                <p>When given a tag query with a SQL where clause and select clause,
                                analytics should give out objects. The query can also contain labels,
                                and the labels can have different operators. </p>
                                <p>Example: </p>
                                <p>
                                    User might want to know: a list of VMIs where 
                                    <code class="inline" v-pre="">&#8217;site
                                    == USA and deployment == Production'</code>
                                </p>
                                <p>
                                     list of VMIs where 
                                    <code class="inline" v-pre="">&#8217;site == USA and deployment
                                    == Production has &#8217; </code>
                                </p>
                                <p>Given tag SQL where clause and select clause, analytics should
                                give out flows.</p>
                                <h4 id="jd0e232">Control Node </h4>
                                <p>The control node passes the tags, along with route updates,
                                to agents and other control nodes. </p>
                                <h4 id="jd0e237">Agent</h4>
                                <p>Agent gets attached tags along with configuration objects. Agent
                                also gets route updates containing tags associated with IP route.
                                This process is similar to getting security group IDs along with the
                                route update.</p>
                                <h3 id="jd0e242">Address-Group Configuration Object</h3>
                                <div style="">
                                    <p>There are multiple ways to add IP address to address-group.</p>
                                </div>
                                <ul>
                                    <li style="">
                                        <p>Manually add IP prefixes to the address-group by means
                                        of configuration.</p>
                                    </li>
                                    <li style="">
                                        <p>Label a work load with the address-group&#8217;s specified
                                        label. All ports that are labelled with the same label are considered
                                        to be part of that address-group. </p>
                                    </li>
                                    <li style="">
                                        <p>Use introspect workloads, based on certain criteria, to
                                        add ip-address to address-group. </p>
                                    </li>
                                </ul>
                                <h4 id="jd0e258">Configuration</h4>
                                <p>The address-group object refers to a label object, description,
                                and list of IP prefixes. The label - object is created using the tag
                                APIs. </p>
                                <h4 id="jd0e263">Agent</h4>
                                <p>Agent gets address-group and label objects referenced in policy
                                configuration. Agent uses this address group for matching policy rules. </p>
                                <h4 id="jd0e268">Analytics</h4>
                                <p>When given address group label, analytics gets all the objects
                                associated with it. Given address group label, get all the flows associated
                                with it.</p>
                                <h3 id="jd0e273">Service-Group Configuration Object</h3>
                                <p>Configuration </p>
                                <p>The service-group contains a list of ports and protocols. The
                                open stack service-group has a list of service objects; the service
                                object contains attributes: id, name, service group id, protocol,
                                source_port, destination_port, icmp_code, icmp_type, timeout, tenant
                                id.</p>
                                <p>Agent </p>
                                <p>Agent gets service-group object as it is referred to in a policy
                                rule. Agent uses this service group during policy evaluation.</p>
                                <h3 id="jd0e284">Application-policy-set Configuration Object</h3>
                                <p>The application-policy-set configuration object can refer to
                                a tag of type application, network-policy objects, and firewall-policy
                                objects. This object can be local (project) or globally scoped. </p>
                                <p>When an application tag is attached to an application-policy-set
                                object, the policies referred by that object are automatically applied
                                to the ports that have the same application tag. </p>
                                <p>Any firewall-policies referred by the application-policy-set
                                objects are ordered using sequence numbers. If the same application
                                tag is attached to multiple application-policy-sets, all those sets
                                will apply, but order among those sets is undefined. </p>
                                <p>One application-policy-set (called default-policy-application-set)
                                is special in that policies referred by it are applied to all interfaces
                                by default, after applying policies referred to other application-policy-sets. </p>
                                <p>Upon seeing the application tag for any object, the associated
                                policies are sent to agent. Agent will use this information to find
                                out the list of policies to be applied and their sequence during flow
                                evaluation. User can attach application tag to allowed objects (Project,
                                VN, VM or VMI).</p>
                                <h3 id="jd0e297">Policy-management Configuration Object</h3>
                                <p>Policy-management is a global container object for all policy-related
                                configuration. </p>
                                <div style="">
                                    <p>Policy-management object contains</p>
                                </div>
                                <ul>
                                    <li style="">
                                        <p>network-policies (NPs)</p>
                                    </li>
                                    <li style="">
                                        <p>firewall-policies (FWPs)</p>
                                    </li>
                                    <li style="">
                                        <p>application-policy-sets</p>
                                    </li>
                                    <li style="">
                                        <p>global-policy objects</p>
                                    </li>
                                    <li style="">
                                        <p>global-policy-apply objects</p>
                                    </li>
                                    <li style="">
                                        <p>NPs - List of contrail networking policy objects</p>
                                    </li>
                                    <li style="">
                                        <p>FWPs - List of new firewall policy objects</p>
                                    </li>
                                    <li style="">
                                        <p>Application-policies - List of Application-policy objects </p>
                                    </li>
                                    <li style="">
                                        <p>Global-policies - List of new firewall policy objects,
                                        that are defined for global access</p>
                                    </li>
                                    <li style="">
                                        <p>Global-policy-apply - List of global policies in a sequence,
                                        and these policies applied during flow evaluation.</p>
                                    </li>
                                    <li style="">
                                        <p>Network Policies (NP) references are available, as they
                                        are today.</p>
                                    </li>
                                </ul>
                                <h3 id="jd0e339">Firewall-policy Configuration Object</h3>
                                <p>
                                    <code class="inline" v-pre="">Firewall-policy </code>
                                    is a new policy object
                                    that contains a list of firewall-rule-objects and audited flag. Firewall-policy
                                    can be project or global scoped depending on usage. Includes an audited
                                    Boolean flag to indicate that the owner of the policy indicated that
                                    the policy is audited. Default is False, and will have to explicitly
                                    be set to True after review. Generates a log event for audited with
                                    timestamp and user details.
                                </p>
                                <h3 id="jd0e346">Firewall-rule Configuration Object</h3>
                                <p>Firewall-rule is a new rule object, which contains the following
                                fields. The syntax is to give information about their layout inside
                                the rule.</p>
                                <ul>
                                    <li style="">
                                        <p>
                                            &lt;sequence number&gt; 
                                            <br>
                                            </br>
                                            There is a string
                                            object sequence number on the link from firewall-policy to firewall-policy-rule
                                            objects. The sequence number decides the order in which the rules
                                            are applied.
                                        </p>
                                    </li>
                                    <li style="">
                                        <p>[&lt; id &gt;] </p>
                                        <p>uuid</p>
                                    </li>
                                    <li style="">
                                        <p>[name &lt; name &gt;] </p>
                                        <p>Unique name selected by user</p>
                                    </li>
                                    <li style="">
                                        <p>[description &lt; description &gt;] </p>
                                    </li>
                                    <li style="">
                                        <p>public</p>
                                    </li>
                                    <li style="">
                                        <p>{permit | deny} </p>
                                    </li>
                                    <li style="">
                                        <p>[ protocol {&lt; protocol-name &gt; | any } destination-port
                                        { &lt; port range &gt; | any } [ source-port { &lt; port range &gt; | any}
                                        ] ] | service-group &lt; name &gt; </p>
                                    </li>
                                    <li style="">
                                        <p>endpoint-1 { [ip &lt; prefix &gt; ] | [virtual-network &lt;
                                        vnname &gt;] | [address-group &lt; group name &gt;] | [tags T1 == V1 &amp;&amp;
                                        T2 == V2 &#8230; &amp;&amp; Tn == Vn &amp;&amp; label == label name...]
                                        | any} </p>
                                    </li>
                                    <li style="">
                                        <p>{ -&gt; | &lt;- | &lt;-&gt; } </p>
                                        <p>Specifies connection direction. All the rules are connection
                                        oriented and this option gives the direction of the connection.</p>
                                    </li>
                                    <li style="">
                                        <p>endpoint-2 { [ip &lt; prefix &gt; ] | [virtual-network &lt;
                                        vnname &gt;] | [address-group &lt; group name &gt;] | [tags T1 == V1 &amp;&amp;
                                        T2 == V2 &#8230; &amp;&amp; Tn == Vn &amp;&amp; label == label name...]
                                        | any } </p>
                                        <p>Tags at endpoints support an expression of tags. We support
                                        only &#8216;==&#8216; and &#8216;&amp;&amp;&#8217; operators. User
                                        can specify labels also as part the expression. Configuration object
                                        contains list of tag names (or global:tag-name in case of global tags)
                                        for endpoints. </p>
                                    </li>
                                    <li style="">
                                        <p>[ match_tags {T1 &#8230;. Tn} | none} ] </p>
                                        <p>List of tag types or none. User can specify either match with
                                        list of tags or none. Match with list of tags mean, source and destination
                                        tag values should match for the rule to take effect.</p>
                                    </li>
                                    <li style="">
                                        <p>[ log| mirror | alert | activate | drop | reject | sdrop
                                        ] </p>
                                        <p>complex actions</p>
                                    </li>
                                    <li style="">
                                        <p>{ enable | disable }</p>
                                        <p>A boolean flag to indicate the rule is enabled or disabled.
                                        Facilitates selectively turn off the rules, without remove the rule
                                        from the policy. Default is True.</p>
                                    </li>
                                    <li style="">
                                        <p>filter </p>
                                    </li>
                                </ul>
                                <h4 id="jd0e410">Compilation of Rules</h4>
                                <p>Whenever the API server receives a request to create/update
                                a firewall policy rule object, it analyzes the object data to make
                                sure that all virtual-networks, address-group, tag objects exist.
                                If any of them do not exist, the request will be rejected. In addition,
                                it will actually create a reference to those objects mentioned in
                                the two endpoints. This achieves two purposes. First, we don't allow
                                users to name non-existent objects in the rule and second, the user
                                is not allowed to delete those objects without first removing them
                                from all rules that are referring to them. </p>
                                <p></p>
                                <h2 id="jd0e416">Using the Contrail Web User Interface to Manage Security Policies</h2>
                                <ul>
                                    <li style="">
                                        <p>
                                            <a href="security-policy-enhancements.html#jd0e421">Adding Security Policies</a>
                                        </p>
                                    </li>
                                    <li style="">
                                        <p>
                                            <a href="security-policy-enhancements.html#jd0e495">Managing Policy Tags</a>
                                        </p>
                                    </li>
                                    <li style="">
                                        <p>
                                            <a href="security-policy-enhancements.html#jd0e528">Viewing Global Policies</a>
                                        </p>
                                    </li>
                                    <li style="">
                                        <p>
                                            <a href="security-policy-enhancements.html#jd0e566">Visualizing Traffic Groups</a>
                                        </p>
                                    </li>
                                </ul>
                                <h3 id="jd0e421">Adding Security Policies</h3>
                                <div style=""></div>
                                <ol type="1">
                                    <li id="jd0e426" style="">
                                        To add a security policy, go to 
                                        <strong v-pre="">Configure &gt; Security
                                        &gt; Global Policies</strong>
                                        . Near the upper right, click the button 
                                        <strong v-pre="">Firewall Policy Wizard</strong>
                                        . The 
                                        <strong v-pre="">Firewall Policy Wizard</strong>
                                         appears, where you can create your new firewall policy by adding
                                        or selecting an application policy set. See 
                                        <a href="security-policy-enhancements.html#fw1">Figure&nbsp;1</a>
                                        .
                                        <figure id="fw1">
                                            <figurecaption>Figure 1: Firewall Policy Wizard</figurecaption>
                                            <div class="graphic">
                                                <img alt="Firewall Policy Wizard" src="/documentation/images/s019913.png" style="">
                                                </img>
                                            </div>
                                        </figure>
                                    </li>
                                    <li id="jd0e444" style="">
                                        Click the large + on the Firewall Policy Wizard screen
                                        to view the
                                        <strong v-pre=""> Application Policy Sets</strong>
                                         window. The existing
                                        application policy sets are displayed. See 
                                        <a href="security-policy-enhancements.html#fw2">Figure&nbsp;2</a>
                                        .
                                        <figure id="fw2">
                                            <figurecaption>Figure 2: Application Policy Sets</figurecaption>
                                            <div class="graphic">
                                                <img alt="Application Policy Sets" src="/documentation/images/s019914.png" style="">
                                                </img>
                                            </div>
                                        </figure>
                                    </li>
                                    <li id="jd0e456" style="">
                                        To create a new firewall policy, click the application
                                        policy set in the list to which the new firewall policy will belong.
                                        The 
                                        <strong v-pre="">Edit Application Policy Sets </strong>
                                        window appears, displaying
                                        a field for the description of the selected policy set and listing
                                        firewall policies associated with the set. See 
                                        <a href="security-policy-enhancements.html#fw3">Figure&nbsp;3</a>
                                        , where the 
                                        <strong v-pre="">HRPolicySet</strong>
                                         has been selected.
                                        <figure id="fw3">
                                            <figurecaption>Figure 3: Edit Application Policy Sets</figurecaption>
                                            <div class="graphic">
                                                <img alt="Edit Application Policy Sets" src="/documentation/images/s019915.png" style="">
                                                </img>
                                            </div>
                                        </figure>
                                    </li>
                                    <li id="jd0e471" style="">
                                        To view all firewall policies, click the Application Policy
                                        Sets link in the left side. 
                                        <p>
                                            See 
                                            <a href="security-policy-enhancements.html#fw4">Figure&nbsp;4</a>
                                            .
                                        </p>
                                        <figure id="fw4">
                                            <figurecaption>Figure 4: All Firewall Policies</figurecaption>
                                            <div class="graphic">
                                                <img alt="All Firewall Policies" src="/documentation/images/s019916.png" style="">
                                                </img>
                                            </div>
                                        </figure>
                                    </li>
                                    <li id="jd0e482" style="">
                                        Select any listed firewall policy to view or edit the
                                        rules associated with that policy. See 
                                        <a href="security-policy-enhancements.html#fw5">Figure&nbsp;5</a>
                                        ,
                                        where all the rules for the 
                                        <strong v-pre="">AdminPolicy</strong>
                                         are listed. Use
                                        the dropdown menus in each field to add or change policy rules, and
                                        use the +, - icons to the right of each rule to add or delete the
                                        rule.
                                        <figure id="fw5">
                                            <figurecaption>Figure 5: Firewall Policy Rules</figurecaption>
                                            <div class="graphic">
                                                <img alt="Firewall Policy Rules" src="/documentation/images/s019917.png" style="">
                                                </img>
                                            </div>
                                        </figure>
                                    </li>
                                </ol>
                                <h3 id="jd0e495">Managing Policy Tags</h3>
                                <p>You can use the Contrail web user interface to create and manage
                                the tags used to provide granularity to security policies. You can
                                have global tags, applicable to the entire system, or project tags,
                                defined for specific uses in specific projects.</p>
                                <ol type="1">
                                    <li id="jd0e501" style="">
                                        To manage policy tags, go to 
                                        <strong v-pre="">Configure &gt; Tags &gt; Global
                                        Tags</strong>
                                        . The 
                                        <strong v-pre="">Tags</strong>
                                         window appears, listing all of the
                                        tags in use in the system, with the associated virtual networks, ports,
                                        and projects for each tag. Tags are defined first by type, such as
                                        application, deployment, site, tier, and so on. See 
                                        <a href="security-policy-enhancements.html#fw6">Figure&nbsp;6</a>
                                        . 
                                        <figure id="fw6">
                                            <figurecaption>Figure 6: Tags</figurecaption>
                                            <div class="graphic">
                                                <img alt="Tags" src="/documentation/images/s019918.png" style="">
                                                </img>
                                            </div>
                                        </figure>
                                    </li>
                                    <li id="jd0e516" style="">
                                        You can click through any listed tag to see the rules
                                        to which the tag is applied. See 
                                        <a href="security-policy-enhancements.html#fw7">Figure&nbsp;7</a>
                                        , which
                                        shows the application tags that are applied to the current application
                                        sets. You can also reach this page from 
                                        <strong v-pre="">Configure &gt; Security
                                        &gt; Global Policies</strong>
                                        .
                                        <figure id="fw7">
                                            <figurecaption>Figure 7: View Application Tags</figurecaption>
                                            <div class="graphic">
                                                <img alt="View Application Tags" src="/documentation/images/s019919.png" style="">
                                                </img>
                                            </div>
                                        </figure>
                                    </li>
                                </ol>
                                <h3 id="jd0e528">Viewing Global Policies</h3>
                                <p>
                                    From 
                                    <strong v-pre="">Configure &gt; Security &gt; Global Policies</strong>
                                    , in addition
                                    to viewing the policies includes in application policy sets, you can
                                    also view all firewall policies, all service groups policies, and
                                    all address groups policies.
                                </p>
                                <div style=""></div>
                                <ol type="1">
                                    <li id="jd0e538" style="">
                                        To view and manage the global firewall policies, from 
                                        <strong v-pre="">Configure &gt; Security &gt; Global Policies</strong>
                                        , click the Firewall
                                        Policies tab to view the details for system firewall policies, see 
                                        <a href="security-policy-enhancements.html#fw8">Figure&nbsp;8</a>
                                        <figure id="fw8">
                                            <figurecaption>Figure 8: Firewall Policies</figurecaption>
                                            <div class="graphic">
                                                <img alt="Firewall Policies" src="/documentation/images/s019920.png" style="">
                                                </img>
                                            </div>
                                        </figure>
                                    </li>
                                    <li id="jd0e550" style="">
                                        To view and manage the service groups policies, from 
                                        <strong v-pre="">Configure &gt; Security &gt; Global Policies</strong>
                                        , click the 
                                        <strong v-pre="">Service
                                        Groups</strong>
                                         tab to view the details for system policies for service
                                        groups, see 
                                        <a href="security-policy-enhancements.html#fw9">Figure&nbsp;9</a>
                                        .
                                        <figure id="fw9">
                                            <figurecaption>Figure 9: Service Groups</figurecaption>
                                            <div class="graphic">
                                                <img alt="Service Groups" src="/documentation/images/s019921.png" style="">
                                                </img>
                                            </div>
                                        </figure>
                                    </li>
                                </ol>
                                <h3 id="jd0e566">Visualizing Traffic Groups</h3>
                                <p>
                                    Use 
                                    <strong v-pre="">Monitor &gt; Security &gt; Traffic Groups</strong>
                                     to explore
                                    visual representations of how policies are applied to traffic groups.
                                    See 
                                    <a href="security-policy-enhancements.html#fw10">Figure&nbsp;10</a>
                                    , which is a visual representation of
                                    the source and destination traffic for the past one hour of a traffic
                                    group named Traffic Groups. The outer circle represents traffic tagged
                                    with application, deployment, or project. The inner circle represents
                                    traffic tagged with tier. The center of the circle shows the traffic
                                    origination and destination.
                                </p>
                                <figure id="fw10">
                                    <figurecaption>Figure 10: Traffic Groups</figurecaption>
                                    <div class="graphic">
                                        <img alt="Traffic Groups" src="/documentation/images/s019922.png" style="">
                                        </img>
                                    </div>
                                </figure>
                                <p>
                                    You can click in the right side of the screen to get details
                                    of the policy rules that have been matched by the selected traffic.
                                    See 
                                    <a href="security-policy-enhancements.html#fw11">Figure&nbsp;11</a>
                                    .
                                </p>
                                <figure id="fw11">
                                    <figurecaption>Figure 11: Traffic Groups, Policy Details</figurecaption>
                                    <div class="graphic">
                                        <img alt="Traffic Groups, Policy Details" src="/documentation/images/s019923.png" style="">
                                        </img>
                                    </div>
                                </figure>
                                <p>
                                    You can click in the right side of the screen to get to the 
                                    <strong v-pre="">Settings</strong>
                                     window, where you can change the type of view and
                                    change which items appear in the visual representation. See 
                                    <a href="security-policy-enhancements.html#fw12">Figure&nbsp;12</a>
                                    .
                                </p>
                                <figure id="fw12">
                                    <figurecaption>Figure 12: Traffic Groups, Settings</figurecaption>
                                    <div class="graphic">
                                        <img alt="Traffic Groups, Settings" src="/documentation/images/s019924.png" style="">
                                        </img>
                                    </div>
                                </figure>
                                <p>
                                    You can click on the name of a policy that has been matched
                                    to view the endpoint statistics, including source tags and remote
                                    tags, of the traffic currently represented in the visual. See 
                                    <a href="security-policy-enhancements.html#fw13">Figure&nbsp;13</a>
                                    .
                                </p>
                                <figure id="fw13">
                                    <figurecaption>Figure 13: Traffic Groups, Endpoint Statistics</figurecaption>
                                    <div class="graphic">
                                        <img alt="Traffic Groups, Endpoint Statistics" src="/documentation/images/s019925.png" style="">
                                        </img>
                                    </div>
                                </figure>
                                <p>
                                    You can click deeper through any linked statistic to view more
                                    details about that statistic, see 
                                    <a href="security-policy-enhancements.html#fw15">Figure&nbsp;15</a>
                                      and 
                                    <a href="security-policy-enhancements.html#fw15">Figure&nbsp;15</a>
                                    .
                                </p>
                                <figure id="fw14">
                                    <figurecaption>Figure 14: Traffic Groups, Details</figurecaption>
                                    <div class="graphic">
                                        <img alt="Traffic Groups, Details" src="/documentation/images/s019926.png" style="">
                                        </img>
                                    </div>
                                </figure>
                                <p></p>
                                <figure id="fw15">
                                    <figurecaption>Figure 15: Traffic Groups, Details</figurecaption>
                                    <div class="graphic">
                                        <img alt="Traffic Groups, Details" src="/documentation/images/s019927.png" style="">
                                        </img>
                                    </div>
                                </figure>
                                <p>
                                    You can change the settings of what statistics are displayed
                                    in each traffic group at the 
                                    <strong v-pre="">Traffic Groups Settings </strong>
                                    screen
                                    see 
                                    <a href="security-policy-enhancements.html#fw16">Figure&nbsp;16</a>
                                    .
                                </p>
                                <figure id="fw16">
                                    <figurecaption>Figure 16: Traffic Groups Settings</figurecaption>
                                    <div class="graphic">
                                        <img alt="Traffic Groups Settings" src="/documentation/images/s019928.png" style="">
                                        </img>
                                    </div>
                                </figure>
                                <div class="l-aside-box">
                                    <h3>Related Documentation</h3>
                                    <ul>
                                        <li style="">
                                            <p>
                                                <a href="openstack-security-policy-features.html">Security Policy Features in OpenStack</a>
                                            </p>
                                        </li>
                                    </ul>
                                </div>
                                <sw-prev-next>&nbsp;</sw-prev-next>
                            </div>
                            <sw-comments>&nbsp;</sw-comments>
                        </div>
                    </div>
                </section>
                <sw-pop-over v-bind:head="gterm.head" v-bind:body="gterm.body" v-bind:left="gterm.pos.left" v-bind:top="gterm.pos.top" v-bind:visible="gterm.visible" v-on:close-popover="closegterm()"></sw-pop-over>
                <sw-footer></sw-footer>
            </div>
        </sw-app>
    </div>
    <script type="text/javascript" src="/documentation/assets/scripts/glossary-list.js">&nbsp;</script>
    <script type="text/javascript" src="/documentation/webstatic/js/manifest.3b5eaa58cfd451fc08ad.js"></script>
    <script type="text/javascript" src="/documentation/webstatic/js/vendor.ed74aebf5dabf03fc698.js"></script>
    <script type="text/javascript" src="/documentation/webstatic/js/topic.200c1024fdcb210913b8.js"></script>
    <script type="text/javascript">
    _satellite.pageBottom();
    </script>
</body>
</html>

"""
        pp = pprint.PrettyPrinter(indent=4)
        for document in documents:
            pages=[] #list of pages in that document
            print('Analyzing '+document['name'])
            
            #create folder for that document and images
            if not os.path.exists(args.outputFolder+"/"+document['name']):
                os.mkdir(args.outputFolder+"/"+document['name']) 
            if not os.path.exists(args.outputFolder+"/"+document['name']+"/documentation"):
                os.mkdir(args.outputFolder+"/"+document['name']+"/documentation") 
            if not os.path.exists(args.outputFolder+"/"+document['name']+"/documentation/images"):
                os.mkdir(args.outputFolder+"/"+document['name']+"/documentation/images") 
            #analyze pages
            for page in document['pages']: 
                if page['juniperAgreesToCopy']:
                    #try:
                        print('    Analyzing '+str(page['id'])+":"+page['url'])
                        #get filename
                        filename=os.path.basename(urlparse(page['url']).path) 
                        #check if file exist
                        if os.path.isfile(args.outputFolder+"/"+document['name']+"/"+filename):
                        #if yes print message
                            print("Page already exist: "+document['url'])
                            continue
                        else:
                            #open file
                            f = open(args.outputFolder+"/"+document['name']+"/"+filename, "w")
                            #download that page
                            websiteCode = urllib.request.urlopen(page['url']).read()
                            #extract the content
                            #parsed_html = BeautifulSoup(websiteCode, 'html.parser')
                            parsed_html = BeautifulSoup(test_html_docs, 'html.parser')    

                            #remove empty tags for better html
                            empty_tags = parsed_html.findAll(lambda tag: (not tag.contents or len(tag.get_text(strip=True)) <= 0) and not tag.name == 'br' and not tag.name == 'img')
                            for empty_tag in empty_tags:
                                empty_tag.decompose()
                            #parsed_.smooth()
                            content = parsed_html.body.find(id="topic-content")
                            #extract all images and files
                            images=parsed_html.body.find(id="topic-content").find_all("img")
                            #for each found image
                            for image in images:                                
                                print(image['src'])
                                if os.path.isfile(args.outputFolder+"/"+document['name']+image['src']):
                                #if yes print message
                                    print("Image already exist: "+image['src'])
                                    continue
                                else:
                                    imageContent = urllib.request.urlopen("https://www.juniper.net"+image['src']).read()
                                    imageFileName=os.path.basename(urlparse(image['src']).path)
                                    imagePosixPath=image['src'].replace(imageFileName,"")
                                    #check if image folder is documentation/images
                                    #if not, then save it in documentation/images anyway
                                    #print(imageFileName)
                                    #exit()
                                    imageFile = open(args.outputFolder+"/"+document['name']+"/documentation/images/"+imageFileName, "wb")
                                    imageFile.write(imageContent)
                                    #always change path of file as it needs to be inside document folder
                                    image['src']="documentation/images/"+str(imageFileName)
                                    #image['src']="LOLA"
                                    #newSrc="documentation/images/"+str(imageFileName)
                                    #content=content.replace(image['src'],newSrc)
                                    
                            #write to file
                            
                            f.write(str(content))              
                            f.close()
                            #Convert from html to github markdown
                            
                            mdFileName=str(args.outputFolder+"/"+document['name']+"/"+filename).replace(".html",".md")
                            rstFileName=str(mdFileName).replace(".md",".rst")
                            pdoc_args = ['-s']
                            output = pypandoc.convert_file(args.outputFolder+"/"+document['name']+"/"+filename,
                                                        to='gfm',
                                                        format='html',
                                                        extra_args=pdoc_args,
                                                        outputfile=mdFileName
                                                        )
                            output = pypandoc.convert_file(mdFileName,
                                                        to='rst',
                                                        format='gfm',
                                                        extra_args=pdoc_args,
                                                        outputfile=rstFileName
                                                        )
                            #output = pypandoc.convert_file(args.outputFolder+"/"+document['name']+"/"+filename, 'gfm', outputfile=mdFileName)
                            #output = pypandoc.convert_file(mdFileName, 'rst', outputfile=rstFileName)

                            #Convert from github markdown to rst

                            exit()
                    #except:
                    #   print("Page doesn't exist: "+page['url'])
                    #  continue
            #websiteBaseUrl=websiteURL.replace(filename, "") #domena do której będą doklejane linki z ToC

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='This script takes input file with links to documentation pages, downloads pages where we have permission from Juniper to copy their content to Tungsten Fabric.',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i','--input', help=textwrap.dedent('''\
        YAML file containint links to documentation pages
        '''),
        required=True)
    parser.add_argument('-o','--outputFolder',help='Output folder where downloaded files will be stored', required=True)
    args = parser.parse_args()
    #create folder for output
    if not os.path.exists(args.outputFolder):
            os.mkdir(args.outputFolder) 

    input = read_input_file()
    AllDocuments(input)