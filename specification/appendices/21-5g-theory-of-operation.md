# 5G Theory of Operation {.appendix .same-file}
::: note
The theory of operation defined in this Appendix is DEPRECATED in favor of the “3GPP NAS” theory of operation defined in Appendix XXV.
The 3GPP NAS theory of operation takes a more wholistic approach and is inclusive of 3G, 4G and 5G rather than the previous focus on 5G WWC
:::

This section discusses the Theory of Operation for 5G Wireline Wireless Convergence using CWMP or USP and the supporting Device.WWC, Device.PDU and Device.FWE objects.

## Overview

A 5G-RG brings with it a completely different way of operation. This is a direct consequence of features such as:

* Control User Plane Separation (CUPS)
* Multiple IP sessions over a PHY
* 5G QoS
* Hybrid Access (Fixed and Cellular)
* Network Slicing

The above features are supported by the TR-181 data model using new data model elements comprising:

* Interface stack layer to support 5G Fixed Encapsulation (5WE)
* Objects to describe registration and session management.
* Integration with existing TR-181 elements

## Architecture

The 5G converged core represents a significant departure from the TR-101 [@TR-101] based architecture currently used to support residential gateway access. Most noteworthy is the alignment with 3GPP architectural principles. It is important to understand the two deployment scenarios for the 5G core---Integration and Interworking.

**Integration** -- All wireline traffic transits the AGF (Access Gateway Function) before entering the 3GPP-defined 5G core. Both 5G-RGs and FN-RGs may use the AGF natively. In the case of a 5G-RG, the AGF will support 5G NAS and PDU (multiple IP sessions) transport. Whilst a FN-RG is limited to TR-101 and the NAS and PDU (single IP session) is emulated by the AGF on behalf of the FN-RG, RGs may use wireline, wireless or both access networks. However, in the case of multiple access networks, all must use 5G NAS + PDU if ATSSS is to be supported.

**Interworking** -- All wireline traffic uses the current TR-101-based solutions (BNG + AAA). The FMIF emulates all the TR-101 control plane functions needed by the BNG and converts to 5G NAS. Current thinking is that user plane traffic will continue to be handled by the BNG. Note: A 5G-RG reverts to FN-RG mode when connected to a BNG. The interworking scenario is based around a standard FN-RG and has zero impact on the TR-181 data model

In the diagram below the elements in green, namely 5G-RG, AGF and FMIF, are BBF-defined.

![5G Converged Core Network](/images/5g-converged-core-network.png)

The complete 5G architecture is documented in the 3GPP 23.501 [@3GPP-TS.23.501] standard. BBF has produced TR-470 [@TR-470] documenting the Wireline Wireless Convergence architecture. Shown below is a simplified architecture with the network functions and interfaces relevant to supporting a 5G-RG.

![5G Architecture](/images/5g-architecture.png)

### Network Functions

| Network Function      | Plane    | Description
|-----------------------|----------|-----------------------------------------------------------------
| W-5GAN: Wireline\
5G Access Network | Both     | Functionally equivalent to a 3GPP RAN. It incorporates both an AGF and one or more TR-101-based access networks. These networks may be owned by the service provider or provided by a third party.
| AUSF: Authentication Server Function | Control  | Support the AMF authentication function by making the actual authentication decisions.
| AMF: Access and\
Mobility Management Function | Control  | Can be considered to be the entry point to the control plane. From the perspective of a 5G-RG, the AMF processes all N1 traffic and thus is the frontend for authentication and the establishment of PDU sessions.
| NSSF: Network\
Slice Selection Function | Control  | Selects the network slice instance servicing the 5G-RG. The AGF will use the NSSF to choose an AMF at the time of registration.
| PCF: Policy\
Control Function | Control  | Responsible for control plane policy rules. In particular, supports the AMF to provide policy rules as part of registration.
| SMF: Session\
Management Function | Control  | The SMF acts as a controller for the UPF. Major responsibilities include DHCP (server or relay), QoS handling and user plane policy enforcement (downstream traffic shaping).
| UDM: Unified Data\
Management | Control  | Responsible for subscription data used by other network functions to authenticate and provide subscription-based policy.
| UPF: User Plane\
Function | User     | Provides the packet routing and forwarding to the data network. Other necessary functions include usage, QoS management, user plane policy and being the anchor point for multipath traffic.

## Concepts

