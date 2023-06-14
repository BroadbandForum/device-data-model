# IPv6 Data Modeling Theory of Operation {.appendix .same-file}

The Device:2 data model supports IPv6 (introduced in Amendment 2) via various IPv6-specific objects and parameters that are designed to be used with other IP version neutral and IPv4-specific objects and parameters. This Appendix briefly reviews all the relevant objects and parameters, and then presents some example configurations.

## IPv6 Overview

The IETF published RFC 2460 [@RFC2460], Internet Protocol, *Version 6 (IPv6) Specification* in 1998. Since then, it has published a variety of RFCs to create a suite of protocols (and extensions to protocols) for operating, managing, and configuring IPv6 networks and devices. In addition there are RFCs that document transition mechanisms (to transition from IPv4 to IPv6) and best current practices (that describe which RFCs to implement depending on what a device is or needs to do).

The Broadband Forum has published several Technical Reports describing IPv6 architectures and device requirements. Specifically, TR-124 Issue 2 [@TR-124] includes IPv6 requirements for Residential Gateways (RGs), TR-177 [@TR-177] describes migration to IPv6 in the context of TR-101 [@TR-101], and TR-187 [@TR-187] describes an architecture for IPv6 for PPP Broadband Access. The Device:2 IPv6 Data Model is intended to ensure that TR-069 [@TR-069] or USP [@TR-369] managed End Devices, RGs, and other Network Infrastructure Devices can be managed and configured, consistent with the requirements listed in these documents.

The basic elements of IPv6 data modeling involve information on IPv6 capabilities, and enabling those capabilities on devices and device interfaces (see *[Enabling IPv6]*), configuring addresses, prefixes , and configuration protocols on upstream and downstream interfaces (see *[Configuring Upstream IP Interfaces]* and *[Configuring Downstream IP Interfaces]*), interacting with other devices on the Local Area Network (LAN) (see *[Device Interactions]*), and configuring IPv6 routing and forwarding information (see *[Configuring IPv6 Routing and Forwarding*]).

