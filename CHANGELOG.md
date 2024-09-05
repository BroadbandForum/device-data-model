<!-- do not edit! this file was created from PROJECT.yaml by project-parser.py -->

# TR-181: Device Data Model Change Log

See <https://device-data-model.broadband-forum.org> for the
current TR-181 specification.

## 2024-09-04: TR-181 Issue 2 Amendment 18 Corrigendum 1

*Tags: [v2.18.1] (TR-181), 
       [v1.14.0][TR-106-v1.14.0] (TR-106 didn't change)*

### Data Model
* Fixed newly introduced parameter name from IPv6PassTroughICMPEchoRequest to IPv6PassThroughICMPEchoRequest
* Replaced manual Alias definition by use of component
* Fixed invalid syntax in description of Device.DNS.Client.Server.{i}.Type

## 2024-07-23: [TR-181 Issue 2 Amendment 18]

*Tags: [v2.18.0] (TR-181), 
       [v1.14.0][TR-106-v1.14.0] (TR-106)*

### TR-181 Document
* Fixed logical interface table
* Added ToO chapter about network interface MTU
* Manually resized diagrams to look nice
* Updated all generated diagrams

### Data Model
* Added more counter types to IoT
* Improved MoCA network state parameter descriptions
* Added new parameter to support VLAN priority
* Added new parameter to indicate the used Ethernet duplex mode
* Improved example Ethernet PHY types by using more commonly used types
* Added new parameter to control the sending of ARP messages on an Ethernet link
* Corrected access type of multiple parameters
* Added new parameters for IP based access control in HTTP access
* Added new parameter to configure the MTU on an Ethernet link
* Added new parameter to link a USPService to an ExecutionUnit providing it
* Extended size of various QoS parameter types from 32 bits to 64 bits types
* Added new parameter to control filtering of ICMPv6 packets
* Changed one more missed parameter from hidden to secured
* Added new parameters to control DHCP retransmission/retry behavior
* Removed some dmr:fixedObject attributes from non-fixed objects
* Added Device.Schedules. mechanism to define time-based schedules for services to use
* Added new parameters indicate the reason for a device reboot
* Added new parameters to configure and check the Ethernet MDIX mode
* Deprecated a decent number of MultiAP commands and parameters due to being supported in DataElements
* Refactored many Interface and Link objects, parameters and commands into components for deduplication
* Refactored and improved the description of the NetworkConfig object
* Replaced outdated DHCPv6 bibref by latest RFC
* Added Reset() command to various interface stats objects
* Promoted some readOnly parameters to readWrite
* Added source and dest port ranges to more firewall objects
* Added success and failure counters to IEEE802.1x supplicant stats
* Added 3GPP-NAS auto configuration type to various enumerations
* Added RemainingLeastTime to port-mapping objects
* Demoted a few readWrite objects to readOnly since they were never meant to be the former
* Added histogram mode to PeriodicSampling mechanism
* Added more informational parameters and ShutdownDelay as well as user configuration to SMM DUs
* Added system capabilities configuration to Users
* Changed parameter type of some Wi-Fi timestamps from string to datetime
* Clarified the credentials allowed usages
* Added UUID, Version, and ExecEnvRef as output arguments to the InstallDU() command
* Adjusted indentation to fix rendering issues
* Added missing Alias keys throughout the data model
* Removed some inappropriate dmr:noUniqueKeys annotations

## 2024-01-18: [TR-181 Issue 2 Amendment 17]

*Tags: [v2.17.0] (TR-181), 
       [v1.13.0][TR-106-v1.13.0] (TR-106)*

### TR-181 Document
* Refreshed some data model diagrams

### Data Model
* Added new parameters for Multi-flow and Multi-server testing
  capability as defined in TR-471 Issue 4
* Updated MoCA data model with MoCA Alliance 2.5 specification
* Added Device.DNS.SD.Advertise object to to allow the configuration of
  DNS-SD services that need to be advertised by the device
* Added RDNSS and DNSSL options to the Device.RouterAdvertisement.InterfaceSetting.{i}. object
* Added missing parameters from the Data Elements R2.1 specification
* Added the Zone file concept to the Device.DNS. object
* Added DNS caching configurability to the Device.DNS.Relay. object, allowing for control
  over the cache settings, added a mechanism to allow the specification of the ingress (LAN side) interface(s)
  to be used by the DNS forwarders
* Added new InterfaceSetting object to Device.Firewall.
* Added ModuleVersion parameter to InstallDU() and Update() commands
* Added Origin parameter to PinHole, PortMapping and AccessControl
* Added PhysAddressMask parameter to AccessControl
* Added LeaseDuration and RemainLeaseTime parameters to the DMZ and Pinhole objects
* Added Device.Firewall.ConnectionTracking. object tree to configure ALGs
* Added missing DSL xTU-C and xTU-R parameters to DSL objects
* Added Device.Syslog. object tree to configure a syslog service
* Added Support for password authentication in xPON
* Added MaxNumberOfPortMappings and MaxNumberOfPortTriggers parameters to indicate system limits
* Fixed the access of some UserInterface parameters and objects: Demoted Session and User to read-only, promoted Protocol to read-write
* Fixed the access of a SSH parameter: Promoted AutoDisableDuration to read-write
* Fixed the access of a USPServices parameter: Demoted Protocol to read-only
* Added UDSAgent:1 and UDSController:1 profiles
* Added Device.DeviceInfo.LogRotate.{i}. to setup a log rotation mechanism
* Clarified descriptions of parameters in Device.SoftwareModules.ExecutionUnit.{i}.AutoRestart.
* Added initial support for the 802.11be Wi-Fi 7 standard/mode in various places
* Added OnBoardingComplete parameter to Device.LocalAgent.Controller.{i}.
* Clarified suggested implementation of Device.PeriodicStatistics. concept
* Added support for passing environment variables to software modules
* Removed reference to an incorrect default port requirement from TR-471
* Added EEEStatus parameter to Device.Ethernet.Interface.{i}.
* Extended the key of Device.LocalAgent.Monitor.{i}.OnChange! ChangeSet.{i}.Parameter.{i}. output argument to include ChangeTime
* Added objects and parameters to align with the work-in-progress DataElements R3 specification
* Refactored scheduling related parameters into component for easier reuse and added Active and TimeLeft parameters
* Added Device.SoftwareModules.ExecutionUnit.{i}.NetworkConfig. object and parameters
* Added MaxSupportedDataDownlinkRate, MaxSupportedDataUplinkRate, SNR, and MaxSupportedBandwidth parameters to Device.WiFi.AccessPoint.{i}.AssociatedDevice.{i}.
* Replaced custom coded Order parameter type and descriptions with the new Order datatype and text template
* Changed the default WebSocket port from 5683 to 8443
* Added support for checksum reporting to TransferComplete! event

## 2023-06-14: [TR-181 Issue 2 Amendment 16]

*Tags: [v2.16.0] (TR-181), 
       [v1.12.0][TR-106-v1.12.0] (TR-106)*

### TR-181 Document
* Refreshed all diagrams
* Added ToO appendix for logical interfaces concept
* Extended advanced firewall appendix
* Updated Wi-Fi theory of operation

### Data Model
* Added Device.LocalAgent.Subscription.{i}.TriggerAction parameter to
  control the notification behavior
* Added SecuredRoles concept to the USP-specific ControllerTrust
* Turned a number of "hidden" parameters into "secured" parameters to
  allow USP Controllers with a secure role to read parameter values
* Added a few parameters to Device.Bridging.Bridge. and sub-objects to
  allow better control over bridges and STP behavior
* Made unique key type (functional vs non-functional) explicit rather
  than defaulting, and fixed incorrect choices
* Added ability to configure exclusions from BulkData reports
* Added Device.DeviceInfo.HostName parameter
* Unified description of Interface parameters
* Updated status according to our deprecation policy
* Extended some incorrect type restrictions
* Fixed/unified some units and their use in the description
* Added SupportedLinkModes parameter to ethernet interfaces
* Clarified the Device.Firewall. object and added support for
  firewall features DMZ, Services, Pinholing and Policies. Also added
  support for additional classifiers
* Introduced Device.GatewayInfo. into USP
* Extended the type of a few counters from unsignedInt to StatsCounter64
* Added new IPLayerCapacityDiagnostic parameters/arguments from the
  TR-471i3 document
* Added UDS (Unix Domain Socket) MTP and Device.UnixDomainSockets. objects
  for internal services
* Added Device.Logical. sub-tree to allow for definition of logical network
  interfaces
* Added Device.NAT.PortTrigger.
* Added USP notification mechanism to Device.PeriodicStatistics.
* Improved PPP LCPEcho description and added LCPEchoAdaptive parameter
* Vastly extended Device.QoS. features by adding Queues, Shapers and Schedulers
* Added new parameters to Device.Routing. and sub-objects to add more routing
  features
* Vastly extended SMM (Software Module Management) capabilities with support for
  ApplicationData, HostObject, ExecEnvClass and AutoRestart
* Added Device.SSH. to configure an SSH service
* Extended Device.Time. with support for NTP client and server configuration
* Added Device.UserInterface.HTTPAccess. to allow for local UI access control
* Added USP-specific Device.LocalAgent.Monitor. object to allow for efficient
  tracking of parameter value changes
* Added support for Device.USPServices. to manage internal services via USP
* Added Device.XPON. to model xPON interfaces
* Applied cleanup for Wi-Fi objects/parameters to line up with Wi-Fi Alliance
  documents
* Removed activeNotify="canDeny" attributes from some parameters
* Added PeriodicStatsAdv:2 and MQTTController:2 profiles
* Added USPServiceRef parameters to MTP referencing a service using it
* Disambiguated NTP vs. SNTP protocols
* Expanded/unified descriptions of parameters used for retries

## 2022-04-06: TR-181 Issue 2 Amendment 15 Corrigendum 1

*Tags: [v2.15.1] (TR-181), 
       [v1.11.0][TR-106-v1.11.0] (TR-106 didn't change)*

### Data Model
* Removed items that were erroneously added to the User:1 profile and
  instead added them to a new User:2 profile
* Fixed the BulkData Profile Parameter reference; it's a string, not a
  formal path reference
* Fixed the InstallDU() command's ExecutionEnvRef argument; it
  references an execution environment, not an execution unit
* Fixed the VendorConfigFile description's CWMP/USP-specific text

## 2022-01-27: [TR-181 Issue 2 Amendment 15]

*Tags: [v2.15.0] (TR-181), 
       [v1.11.0][TR-106-v1.11.0] (TR-106)*

### TR-181 Document
* Converted the document to markdown and extended the Wi-Fi
  Theory of Operation

### Data Model
* Split the XML into multiple smaller files (this is just
  housekeeping; it doesn't affect how the model is used)
* Added Device.USPAgent to the CWMP model to allow a CWMP ACS
  to configure a device for USP communications
* Allowed USP to access the EnableCWMP parameter (so a USP
  Controller can enable/disable CWMP access)
* Added Device.Routing.Babel for the RFC 8966 Babel routing
  protocol
* Added Device.DOCSIS for modeling DOCSIS 3.0 and 3.1 interfaces
* Added Device.Users.Group, Device.Users.Role and
  Device.Users.SupportedShell tables for modeling system users
* Improved the Wi-Fi data model by adding Data Elements R2
  parameters, commands and events, moving MultiAP parameters and
  commands into the Data Elements structure, and by deprecating
  AIFSN, ECWMin, ECWMax and TxOpMax
* Clarified the LockoutPeriod and Retries ControllerTrust
  parameters that impact how the RequestChallenge() and
  ChallengeResponse() data model commands handle failed attempts
* Clarified bulk data profile, threshold and periodic statistics USP
  Controller permissions: only the USP Controller that created the
  profile will receive the corresponding events
* Added a bulk data profile ForceCollection() command
* Added support for a new bulk data collection mechanism that
  utilizes MQTT as the transport protocol
* Removed old bulk data collection protocols (Streaming and File)
  from the USP data model (they don't apply to USP)
* Updated the IPLayerCapacity() test to support TR-472 Issue 2
* Added an enumeration to indicate when a Boot! event was due to a
  factory reset
* Added an enumeration to distinguish encrypted and unencrypted
  USP MQTT WebSocket connections
* Added an Order parameter to provide guidance to USP Agents on
  which MTP to use when communicating with a Controller
* Clarified that Device.Optical is intended for generic optical
  interfaces and is not intended to model anything specific to
  IEEE or ITU-T PON technologies (objects specific to such
  technologies may be added in future versions of the data model)
* Clarified the meaning and usage of the Device.Ethernet.Interface
  and Device.Ethernet.Link objects (also allowed the Ethernet
  Link MACAddress parameter to be written)
* Improved (and made more consistent) the marking of (and
  explanation of) deprecated items, and how such items should
  progress from being deprecated to obsoleted to deleted
* Added a Baseline:4 profile that doesn't include
  Device.LANConfigSecurity (it relates to the now-deprecated
  TR-064 LAN management protocol)
* Many minor improvements to object and parameter descriptions
* Many minor improvements to object, parameter, command and event
  descriptions
* Replaced the non-standard dmr:version attribute with the version
  attribute (which supports three levels of version)
* Switched to DMR (data model report) schema v1.0, which supports
  multi-line paragraphs, and wrapped all lines to 80 characters
  maximum

## 2020-11-17: TR-181 Issue 2 Amendment 14 Corrigendum 1

*Tag: [v2.14.1]*

### Data Model
* Fixed Device.LocalAgent.Subscription.{i}.ID constraints
* Removed duplicate remarks about CWMP BOOTSTRAP from descriptions
* Fixed typos

## 2020-11-05: [TR-181 Issue 2 Amendment 14]

*Tag: [v2.14.0]*

### TR-181 Document
* Added Appendix XXI 5G - Wireline Wireless Convergence and Appendix
  XXII Data Elements

### Data Model
* Added WWC (5G Wireline Wireless Convergence), PDU (Protocol Data
  Unit) and FWE (5G Wireline wireless Encapsulation) top-level objects
* Updated Cellular object to be applicable to 5G Residential Gateways
* Extended support for TR-471 IP-layer metrics, including new IP-layer
  capacity test
* Supported LAN device time-based access-control
* Various Wi-Fi improvements

## 2019-09-13: [TR-181 Issue 2 Amendment 13]

*Tag: [v2.13.0]*

### TR-181 Document
* Unified text for CWMP and USP support
* Updated references

### Data Model
* Added support for WFA Data Elements
* Added support for Multi AP
* Added support for WPA3 and 802.11ax
* Added support for MQTT 5.0
* Added support for Packet capture diagnostics
* Updates for TR-369 MQTT support
* Added support for IoT Data model

## 2018-03-16: [TR-181 Issue 2 Amendment 12]

*Tag: [v2.12.0]*

### TR-181 Document
* Added Appendix I, II, IV from TR-157a10 as Appendix XVII, XVIII
  and XIX
* Added Appendix XX BASAPM and LMAP Theory of Operations
* Added Annex H from TR-069a5 as Annex C

### Data Model
* Added TR-069a6 support
* Added USP Local agent support (TR-369)
* Added Firmware Image support
* Added Ethernet Link Aggregation Group
* Added additional Wi-Fi and WAN statistics
* Added support for Two-Way Active Measurement Protocol (TWAMP)
  reflector
* Added support for Layer Two Tunneling Protocol version 3 (L2TPv3)
* Added support for Virtual eXtensible Local Area Network (VXLAN)
  tunnels
* Added support for Broadband Access Service Attributes and
  Performance Metrics measurement test framework (BASAPM)
* Added support for Large-Scale Measurement of Broadband Performance
  (LMAP)

## 2016-07-18: [TR-181 Issue 2 Amendment 11]

*Tag: [v2.11.0]*

### TR-181 Document
* Added G.fast theory of operation

### Data Model
* LED status model
* Layer 2 tunnel support for IP diagnostics model
* DSL G.fast model
* Management Frame Protection support for WiFi model
* WPS 2.0 support for WiFi model
* User interface toggle
* User interface messaging model
* ConnectionRequest HTTP service toggle
* DNS fallback support for XMPP connections

## 2016-07-01: TR-181 Issue 2 Corrigendum 2

*Tag: [v2.0.2]*

* Removed *SSID* unique key from *WiFi.SSID* object

## 2015-11-09: [TR-181 Issue 2 Amendment 10]

*Tag: [v2.10.0]*

### TR-181 Document
* No changes to the specification

### Data Model
* MQTT model
* Bulk data over HTTP
* DNS Server updates
* New diagnostics state

## 2015-11-01: TR-181 Amendment 7

*Tag: [v1.7.0]*

### Data Model
Incorporated new components from [TR-157 Amendment 10]

* Update Bulk Data Collection for HTTP Transport

## 2014-12-01: TR-181 Issue 2 Amendment 9

*Tag: [v2.9.0]*

### Data Model
* Added support for WiFi MAC Address Filtering
* Fixes for Traceroute
* Added IEEE 1905 data model
* Incorporated new components from TR-143 Amendment 1

## 2014-09-08: [TR-181 Issue 2 Amendment 8]

*Tag: [v2.8.0]*

### TR-181 Document
* Updated Annex B on tunneling
* Added GRE, MAP and PCP theory of operation

### Data Model
* Added LLDP and HTIP home network topology discovery parameters
* Added G.997.1-2012 DSL parameters
* Added various WiFi parameters (associated device statistics,
  retry limits, reports, QoS)
* Added IPv6-related IP diagnostics parameters, and other minor changes
* Updated G.hn data model to align with G.9962
* Added GRE and MAP data models
* Added PCP data model
* Added Cellular interface data model

## 2014-09-01: TR-181 Amendment 6

*Tag: [v1.6.0]*

### Data Model
Incorporated new components from TR-157 Amendment 9

* Added Inform Parameters table to ManagementServer
* Added *HTIP* Component to *DeviceInfo* containing HTIP related
  parameters
* Updated the *UPnP* component for HTIP parameters

## 2013-11-11: [TR-181 Issue 2 Amendment 7]

*Tag: [v2.7.0]*

### TR-181 Document
* Added ZigBee and Provider Bridge theory of operation
* Added backup/restore theory of operation

### Data Model
* Added ZigBee and Provider Bridge data models
* Also added additional WiFi statistics, and other minor changes

## 2013-11-01: TR-181 Amendment 5

*Tag: [v1.5.0]*

### Data Model
Incorporated new components from TR-157 Amendment 8

* Addition of *MS_StandbyPolicy*, *XMPP* and *XMPPConnReq*
  components; other minor updates

## 2012-11-01: [TR-181 Issue 2 Amendment 6]

*Tag: [v2.6.0]*

### TR-181 Document
* Added support M2M SCL Administration as an Appendix

### Data Model

## 2012-11-01: TR-181 Amendment 4

*Tag: [v1.4.0]*

### Data Model
Incorporated new components from TR-157 Amendment 7

* Addition of *DNS_SD* component; other minor updates

## 2012-05-01: [TR-181 Issue 2 Amendment 5]

*Tag: [v2.5.0]*

### TR-181 Document
* Added Tunneling Annex and IPsec Appendix

### Data Model
* Added support for IPsec and bulk data collection

## 2012-05-01: TR-181 Amendment 3

*Tag: [v1.3.0]*

### Data Model
Incorporated new components from TR-157 Amendment 6

* Addition of *BulkDataCollection* component

## 2011-11-01: TR-181 Issue 2 Amendment 4

*Tag: [v2.4.0]*

### Data Model
* Added support for G.hn and Optical interfaces
* Additional WiFi parameters

## 2011-11-01: TR-181 Amendment 2

*Tag: [v1.2.0]*

### Data Model
Incorporated new components from [TR-157 Amendment 5]

Incorporated Femto components from [TR-262]

* Addition of *Location*, *FaultManagement* and *Security* components

## 2011-07-01: TR-181 Issue 2 Amendment 3

*Tag: [v2.3.0]*

### Data Model
* Added support for proxy management and alias-based addressing

## 2011-07-01: TR-181 Amendment 1

*Tag: [v1.1.0]*

### Data Model
Incorporated new components from TR-157 Amendment 4

* Support for CWMP Proxy Management and Alias-Based Addressing

## 2011-02-01: [TR-181 Issue 2 Amendment 2]

*Tag: [v2.2.0]*

### TR-181 Document
* Added IPv6 and Firewall Appendices

### Data Model
* Added support for IPv6 and Firewall

## 2010-11-01: TR-181 Issue 2 Amendment 1

*Tag: [v2.1.0]*

### Data Model
* Added support for Software Module Management

## 2010-11-01: TR-181 Issue 2 Corrigendum 1

*Tag: [v2.0.1]*

### Data Model
* Fixed various ranges and defaults
* Removed non interface object *Alias* parameters from profiles

## 2010-05-01: [TR-181 Issue 2]

*Tag: [v2.0.0]*

### TR-181 Document
* Original

### Data Model
* Original

## 2010-02-01: [TR-181 Issue 1]

*Tag: [v1.0.0]*

### TR-181 Document
* Original

### Data Model
* Minor clarifications and additions

[TR-106-v1.11.0]: https://github.com/BroadbandForum/data-model-template/releases/tag/v1.11.0
[TR-106-v1.12.0]: https://github.com/BroadbandForum/data-model-template/releases/tag/v1.12.0
[TR-106-v1.13.0]: https://github.com/BroadbandForum/data-model-template/releases/tag/v1.13.0
[TR-106-v1.14.0]: https://github.com/BroadbandForum/data-model-template/releases/tag/v1.14.0
[TR-157 Amendment 10]: https://www.broadband-forum.org/download/TR-157_Amendment-10.pdf
[TR-157 Amendment 5]: https://www.broadband-forum.org/download/TR-157_Amendment-5.pdf
[TR-181 Issue 1]: https://www.broadband-forum.org/download/TR-181_Issue-1.pdf
[TR-181 Issue 2]: https://www.broadband-forum.org/download/TR-181_Issue-2.pdf
[TR-181 Issue 2 Amendment 10]: https://www.broadband-forum.org/download/TR-181_Issue-2_Amendment-10.pdf
[TR-181 Issue 2 Amendment 11]: https://www.broadband-forum.org/download/TR-181_Issue-2_Amendment-11.pdf
[TR-181 Issue 2 Amendment 12]: https://www.broadband-forum.org/download/TR-181_Issue-2_Amendment-12.pdf
[TR-181 Issue 2 Amendment 13]: https://www.broadband-forum.org/download/TR-181_Issue-2_Amendment-13.pdf
[TR-181 Issue 2 Amendment 14]: https://www.broadband-forum.org/download/TR-181_Issue-2_Amendment-14.pdf
[TR-181 Issue 2 Amendment 15]: https://www.broadband-forum.org/download/TR-181_Issue-2_Amendment-15.pdf
[TR-181 Issue 2 Amendment 16]: https://www.broadband-forum.org/download/TR-181_Issue-2_Amendment-16.pdf
[TR-181 Issue 2 Amendment 17]: https://www.broadband-forum.org/download/TR-181_Issue-2_Amendment-17.pdf
[TR-181 Issue 2 Amendment 18]: https://www.broadband-forum.org/download/TR-181_Issue-2_Amendment-18.pdf
[TR-181 Issue 2 Amendment 2]: https://www.broadband-forum.org/download/TR-181_Issue-2_Amendment-2.pdf
[TR-181 Issue 2 Amendment 5]: https://www.broadband-forum.org/download/TR-181_Issue-2_Amendment-5.pdf
[TR-181 Issue 2 Amendment 6]: https://www.broadband-forum.org/download/TR-181_Issue-2_Amendment-6.pdf
[TR-181 Issue 2 Amendment 7]: https://www.broadband-forum.org/download/TR-181_Issue-2_Amendment-7.pdf
[TR-181 Issue 2 Amendment 8]: https://www.broadband-forum.org/download/TR-181_Issue-2_Amendment-8.pdf
[TR-262]: https://www.broadband-forum.org/download/TR-262.pdf
[v1.0.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v1.0.0
[v1.1.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v1.1.0
[v1.2.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v1.2.0
[v1.3.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v1.3.0
[v1.4.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v1.4.0
[v1.5.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v1.5.0
[v1.6.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v1.6.0
[v1.7.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v1.7.0
[v2.0.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.0.0
[v2.0.1]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.0.1
[v2.0.2]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.0.2
[v2.1.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.1.0
[v2.2.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.2.0
[v2.3.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.3.0
[v2.4.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.4.0
[v2.5.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.5.0
[v2.6.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.6.0
[v2.7.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.7.0
[v2.8.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.8.0
[v2.9.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.9.0
[v2.10.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.10.0
[v2.11.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.11.0
[v2.12.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.12.0
[v2.13.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.13.0
[v2.14.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.14.0
[v2.14.1]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.14.1
[v2.15.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.15.0
[v2.15.1]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.15.1
[v2.16.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.16.0
[v2.17.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.17.0
[v2.18.0]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.18.0
[v2.18.1]: https://github.com/BroadbandForum/device-data-model/releases/tag/v2.18.1