### Control User Plane Separation (CUPS)

CUPS is integral to the entire 5G architecture. It starts with the segregation of control and user plane traffic at the 5G-RG and continues through to the physical separation of control and user plane network functions. The main driver for separation is to centralize control plane functions whilst distributing user plane functions deeper into the network. CUPS is documented in TR-470 Section 5.2 [@TR-470] whilst TS 23.501 [@3GPP-TS.23.501] details the architectural elements. From the perspective of a 5G-RG, CUPS has the following impacts:

* Control plane communications move from transient (DHCP and PPP LCP ) to persistent (NAS). As a result, the operator can now modify a customer session at any time rather than at the point of authorization.
* Traffic for control and user planes uses separate sessions over a common PHY.
* DHCP and DHCPv6 technically move from the control to the user plane (UPF responsibility). However, both protocols can and need to be used to deliver configuration via their options.

### Policy

One of the new design principles brought by 5G to the residential gateway is that of policy. Previous generations of mobile devices have been users of policy but 5G takes it to a new level. Policy and the role of the PCF are documented in TS 23.503 [@3GPP-TS.23.503].

**So, what is policy?**\
The simplest way to think of policy is as a set of per-service rules sent to the 5G-RG by the network operator. This allows the operator to dynamically control how a 5G-RG connects to a 5G network in terms of network slices, data networks and QoS with application level granularity.

**How is it delivered?**\
Policy is managed by the Policy Control Function (PCF), which provides policy in two distinct phases. At the time of registration, a routing policy table (URSP) is provided upon successful authentication. When a PDU session is created, URSP provides the necessary network slice and data network information. The second phase of policy is learnt upon successful PDU creation, where a set of QoS rules is provided.

### Multiple PDU sessions

One of the more significant features of a 5G-RG is the support of multiple PDU sessions. Each PDU can be considered to be a virtual circuit between a 5G-RG and a UPF instance. A PDU instance can be assigned IP addresses, QoS rules and even guaranteed bit rates. This leads to applications requiring:

* Separate IP sessions.
* Preferential data paths within the operator's network.
* Traffic separation for security.
* Guaranteed bit rates for a given application.

TR-470 Section 6.2 [@TR-470] provides examples of multiple PDU scenarios for a 5G-RG.

### 5G QoS

Unlike the more familiar QoS markings such as DSCP or Ethernet priority, 5G QoS marking is merely a label called a QoS Flow Indicator (QFI). End-to-end QoS as documented in TR-470 Section 5.1 [@TR-470] is a key outcome of policy. As part of PDU establishment, a set of QoS rules is supplied specific to that PDU. Consequently, the access network specifies not only the supported QFI labels but also the properties of the QoS profile. A QoS profile consists of the following properties:

* 5G QoS Identifier (5QI). Unlike a QFI, 5QI does have a defined set of properties such as priority and whether its bit rate is guaranteed.
* Allocation and Retention Policy (ARP).
* For Guaranteed Bit Rate (GBR) profiles the guaranteed and maximum upload and download bit rates.
* GBR profiles may also specify a maximum packet loss.

### Data Network Name (DNN)

One of the benefits of multiple PDU sessions is the ability to have preferred data paths within the network. A 5G core achieves this using DNNs mapped to dedicated UPFs. A DNN is always specified when establishing a PDU and the 5G-RG learns the preferred DNN through URSP policy.

### Multiple Access Networks

Whilst FN-RGs are perfectly capable of supporting multiple access networks, each access network operates independently with separate IP addresses and an inability to seamlessly switch traffic between them. A 5G-RG can modify a PDU and switch traffic to another supported access network and maintain all the PDU properties including IP addresses. An operator can optimize its network usage by sending policy rules to a 5G-RG, indicating the preferred access and data networks. TR-470 Section 4.4 [@TR-470] provides a more in-depth description of hybrid access.

### Network Slicing

An operator may choose to partition their network infrastructure for the purposes of resiliency or merely to optimize for a particular function such as IoT. Each instance of the partitioned network is called a network slice. Operators will provide slice information as part of URSP policy rules. Every PDU at the time of establishment must specify a network slice. Slicing is further documented in TS 23.501 Clause 5.15 [@3GPP-TS.23.501].

## Data Model Elements

### Interface Stack