Configuration protocols include Neighbor Discovery (ND; RFC 4861 [@RFC4861]) and DHCPv6 (RFC 3315 [@RFC3315]). Neighbor Discovery includes several messages that are important to configuration, including Router Solicitation (RS) [sent by devices looking for routers], Router Advertisement (RA) [sent by routers to other devices on the LAN], Neighbor Solicitation (NS) [used to identify if any other device on the LAN is using the same IPv6 address, and used to see if previously detected devices are still present; the latter is called Neighbor Unreachability Detection (NUD)], and Neighbor Advertisement (NA) [used to respond to a NS sent to one of the device's IPv6 addresses]. These messages are central to the stateless address autoconfiguration (SLAAC) mechanism described in RFC 4862 [@RFC4862]. SLAAC is expected to be the primary means of IPv6 address configuration for devices inside a home network. RFC 4191 [@RFC4191] extended the RA message to support a RouteInformation option. RFC 6106 [@RFC6106] extended the RA message to support sending Recursive DNS Servers (RDNSS) information for DNS configuration.

DHCPv6 can also be used for IPv6 address provisioning, through its IA_NA option. DHCPv6 was extended by RFC 3633 [@RFC3633] to provide the IA_PD option for delegating IPv6 prefixes to routers (that the routers can then use to provide IPv6 addresses to other devices on the LAN, or to further sub-delegate to other routers inside the LAN). Both IA_NA and IA_PD require the DHCPv6 server to maintain state for these assignments (since they have lifetimes, can expire, and require renewal). DHCPv6 can also supply a variety of stateless configuration options, including recursive DNS server information. RGs can have both DHCPv6 client and server, and it may be desirable for some of the stateless options to be passed through from the client to the server.

Interfaces that support IPv6 will have more than one IPv6 address. IPv6 interfaces are always required to have a link-local address (described in RFC 4862 [@RFC4862]). Other IPv6 addresses may be acquired through SLAAC, DHCPv6 IA_NA, or they may be statically configured. Routers may acquire prefixes (for use with address assignment in the LAN) from DHCPv6 IA_PD, static configuration, or by generating their own Unique Local Address (ULA) prefixes from a self-generated ULA Global ID (RFC 4193 [@RFC4193]).

Because of the various IPv6 addresses that devices can have, maintaining good routing table and IPv6 forwarding information is critical. Route information can be obtained from received RA messages (both by noting that the sending device is a router, and from the RouteInformation option) as well as other protocols.

## Data Model Overview

This Theory of Operations focuses on data modeling for the purpose of establishing upstream and downstream connectivity for TR-069 [@TR-069] or USP [@TR-369] enabled devices, and for configuration of IPv6-related parameters. This is not an exhaustive description of data model changes made in support of IPv6, and only intends to describe the working of elements that are not readily obvious.

The following tables are key to IPv6 data modeling:

::: emphasis
* IP
    * IP.Interface
        * IP.Interface.IPv6Address
        * IP.Interface.IPv6Prefix
* PPP.Interface
* Routing.Router
    * Routing.Router.IPv6Forwarding
    * Routing.RouteInformation.InterfaceSetting
* NeighborDiscovery.InterfaceSetting
* RouterAdvertisement.InterfaceSetting
    * RouterAdvertisement.InterfaceSetting.Option
* Hosts.Host
* DHCPv6
* DHCPv6.Client
    * DHCPv6.Client.Server
    * DHCPv6.Client.SentOption
    * DHCPv6.Client.ReceivedOption
* DHCPv6.Server
    * DHCPv6.Server.Pool
        * DHCPv6.Server.Pool.Client
            * DHCPv6.Server.Pool.Client.IPv6Address
            * DHCPv6.Server.Pool.Client.IPv6Prefix
            * DHCPv6.Server.Pool.Client.Option
        * DHCPv6.Server.Pool.Option
:::

Note that the following tables have separate theories of operation, and are not described again here:

::: emphasis
* IPv6rd.InterfaceSetting
* DSLite.InterfaceSetting
:::

*Firewall* includes some IPv6 elements that are not described, since it does not interact with tables other than an association with *IP.Interface*. As such, its IPv6 usage is considered straightforward, and explanation is considered unnecessary.

Similarly, *DNS.Client.Server* is not described.

Use of DHCPv6 elements of *Bridging.Filter* are also not described, as there is no conceptual difference between how they are used and how DHCPv4 elements are used.

@fig:relationship-of-protocols-to-data-model shows the relationship of IPv6 configuration messages to devices and the tables used to configure the protocol messages and store the responses.

![Relationship of Protocols to Data Model](/images/relationship-of-protocols-to-data-model.png)

@fig:internal-relationships-of-ipv6-addresses-and-prefixes shows internal relationships of parts of the data model involved in IPv6 addresses and IPv6 prefixes. The following sections describe in greater detail how these various tables are populated.

![Internal Relationships of IPv6 Addresses and Prefixes](/images/internal-relationships-of-ipv6-addresses-and-prefixes.png)

## Enabling IPv6

The *IP IPv6Capable* parameter indicates whether the device supports IPv6. *IP.IPv6Enable* controls enabling IPv6 is on the device. IPv6 can only be enabled on a device with *IPv6Capable*=*true*. *IPv6Status* indicates whether IPv6 has been enabled on the device.

Per TR-124 Issue 2 [@TR-124], the upstream interface can be configured to establish an IPv6 connection either over PPP (PPPoA or PPPoE) or directly over Ethernet. Both mechanisms require an *IP.Interface* instance with *IPv6Enable* set to *true*. When using PPP, a *PPP.Interface* instance must have *IPv6CPEnable* set to *true* (which can only occur if *PPP.SupportedNCPs* includes *IPv6CP* in its list of Network Control Protocols (NCPs)).

Enabling IPv6 on specific downstream or upstream interfaces requires that *IP.Interface* instances have *IPv6Enable* set to *true*.

## Configuring Upstream IP Interfaces

An upstream IP Interface is an *IP.Interface* that is associated with an *Upstream=true* physical interface, via the *InterfaceStack*. Every *Upstream=true* physical interface that will be used to support routed IPv6 traffic will have an upstream IP Interface for each distinct upstream IPv6 connection that is established over that physical interface.

Upstream IPv6 connections can be established on an upstream IP Interface either through internal logic (for well-known addresses and the link-local address), static configuration, or dynamically through received Router Advertisement (RA) messages or DHCPv6 client behaviors. Received RA and DHCPv6 messages can contain configuration information for more than just establishing the upstream IP interface. The data model allows for the storage of additional configuration information sent by one of these protocols.

### Configuration Messages Sent Out the Upstream IP Interface

The device can be configured to send Router Solicitation and DHCPv6 client messages out an upstream IP interface.

* A device that is configured to send Router Solicitation messages out an upstream IP interface will have a *NeighborDiscovery.InterfaceSetting* instance whose *Interface* is the related upstream *IP.Interface*, and with *RSEnable=true*.

* A device that is configured to send DHCPv6 client requests out an upstream IP interface will have a *DHCPv6.Client* instance whose *Interface* is the related upstream *IP.Interface*, and with *Enable=true*. *RequestAddresses* indicates whether IA_NA is to be requested, *RequestPrefixes* indicates whether IA_PD is to be requested, and *RequestedOptions* identifies which other options are to be requested. *DHCPv6.Client.Server*, *DHCPv6.Client.SentOption*, and *DHCPv6.Client.ReceivedOption* are populated as appropriate, as described in the data model.

### IPv6 Prefixes

*IP.Interface.IPv6Prefix* instances on upstream IP interfaces are used to store all prefixes received in RA messages on the interface (with *Origin* of *RouterAdvertisement*), prefixes delegated by DHCPv6 IA_PD (with *Origin* of *PrefixDelegation*), statically configured IPv6 prefixes (but only the ones that are intended to be sub-divided for use on downstream interfaces with sent RA messages or DHCPv6 server functions), and *WellKnown* prefixes, as appropriate (such as certain well-known multicast prefixes, where the device joins the multicast group for that prefix on that interface).

*RouterAdvertisement* prefixes with *Autonomous=true* are used to create an *IPv6Address* instance on the interface, and can be used to create routes in *Routing.Router.IPv6Forwarding.* *RouterAdvertisement* prefixes with *OnLink=true* can also be used to create routes in *Routing.Router.IPv6Forwarding.* Prefixes received in a RA RouteInformation option are not stored with the interface, but rather in an instance of *Routing.RouteInformation.InterfaceSetting.*

*PrefixDelegation* prefixes and *Static* prefixes are not directly used on the upstream IP interface. They are prefixes that are intended to be sub-divided for use on the device's downstream interfaces, either by the DHCPv6 server for IA_NA or IA_PD, sent in RA messages (as on-link and/or autonomous prefixes), or used to self-assign addresses to other interfaces on the device. Non IA_PD prefixes received in DHCPv6 options are not stored with the upstream IP interface. Prefixes for static routes are entered directly into *Routing.Router.IPv6Forwarding* and do not need to also have upstream IP interface *IPv6Prefix* entries.

It is often desirable to configure information about delegated prefixes before they have been delegated (for example, that a particular /64 of that prefix is to be used on the downstream interface for address assignment). In order to allow for the referencing of not-yet-existing-but-expected delegated prefixes, an *Origin=Static* *IPv6Prefix* entry is created of *Type=PrefixDelegation*. When a device receives a delegated prefix, it is expected to first look for such Static entries and populate them with the delegated prefix information, instead of creating a new *IPv6Prefix* instance of *Origin=PrefixDelegation*. How these references are configured on downstream interfaces is discussed in *[IPv6 Prefixes]*.

### IPv6 Addresses

IPv6 link-local addresses on an upstream IP Interface are generally internally generated, although they can be configured statically, when necessary (when the internal default link-local address fails Duplicate Address Detection (DAD)). A properly configured upstream *IP.Interface* instance will have a *IP.Interface.IPv6Address* instance for its link-local address. This will have *Origin* of *AutoConfigured* (if internally generated per RFC 4862 [@RFC4862]) or *Static* (if statically configured by some management entity).

IPv6 addresses that are created via stateless address autoconfiguration (SLAAC), as defined in RFC 4862 (from received RA messages that contain prefix(es) with *Autonomous=true*) cause the device to create a *IP.Interface.IPv6Address* instance with *Origin* of *AutoConfigured.* IPv6 addresses assigned via DHCPv6 IA_NA cause the device to create a *IP.Interface.IPv6Address* instance with *Origin* of *DHCPv6*. Statically created IPv6 addresses will have *Origin* of *Static*. If any of these addresses are Global Unicast Addresses (GUA), they can be used to originate and terminate traffic to/from either the downstream or the upstream, independent of which physical interface they are associated with.

## Configuring Downstream IP Interfaces

A downstream IP Interface is a *IP.Interface* that is associated with an *Upstream=false* physical interface, via the *InterfaceStack*. As noted in the definition of the *Upstream* parameter, "For an End Device, *Upstream* will be *true* for all interfaces." This means that only RGs or (possibly) other Network Infrastructure Devices will have downstream IP Interfaces.

### IPv6 Prefixes

*IP.Interface.IPv6Prefix* instances on downstream IP interfaces are used to store all prefixes that are either on-link for that downstream IP interface, or can be delegated to or used by routers connected to that downstream IP interface. On-link prefixes include prefixes that are included in Router Advertisement (RA) messages for SLAAC (Autonomous prefixes), those used as DHCPv6 address pools, and those used for static addressing by End Devices that connect to that downstream IP interface.

The device can have a Unique Local Address (ULA) /48 prefix defined in *IP.ULAPrefix*. In general, the device will generate its own ULA /48 prefix, although this value could be configured directly by the user or through TR-069 [@TR-069] or USP [@TR-369]. If ULA addressing is to be supported on a downstream interface, then *IP.Interface.ULAEnable* must be *true*. The ULA /48 prefix can be associated with any downstream IP interface, and can be sub-divided to provide ULA prefixes on multiple downstream IP interfaces (by assigning longer prefixes from the ULA /48 prefix to these downstream IP interfaces). When the device creates a ULA prefix on a downstream interface, it creates an *IPv6Prefix* instance with *Origin=AutoConfigured*.

RGs that are configured to act as routers need to know which prefixes to include in their sent Router Advertisement (RA) messages and to be used in DHCPv6 server pools. These prefixes need to be associated with the downstream IP interface for those *RouterAdvertisement.InterfaceSetting* and *DHCPv6.Server.Pool* instances. These prefixes can be statically configured on the downstream IP interface, or they can be automatically generated from prefixes on an upstream IP interface with *Origin* of *PrefixDelegation* or *Static*, or they can be generated from the ULA /48 prefix (as described in the previous paragraph). Prefixes that are automatically (by internal code) derived from prefixes on an upstream IP interface with *Origin* of *PrefixDelegation* or *Static*, will point to that upstream IP interface in *ParentPrefix* and have *Origin* of *Child*.

It is often desirable to pre-configure information about prefixes on a downstream IP interface that are to be derived from delegated (on the upstream interface) prefixes. This will need to be done before that prefix has been delegated and without knowledge of what that prefix will be. A derived-from-not-yet-existing-but-expected-delegated-prefix downstream IP interface *IPv6Prefix* entry will have *Origin=Static* and *Type=Child*, and will have *ParentPrefix* pointing to an upstream IP interface *IPv6Prefix* instance (that is *Origin=Static* and *Type= PrefixDelegation*). When a device receives a delegated prefix and populates the upstream IP interface IPv6Prefix instance, and needs to generate downstream IP interface prefixes from that delegated prefix, it is expected to first look for such *Static* *Child* entries and populate them with the derived prefix information, instead of creating a new *IPv6Prefix* instance of *Origin=Child*. How the referenced parent prefixes are configured on upstream IP interfaces is discussed in *[IPv6 Prefixes]*.

If the device receives RA messages on downstream IP interfaces, autonomous and on-link prefixes in such received RA message Prefix Information options can also be recorded in *IP.Interface.IPv6Prefix*. At this time, there is no additional guidance for using the information in these RA messages received on downstream interfaces. They are simply stored, to provide information about other devices in the home network.

### IPv6 Addresses

As with the upstream IP interfaces, IPv6 link-local addresses on a downstream IP interface are generally internally generated, although they can be configured statically, when necessary (when the internal default link-local address fails Duplicate Address Detection (DAD)). A properly configured downstream IPv6 connection will have a *IP.Interface* instance with a *IP.Interface.IPv6Address* instance for its link-local address. This will have *Origin* of *AutoConfigured* (if internally generated per RFC 4862 [@RFC4862]) or *Static* (if statically configured by some management entity).

If the device has a Unique Local Address (ULA) prefix that it is advertising and/or sub-delegating to devices on the LAN, then it needs to have at least one address from this prefix assigned to downstream IP interfaces that expect to support usage of the ULA.

If the device did not receive an address on its upstream IP interface (from DHCPv6 or SLAAC), but it was delegated a prefix (DHCPv6 IA_PD), then it is expected to assign an address from a prefix (*Origin=Child* or *Type=Child*) derived from that delegated prefix to one of its non-upstream interfaces. This *IPv6Address* instance will have *Origin* of *AutoConfigured*. This address can be used for originating and terminating messages to and from either the downstream or the upstream interfaces.

## Device Interactions

The RG can interact with other devices on the LAN both by actively sending messages with or without configuration information, and by passively listening to messages received from other devices. End Devices can interact with other devices on the LAN by passively listening to messages received from other devices and by actively performing Neighbor Unreachability Detection (NUD) to determine if previously detected devices are still reachable.

### Active Configuration

To assist in the automated configuration of other devices on the LAN, an RG sends Router Advertisement (RA) messages and DHCPv6 server messages. This function is associated with downstream IP interfaces, and thus does not apply to End Devices. As noted in the above section on downstream IP interfaces, only RGs or other infrastructure devices will have downstream IP interfaces.

* *RouterAdvertisement.InterfaceSetting* instances whose *Interface* is the related downstream *IP.Interface*, with *Enable=true*, define the content of RA messages that get sent on the downstream IP interface. The *RouterAdvertisement.InterfaceSetting* instance will include references to *IPv6Prefix* entries in the associated downstream IP interface. These are *IPv6Prefix* entries of *Origin=Child* or *Origin=Static*.

* *DHCPv6.Server.Pool* instances whose *Interface* is the related downstream *IP.Interface*, with *Enable=true*, contain information for filtering DHCPv6 client requests, and identify the IPv6 prefix(es) (references to *IPv6Prefix* entries of the associated downstream IP interface) that provide the pool of IPv6 addresses and IPv6 prefixes available for assignment from this pool. Information on soliciting clients (including assigned addresses and prefixes and received option information) is stored in *DHCPv6.Server.Pool*.C*lient*. Additional options that are sent to soliciting clients is stored in *DHCPv6.Server.Pool*.O*ption*. The *PassthroughClient* parameter in this table identifies whether the value of this option is simply passed through from a DHCPv6 client on an upstream interface.

As noted above, both *RouterAdvertisement.InterfaceSetting* and *DHCPv6.Server.Pool* have references to *IPv6Prefix* entries. The *ManualPrefixes*, *IANAManualPrefixes* and *IAPDManualPrefixes* parameters allow for configuration (through TR-069 [@TR-069], USP [@TR-369], user interface, or other means) of prefixes that are to be included in RA messages, and to be used in deriving DHCPv6 IA_NA and IA_PD offers, respectively. The *Prefixes*, *IANAPrefixes*, and *IAPDPrefixes* parameters list all of the prefixes that the devices actually does include in these messages. Since the \**ManualPrefixes* entries may point to *IPv6Prefix* entries that are not enabled, it is possible that not all of those will be included in these parameters' lists. In addition to the \**ManualPrefix* entries, these lists may also include references to prefixes that the device creates or uses automatically in RA messages or for deriving DHCPv6 IA_NA or IA_PD offers.

There is some flexibility in the modeling of ULA IA_PD prefixes. It is not required to model the ULA /48 prefix in an *IPv6Prefix* instance. If the ULA /48 is not represented in an IPv6Prefix instance and *ULAEnable* is *true* for a downstream interface and *IAPDEnable* is *true* for a *DHCPv6.Server.Pool* instance, then it can be assumed that the device will sub-delegate prefixes from the ULA /48 prefix. Alternately, the ULA /48 can be included as an *AutoConfigured* prefix in a downstream interface, and that *IPv6Prefix* instance can be referenced in *IAPDPrefixes* in the *DHCPv6.Server.Pool* instance. It is also possible to manually create a *Static* longer-than-/48 prefix from the ULA prefix in a downstream interface. This *Static* prefix can then be referenced in *IAPDManualPrefix* for a *DHCPv6.Server.Pool* instance for that interface.

For IA_PD, there is one additional parameter: *IAPDAddLength*. This parameter is configured to recommend how many bits should be added to an *IAPDPrefixes* prefix to create a delegated prefix offer.

### Monitoring

All devices can monitor and record information from messages sent by other devices.

* Information received in Neighbor Solicitation (NS) and Neighbor Advertisement (NA) messages sent by other devices is recorded in *Hosts.Host.*

* In order to actively solicit information from other devices on the LAN, the device can have a *NeighborDiscovery.InterfaceSetting* instance whose *Interface* is the related downstream *IP.Interface*, and with *NUDEnable=true*. To determine whether there are other routers connected to the LAN that are behaving like IPv6 routers to this same LAN segment, this *InterfaceSetting* can also have  *RSEnable=true*. However, it is not recommended that routers do this until there is better guidance available for routers that co-exist in a peered environment on the same LAN.

## Configuring IPv6 Routing and Forwarding

IPv6 routing information is stored in instances of *Routing.Router.IPv6Forwarding.* This information can in part be derived from Router Advertisement (RA) messages, either directly from the address of the router sending the RA, or from RA RouteInformation (RFC 4191 [@RFC4191]) options that may be included in the message. *Routing.RouteInformation.InterfaceSetting* instances record received RA RouteInformation options.

Following is an example of how a typical RG (one upstream and one downstream interface, with delegated prefix and IA_NA address, and ULA enabled) might be configured. The corresponding data model is shown below the figure. Not all parameters are shown, and objects and parameters that the Controller is likely to have explicitly created or written are shown in **bold face** (some of these settings might alternatively be present in the factory default configuration).

![Example IPv6 RG Configuration](/images/typical-rg-ipv6-configuration.png)

::: code
| # IP
| IP.
|     IPv6Capable = true
|     **IPv6Enable = true**
|     IPv6Status = "Enabled"
|     ULAPrefix = fd01:2345:6789::/48   # typically generated by CPE
|
| # Router Solicitation (Upstream IP interface)
| NeighborDiscovery.
|     **Enable = true**
|     **InterfaceSetting.1.**
|     **Enable = true**
|     **Interface = IP.Interface.1**
|     **RSEnable = true**
|
| # DHCPv6 Client (Upstream IP interface)
| **DHCPv6.Client.1**
|     **Enable = true**
|     **Interface = IP.Interface.1**
|     **RequestAddresses = true**
|     **RequestPrefixes = true**
|
| # Upstream IP interface
| # - Assumes DHCPv6 IA_PD will be 1080:0:0:800::/56 (this is NOT known at
| #   configuration time).
| # - Assumes RA(PI) will be 2001:0DB8::/64 (this is NOT known at configuration
| #   time)
| # - Assumes link-layer address is 55:44:33:22:11:00
| #   [Section 4/RFC 2464[@RFC2464]], [Section 4.1/RFC 5072[@RFC5072]]
| IP.Interface.1
|     **Enable = true**
|     **IPv6Enable = true**
|
|     # Upstream IP interface IPv6 prefixes
|     # - Assumes that the WellKnown Link Local fe80::/10 prefix not modeled
|     **IPv6Prefix.1**
|         **Enable = true**
|         Prefix = 1080:0:0:800::/56    # DHCPv6(IA_PD) [RFC 3633[@RFC3633]]
|         Origin = "Static"
|         **StaticType =** "**PrefixDelegation**"
|
|     # Upstream IP interface IPv6 addresses (LL, GUA)
|     IPv6Address.1
|         Enable = true
|         IPAddress = fe80::5544:33ff:fe22:1100
|         Origin = "AutoConfigured"    # LL
|         Prefix = ""
|     IPv6Address.2
|         Enable = true
|         IPAddress = 1080:0:0:700::
|         Origin = "DHCPv6"            # GUA (from IA_NA [RFC 3315[@RFC3315]])
|         Prefix = ""
|
| # Downstream IP interface
| # - Assumes link-layer address is 00:11:22:33:44:55 [Section 4/RFC 2464[@RFC2464]]
| IP.Interface.2
|     **Enable = true**
|     **IPv6Enable = true**
|     **ULAEnable = true**
|
|     # Downstream IP interface IPv6 prefixes
|     **IPv6Prefix.1**
|         **Enable = true**
|         Prefix = 1080:0:0:800::/64
|         Origin = "Static"
|         **StaticType = "Child"** # IA_PD /64 (for lcl, RA and IA_NA)
|         **ParentPrefix = IP.Interface.1.IPv6Prefix.1**
|         **ChildPrefixBits = 0:0:0:00::/64**
|     **IPv6Prefix.2**
|         **Enable = true**
|         Prefix = 1080:0:0:810::/60
|         Origin = "Static"
|         **StaticType = "Child"**     # IA_PD /60 (for IA_PD)
|         **ParentPrefix = IP.Interface.1.IPv6Prefix.1**
|         **ChildPrefixBits = 0:0:0:10::/60**
|     IPv6Prefix.3
|         Enable = true
|         Prefix = fd01:2345:6789::/48
|         Origin = "AutoConfigured"    # ULA /48
|     IPv6Prefix.4
|         Enable = true
|         Prefix = fd01:2345:6789:0::/64
|         Origin = "AutoConfigured"    # ULA /64 (for lcl, RA and IA_NA)
|     IPv6Prefix.5
|         Enable = true
|         Prefix = 2001:0db9::/60      # RA(PI) [RFC 4861[@RFC4861]]
|         Origin = "RouterAdvertisement" # from peer router
|         Autonomous = true
|         OnLink = true
|
|     # Downstream IP interface IPv6 addresses (LL, GUA?, ULA)
|     IPv6Address.1
|         Enable = true
|         IPAddress = fe80::0011:22ff:fe33:4455
|         Origin = "AutoConfigured"    # LL
|         Prefix = ""
|     IPv6Address.2
|         Enable = false               # have upstream GUA so disabled
|         IPAddress = 1080:0:0:800::
|         Origin = "AutoConfigured"    # GUA (from IA_PD /64)
|         Prefix = IP.Interface.2.IPv6Prefix.1
|     IPv6Address.3
|         Enable = true
|         IPAddress = fd01:2345:6789::0011:22ff:fe33:4455
|         Origin = "AutoConfigured"    # ULA (from ULA /64)
|         Prefix = IP.Interface.2.IPv6Prefix.4
|
| # Router Advertisement (Downstream IP interface)
| RouterAdvertisement.
|     **Enable = true**
|     **InterfaceSetting.1**
|         **Enable = true**
|         **Interface = IP.Interface.2**
|         **ManualPrefixes = IP.Interface.2.IPv6Prefix.2**
|
| # DHCPv6 server (Downstream IP interface)
| DHCPv6.Server.
|     **Enable = true**
|     **Pool.1**
|         **Enable = true**
|         **Interface = IP.Interface.2**
|         **<filter criteria>**
|         **IANAManualPrefixes = IP.Interface.2.IPv6Prefix.1**
|         **IAPDManualPrefixes = IP.Interface.1.IPv6Prefix.1,**
|                              **IP.Interface.2.IPv6Prefix.2**
|         **IAPDADDLength = 4**
:::