User plane traffic on a 5G-RG is carried as part of a PDU session carrying L3 traffic (usually IPv4 or IPv6). Whilst cellular networks have native methods for separating PDU traffic, fixed access networks do not. Operators have a choice of two multiplexing strategies, both of which require co-ordination between the 5G-RG and AGF:

* VLAN: Each PDU uses a separate VLAN with the VLAN id as the session identifier.
* 5WE: An encapsulation method designed to carry multiplexed PDU traffic over existing (non 5G) access networks [@RFC8822].

The OSI layer model (see @fig:osi-layers-and-interface-objects) now has 5WE (Device.FWE.Link in the model) at 'L2\-\-\-' and the previous 'L2\-\-' pushed down to 'L2\-\-\-'.

#### Scenario #1 - Fixed access network only

This example shows two PDU sessions using a VDSL access network. As this is a fixed service, the 5WE protocol is used to multiplex the PDU traffic over the VDSL service. NAS traffic is separate from the PDU traffic and is carried as PPPoE over the VDSL service. All LAN traffic remains unchanged on a 5G-RG.

![Fixed access only example](/images/fixed-access-only-example.png)

#### Scenario #2 - Cellular access network only

This example shows two PDU sessions using a cellular access network. In this case the 5G-RG does not to need to multiplex the PDU traffic as the cellular module handles that internally. NAS traffic does not appear in this diagram as the requests are made directly to the cellular module. Depending on the cellular module, each PDU may need to be carried over a VLAN (this has been omitted for the moment). All LAN traffic remains unchanged on a 5G-RG.

![Cellular access only example](/images/cellular-access-only-example.png)

#### Scenario #3 - Hybrid (Fixed and Cellular) access

This example shows two PDU sessions using both VDSL and cellular access networks. Either access network is capable for carrying either PDU or both. A PDU in this situation can only be carried on a single access network at a time. Fixed traffic is multiplexed using 5WE (even if only one PDU is present) whilst PDU traffic to the cellular network is multiplexed by the cellular module. NAS traffic using the PPP interface is for the fixed component only as cellular requests are made directly to the cellular module. Depending on the cellular module, each PDU may need to be carried over a VLAN (this has been omitted for the moment). All LAN traffic remains unchanged on a 5G-RG.

![Hybrid access example](/images/hybrid-access-example.png)

### Data Model

#### Device.WWC

The relationship between a 5G-RG and the available access networks is represented by the Device.WWC object tree. All objects are read only and are intended for service assurance purposes.

:Device.WWC objects

| Object                                  | Description
|-----------------------------------------|--------------------------------------------------------------------------
| Device.WWC                              | Base object for Wireline Wireless Convergence. The controller can use this object to learn the supported 5G features and whether the 5G-RG is operating in 5G mode
| Device.WWC.AccessNetwork                | Each table entry describes a single access network. The entire table is built by the 5G-RG upon startup. The primary purpose is to show the registration and connectivity status of each access network. Typically, a 5G-RG would register on each available access network. A minimum of one access network must be in the CM-CONNECTED state in order to support N1 messaging
| Device.WWC.AccessNetwork.GUTI           | A 5G Globally Unique Temporary Identity (GUTI) securely identifies an CPE by keeping the permanent User Equipment (UE identifier (IMSI) hidden. This identity is globally unique and assigned by the AMF at the time of registration.
| Device.WWC.URSP                         | User equipment Route Selection Policy (URSP) is a table of rules used to determine which network slice and data network to route a PDU over. Typically, a 5G-RG would search the URSP table in precedence order matching the traffic descriptor types against the service it was setting up. For example, a 5G-RG would search for 'connection capabilities' matching 'ims' in order to establish a dedicated PDU session for telephony
| Device.WWC.URSP.{i}.TrafficDescriptor   | A set of rules for a given precedence that must be matched in order to select a router in the form of data network and slice. Selection criteria range from destination IP addresses to connection capabilities
| Device.WWC.URSP.{i}.TrafficDescriptor.{i}.RouteSelectionDescriptor | Provides a table of data networks and network slices used in PDU establishment. Table entries are used in precedence order until a successful PDU session is established. See TS 23.503 Annex A [@3GPP-TS.23.503] for an example URSP rule traversal
| Device.WWC.URSP.{i}.TrafficDescriptor.{i}.RouteSelectionDescriptor.{i}.NetworkSlice | Describes all the components of a Single-Network Slice Selection Assistance Information (S-NSSAI). A S-NSSAI identifies the network slice a PDU session will be established on

![Device.WWC objects](/images/device.wwc-objects.png)

#### Device.PDU

The logical connection between the 5G-RG and data network is the Protocol Data Unit (PDU). The Device.PDU subtree describes each PDU session's properties together with the QoS rules specific to that PDU session.

:Device.PDU objects

| Object                                           | Description
|--------------------------------------------------|-----------------------------------------------------------------
| Device.PDU                                       | Base object for PDU sessions.
| Device.PDU.Session.{i}                           | Contains all the properties of a PDU session instance, ranging from maximum bitrate through to assigned network slice.
| Device.PDU.Session.{i}.PCO                       | Policy Configuration Options (PCO) is an optional set of configuration parameters supplied by the network at the request of the 5G-RG.
| Device.PDU.Session.{i}.NetworkSlice              | Describes all the components of a Single -Network Slice Selection Assistance Information (S-NSSAI). The S-NSSAI identifies the network slice a PDU session has been established on.
| Device.PDU.Session.{i}.QoSFlow.{i}               | Table of all QoS Flow Indicators (QFI) and their properties supported by the access network for this particular PDU.
| Device.PDU.Session.{i}.QoSRule.{i}               | Set of rules used to select the QFI label for a given packet.
| Device.PDU.Session.{i}.QoSRule.{i}.QoSRuleFilter.{i} | Table of filters to select a QoS rule. Typical filters include destination IP and ports.

![Device.PDU objects](/images/device.pdu-objects.png)

#### Device.FWE

5G Wireless Wireline Convergence User Plane Encapsulation [@RFC8822] is used to separate each PDU session when multiplexed over a PHY. A Device.FWE.Link object is inserted into the interface stack, providing PDU session id as well as 5G QoS markings (QFI, RQI). This is also the level at which fixed QoS rules are applied in order to traverse access networks that do not natively support 5G QoS (QFI) markings. An instance of this object will be created by a 5G-RG whenever a PDU is established.

:Device.FWE objects

| Object                     | Description
|----------------------------|---------------------------------------------------------------------------------------
| Device.FWE                 | Base object for 5WE.
| Device.FWE.Link.{i}        | 5WE link layer table describing the link layer supporting the 5WE protocol.
| Device.FWE.Link.{i}.Stats  | Throughput statistics for this link layer

![Device.FWE objects](/images/device.fwe-objects.png)

### Examples

Each example shows a 5G-RG with two PDU sessions. The first is for general purpose internet traffic and the second for IMS VoIP. Each PDU session has a default QoS rule matching the intended use. The general internet PDU also has rule to mark VoWiFi traffic with the same QFI as IMS traffic.

#### Scenario #1 - Fixed access network only

    Device.WWC.
        Capabilities = "FN-RG,5G-RG,W-5GAN"
        Mode = "5G-RG"
        Status = "5G-RG"
        AccessNetworkNumberOfEntries = 1
        URSPNumberOfEntries = 2
    Device.WWC.AccessNetwork.1.
        Alias = "cpe-fixed"
        Name = "fixed"
        Interface = Device.Ethernet.5
        RegistrationStatus = "RM-REGISTERED"
        ConnectionStatus = "CM_CONNECTED"
        AccessNetworkType = "W-5GAN"
    Device.WWC.AccessNetwork.1.GUTI
        PLMN = 50501
        AMFid = 65601
        TMSI = 60340039
    Device.WWC.URSP.1.          # Default traffic rule
        Alias = "cpe-ursp1"
        Precedence = 100
        TrafficDescriptorNumberOfEntries = 1
    Device.WWC.URSP.1.TrafficDescriptor.1.
        Alias = "cpe-ursp11"
        Type = 1                # Match all traffic
        Value = ""
        RouteSelectionDescriptorNumberOfEntries = 1
    Device.WWC.URSP.1.TrafficDescriptor.1.RouteSelectionDescriptor.1.
        Alias = "cpe-ursp111"
        Precedence = 100
        SSC = 1
        DNN = "provider.internet"
        PDUSessionType = "IPv4v6"
        AccessType = "Non-3GPP access"
    Device.WWC.URSP.1.TrafficDescriptor.1.RouteSelectionDescriptor.1.NetworkSlice
        SliceServiceType = "eMBB"
    Device.WWC.URSP.2.           # VoUP traffic rule
        Alias = "cpe-ursp2"
        Precedence = 10
        TrafficDescriptorNumberOfEntries = 1
    Device.WWC.URSP.2.TrafficDescriptor.1.
        Alias = "cpe-ursp21"
        Type = 144               # Connection Capability Type
        Value = "1"              # IMS
        RouteSelectionDescriptorNumberOfEntries = 1
    Device.WWC.URSP.2.TrafficDescriptor.1.RouteSelectionDescriptor.1.
        Alias = "cpe-ursp211"
        Precedence = 100
        SSC = 1
        DNN = "provider.ims"
        PDUSessionType = "IPv6"
        AccessType = "Non-3GPP access"
    Device.WWC.URSP.2.TrafficDescriptor.1.RouteSelectionDescriptor.1.NetworkSlice
        SliceServiceType = "eMBB"
    Device.PDU.
        SessionNumberOfEntries = 2
    Device.PDU.Session.1.
        Alias = "cpe-pdu1"
        Interface = Device.IP.Interface.1
        SessionId = 1
        PTI = 63
        SSC = 1
        SessionAMBRDownlink = 100000000
        SessionAMBRUplink = 40000000
        DNN = "provider.internet"
        QoSRuleNumberOfEntries = 2
        QoSFlowNumberOfEntries = 2
    Device.PDU.Session.1.PCO
        IPv6DNS = "2001:db8::1,2001:db8::2"
    IPv4DNS = "203.0.113.1,203.0.113.2"
    Device.PDU.Session.1.NetworkSlice
        SliceServiceType = "eMBB"
        SliceDifferentiator = 4
    Device.PDU.Session.1.QoSRule.1.
        Alias = "cpe-pdu11"
        Identifier = 1
        Precedence = 100
        Segregation = false
        QFI = 1
        DQR = true
        FilterNumberOfEntries = 1
    Device.PDU.Session.1.QoSRule.1.Filter.1.
        Alias = "cpe-pdu111"
        Direction = "bidirectional"
        Type = 1                  # Match all
    Device.PDU.Session.1.QoSRule.2.
        Alias = "cpe-pdu12"
        Identifier = 2
        Precedence = 10
        Segregation = false
        QFI = 32
        DQR = true
        FilterNumberOfEntries = 1
    Device.PDU.Session.1.QoSRule.2.Filter.1.
        Alias = "cpe-pdu121"
        Direction = "bidirectional"
        Type = 33                  # Destination IPv6
        Value = "2001:db8::2:1"    # VoWiFi ePDG
    Device.PDU.Session.1.QoSFlow.1.
        Alias = "cpe-pdu11"
        QFI = 1
        FiveQI = 8
    Device.PDU.Session.1.QoSFlow.2.
        Alias = "cpe-pdu11"
        QFI = 32
        FiveQI = 1
        GFBRUplink = 150000
        GFBRDownlink = 150000
    Device.PDU.Session.2.
        Alias = "cpe-pdu2"
        Interface = Device.IP.Interface.2
        SessionId = 6
        PTI = 34
        SSC = 1
        SessionAMBRDownlink = 150000
        SessionAMBRUplink = 150000
        DNN = "provider.ims"
        QoSRuleNumberOfEntries = 2
        QoSFlowNumberOfEntries = 1
    Device.PDU.Session.2.PCO
        IPv6PCSCF = "2001:db8::1:1"
        IPv6DNS = "2001:db8::1,2001:db8::2"
        IPv4DNS = "203.0.113.1,203.0.113.2"
        IPv4PCSCF = "203.0.113.100"
    Device.PDU.Session.2.NetworkSlice
        SliceServiceType = "eMBB"
        SliceDifferentiator = 4
    Device.PDU.Session.2.QoSRule.1.
        Alias = "cpe-pdu21"
        Identifier = 1
        Precedence = 100
        Segregation = false
        QFI = 32
        DQR = true
        FilterNumberOfEntries = 1
    Device.PDU.Session.2.QoSRule.1.Filter.1.
        Alias = "cpe-pdu211"
        Direction = "bidirectional"
        Type = 1            # Match all
    Device.PDU.Session.2.QoSFlow.1.
        Alias = "cpe-pdu21"
        QFI = 32
        FiveQI = 1
        GFBRUplink = 150000
        GFBRDownlink = 150000
    Device.FWE.
        LinkNumberOfEntries
    Device.FWE.Link.1.
        Alias = "cpe-fwe1"
        Name = "cpe-fwe1"
        Status = "Up"
        LowerLayers = "Device.Ethernet.5"
    Device.FWE.Link,1,Stats
        BytesSent = 478945789
        BytesReceived = 589545478

#### Scenario #2 - Cellular access network only

    Device.WWC.
        Capabilities = "FN-RG,5G-RG,NG-RAN,E-UTRAN"
        Mode = "5G-RG"
        Status = "5G-RG"
        AccessNetworkNumberOfEntries = 1
        URSPNumberOfEntries = 2
    Device.WWC.AccessNetwork.1.
        Alias = "cpe-cellular"
        Name = "cellular"
        Interface = Device.Cellular.Interface.1
        RegistrationStatus = "RM-REGISTERED"
        ConnectionStatus = "CM_CONNECTED"
        AccessNetworkType = "NG-RAN"
    Device.WWC.AccessNetwork.1.GUTI
        PLMN = 50501
        AMFid = 131137
        TMSI = 54678959
    Device.WWC.URSP.1.             # Default traffic rule
        Alias = "cpe-ursp1"
        Precedence = 100
        TrafficDescriptorNumberOfEntries = 1
    Device.WWC.URSP.1.TrafficDescriptor.1.
        Alias = "cpe-ursp11"
        Type = 1                   # Match all traffic
        Value = ""
        RouteSelectionDescriptorNumberOfEntries = 1
    Device.WWC.URSP.1.TrafficDescriptor.1.RouteSelectionDescriptor.1.
        Alias = "cpe-ursp111"
        Precedence = 100
        SSC = 1
        DNN = "provider.internet"
        PDUSessionType = "IPv4v6"
        AccessType = "3GPP access"
    Device.WWC.URSP.1.TrafficDescriptor.1.RouteSelectionDescriptor.1.NetworkSlice
        SliceServiceType = "eMBB"
    Device.WWC.URSP.2.             # VoUP traffic rule
        Alias = "cpe-ursp2"
        Precedence = 10
        TrafficDescriptorNumberOfEntries = 1
    Device.WWC.URSP.2.TrafficDescriptor.1.
        Alias = "cpe-ursp21"
        Type = 144                 # Connection Capability Type
        Value = "1"                # IMS
        RouteSelectionDescriptorNumberOfEntries = 1
    Device.WWC.URSP.2.TrafficDescriptor.1.RouteSelectionDescriptor.1.
        Alias = "cpe-ursp211"
        Precedence = 100
        SSC = 1
        DNN = "provider.ims"
        PDUSessionType = "IPv6"
        AccessType = "3GPP access"
    Device.WWC.URSP.2.TrafficDescriptor.1.RouteSelectionDescriptor.1.NetworkSlice
        SliceServiceType = "eMBB"
    Device.PDU.
        SessionNumberOfEntries = 2
    Device.PDU.Session.1.
        Alias = "cpe-pdu1"
        Interface = Device.IP.Interface.1
        SessionId = 1
        PTI = 63
        SSC = 1
        SessionAMBRDownlink = 100000000
        SessionAMBRUplink = 40000000
        DNN = "provider.internet"
        QoSRuleNumberOfEntries = 2
        QoSFlowNumberOfEntries = 2
    Device.PDU.Session.1.PCO
        IPv6DNS = "2001:db8::1,2001:db8::2"
        IPv4DNS = "203.0.113.1,203.0.113.2"
    Device.PDU.Session.1.NetworkSlice
        SliceServiceType = "eMBB"
        SliceDifferentiator = 4
    Device.PDU.Session.1.QoSRule.1.
        Alias = "cpe-pdu11"
        Identifier = 1
        Precedence = 100
        Segregation = false
        QFI = 1
        DQR = true
        FilterNumberOfEntries = 1
    Device.PDU.Session.1.QoSRule.1.Filter.1.
        Alias = "cpe-pdu111"
        Direction = "bidirectional"
        Type = 1                   # Match all
    Device.PDU.Session.1.QoSRule.2.
        Alias = "cpe-pdu12"
        Identifier = 2
        Precedence = 10
        Segregation = false
        QFI = 32
        DQR = true
        FilterNumberOfEntries = 1
    Device.PDU.Session.1.QoSRule.2.Filter.1.
        Alias = "cpe-pdu121"
        Direction = "bidirectional"
        Type = 33                  # Destination IPv6
        Value = "2001:db8::2:1"    # VoWiFi ePDG
    Device.PDU.Session.1.QoSFlow.1.
        Alias = "cpe-pdu11"
        QFI = 1
        FiveQI = 8
    Device.PDU.Session.1.QoSFlow.2.
        Alias = "cpe-pdu11"
        QFI = 32
        FiveQI = 1
        GFBRUplink = 150000
        GFBRDownlink = 150000
    Device.PDU.Session.2.
        Alias = "cpe-pdu2"
        Interface = Device.IP.Interface.2
        SessionId = 6
        PTI = 34
        SSC = 1
        SessionAMBRDownlink = 150000
        SessionAMBRUplink = 150000
        DNN = "provider.ims"
        QoSRuleNumberOfEntries = 2
        QoSFlowNumberOfEntries = 1
    Device.PDU.Session.2.PCO
        IPv6PCSCF = "2001:db8::1:1"
        IPv6DNS = "2001:db8::1,2001:db8::2"
        IPv4DNS = "203.0.113.1,203.0.113.2"
        IPv4PCSCF = "203.0.113.100"
    Device.PDU.Session.2.NetworkSlice
        SliceServiceType = "eMBB"
        SliceDifferentiator = 4
    Device.PDU.Session.2.QoSRule.1.
        Alias = "cpe-pdu21"
        Identifier = 1
        Precedence = 100
        Segregation = false
        QFI = 32
        DQR = true
        FilterNumberOfEntries = 1
    Device.PDU.Session.2.QoSRule.1.Filter.1.
        Alias = "cpe-pdu211"
        Direction = "bidirectional"
        Type = 1            # Match all
    Device.PDU.Session.2.QoSFlow.1.
        Alias = "cpe-pdu21"
        QFI = 32
        FiveQI = 1
        GFBRUplink = 150000
        GFBRDownlink = 150000

#### Scenario #3 - Hybrid (Fixed and Cellular) access

    Device.WWC.
        Capabilities = "FN-RG,5G-RG,W-5GAN"
        Mode = "5G-RG"
        Status = "5G-RG"
        AccessNetworkNumberOfEntries = 2
        URSPNumberOfEntries = 2
    Device.WWC.AccessNetwork.1.
        Alias = "cpe-fixed"
        Name = "fixed"
        Interface = Device.Ethernet.5
        RegistrationStatus = "RM-REGISTERED"
        ConnectionStatus = "CM_CONNECTED"
        AccessNetworkType = "W-5GAN"
    Device.WWC.AccessNetwork.1.GUTI
        PLMN = 50501
        AMFid = 65601
        TMSI = 60340039
    Device.WWC.AccessNetwork.2.
        Alias = "cpe-cellular"
        Name = "cellular"
        Interface = Device.Cellular.Interface.1
        RegistrationStatus = "RM-REGISTERED"
        ConnectionStatus = "CM_CONNECTED"
        AccessNetworkType = "NG-RAN"
    Device.WWC.AccessNetwork.2.GUTI
        PLMN = 50501
        AMFid = 131137
        TMSI = 54678959
    Device.WWC.URSP.1.             # Default traffic rule
        Alias = "cpe-ursp1"
        Precedence = 100
        TrafficDescriptorNumberOfEntries = 1
    Device.WWC.URSP.1.TrafficDescriptor.1.
        Alias = "cpe-ursp11"
        Type = 1                   # Match all traffic
        Value = ""
        RouteSelectionDescriptorNumberOfEntries = 1
    Device.WWC.URSP.1.TrafficDescriptor.1.RouteSelectionDescriptor.1.
        Alias = "cpe-ursp111"
        Precedence = 100
        SSC = 1
        DNN = "provider.internet"
        PDUSessionType = "IPv4v6"
        AccessType = "Non-3GPP access"
    Device.WWC.URSP.1.TrafficDescriptor.1.RouteSelectionDescriptor.1.NetworkSlice
        SliceServiceType = "eMBB"
    Device.WWC.URSP.2.             # VoUP traffic rule
        Alias = "cpe-ursp2"
        Precedence = 10
        TrafficDescriptorNumberOfEntries = 1
    Device.WWC.URSP.2.TrafficDescriptor.1.
        Alias = "cpe-ursp21"
        Type = 144                 # Connection Capability Type
        Value = "1"                # IMS
        RouteSelectionDescriptorNumberOfEntries = 1
    Device.WWC.URSP.2.TrafficDescriptor.1.RouteSelectionDescriptor.1.
        Alias = "cpe-ursp211"
        Precedence = 100
        SSC = 1
        DNN = "provider.ims"
        PDUSessionType = "IPv6"
        AccessType = "Non-3GPP access"
    Device.WWC.URSP.2.TrafficDescriptor.1.RouteSelectionDescriptor.1.NetworkSlice
        SliceServiceType = "eMBB"
    Device.PDU.
        SessionNumberOfEntries = 2
    Device.PDU.Session.1.
        Alias = "cpe-pdu1"
        Interface = Device.IP.Interface.1
        SessionId = 1
        PTI = 63
        SSC = 1
        SessionAMBRDownlink = 100000000
        SessionAMBRUplink = 40000000
        DNN = "provider.internet"
        QoSRuleNumberOfEntries = 2
        QoSFlowNumberOfEntries = 2
    Device.PDU.Session.1.PCO
        IPv6DNS = "2001:db8::1,2001:db8::2"
        IPv4DNS = "203.0.113.1,203.0.113.2"
    Device.PDU.Session.1.NetworkSlice
        SliceServiceType = "eMBB"
        SliceDifferentiator = 4
    Device.PDU.Session.1.QoSRule.1.
        Alias = "cpe-pdu11"
        Identifier = 1
        Precedence = 100
        Segregation = false
        QFI = 1
        DQR = true
        FilterNumberOfEntries = 1
    Device.PDU.Session.1.QoSRule.1.Filter.1.
        Alias = "cpe-pdu111"
        Direction = "bidirectional"
        Type = 1                   # Match all
    Device.PDU.Session.1.QoSRule.2.
        Alias = "cpe-pdu12"
        Identifier = 2
        Precedence = 10
        Segregation = false
        QFI = 32
        DQR = true
        FilterNumberOfEntries = 1
    Device.PDU.Session.1.QoSRule.2.Filter.1.
        Alias = "cpe-pdu121"
        Direction = "bidirectional"
        Type = 33                  # Destination IPv6
        Value = "2001:db8::2:1"    # VoWiFi ePDG
    Device.PDU.Session.1.QoSFlow.1.
        Alias = "cpe-pdu11"
        QFI = 1
        FiveQI = 8
    Device.PDU.Session.1.QoSFlow.2.
        Alias = "cpe-pdu11"
        QFI = 32
        FiveQI = 1
        GFBRUplink = 150000
        GFBRDownlink = 150000
    Device.PDU.Session.2.
        Alias = "cpe-pdu2"
        Interface = Device.IP.Interface.2
        SessionId = 6
        PTI = 34
        SSC = 1
        SessionAMBRDownlink = 150000
        SessionAMBRUplink = 150000
        DNN = "provider.ims"
        QoSRuleNumberOfEntries = 2
        QoSFlowNumberOfEntries = 1
    Device.PDU.Session.2.PCO
        IPv6PCSCF = "2001:db8::1:1"
        IPv6DNS = "2001:db8::1,2001:db8::2"
        IPv4DNS = "203.0.113.1,203.0.113.2"
        IPv4PCSCF = "203.0.113.100"
    Device.PDU.Session.2.NetworkSlice
        SliceServiceType = "eMBB"
        SliceDifferentiator = 4
    Device.PDU.Session.2.QoSRule.1.
        Alias = "cpe-pdu21"
        Identifier = 1
        Precedence = 100
        Segregation = false
        QFI = 32
        DQR = true
        FilterNumberOfEntries = 1
    Device.PDU.Session.2.QoSRule.1.Filter.1.
        Alias = "cpe-pdu211"
        Direction = "bidirectional"
        Type = 1            # Match all
    Device.PDU.Session.2.QoSFlow.1.
        Alias = "cpe-pdu21"
        QFI = 32
        FiveQI = 1
        GFBRUplink = 150000
        GFBRDownlink = 150000
    Device.FWE.
        LinkNumberOfEntries
    Device.FWE.Link.1.
        Alias = "cpe-fwe1"
        Name = "cpe-fwe1"
        Status = "Up"
        LowerLayers = Device.Ethernet.5
    Device.FWE.Link,1,Stats
        BytesSent = 478945789
        BytesReceived = 589545478

