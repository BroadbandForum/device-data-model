# 3GPP NAS Theory of Operation {.appendix .same-file}

This section discusses the Theory of Operation for RGs using 3GPP NAS signalling. This includes both the cellular and 5G fixed interfaces using CWMP or USP and the supporting `Device.Cellular` and `Device.SessionManagement` objects.

## Overview

The addition of a cellular interface to a residential gateway has become more commonplace in recent years. In particular, hybrid and Fixed Wireless Access (FWA) devices are increasingly offered by service providers. 
With increased usage comes a more diverse set of use cases, all of which drive the need for a set of cellular objects better aligned with the overall TR-181 model.

An RG utilizing interfaces with NAS signalling brings with it a completely different way of operation. This is a direct consequence of features such as:

* Control User Plane Separation (CUPS)
* Multiple IP sessions over a PHY
* 3GPP QoS
* Hybrid Access (Fixed and Cellular)
* Network Slicing

The above features are supported by the TR-181 data model using new data model elements comprising:

* Interface stack layer to support 5G Fixed Encapsulation (5WE)
* Objects to describe registration and session management.
* Integration with existing TR-181 elements

## Concepts
### 3GPP Generations - 2, 3, 4 and 5G
| Generation | Standard | Features                          | Release year
|------------|----------|-----------------------------------|-------------
| 1G         | NMT, AMPS| Analog voice communication, no data services| Early 1980's
| 2G         | GSM, CDMA| Digital voice, SMS, basic data services (GPRS, EDGE)| Early 1990's
| 3G         | UMTS (W-CDMA), CDMA2000| Enhanced data services, mobile internet, video calls| Early 2000's
| 4G         | LTE | High-speed internet, HD video streaming, VoIP| Late 2000's
| 5G         | NR | Ultra-fast internet, low latency, IoT, enhanced mobile broadband | Late 2010's

### Control User Plane Separation (CUPS) - 4G and 5G
CUPS is integral to the 4G and 5G architectures. It starts with the segregation of control and user plane traffic at the RG and continues through to the physical separation of control and user plane network functions. The main driver for separation is to centralize control plane functions while distributing user plane functions deeper into the network. CUPS as it impacts Wireless Wireline Convergernce is documented in TR-470 Section 5.2 [@TR-470] whilst TS 23.501 [@3GPP-TS.23.501] details the architectural elements. From the perspective of a 5G-RG, CUPS has the following impacts:

* Control plane communications move from transient (DHCP and PPP LCP ) to persistent (NAS). As a result, the operator can now modify a customer session at any time rather than at the point of authorization.
* Traffic for control and user planes uses separate sessions over a common PHY.
* DHCP and DHCPv6 technically move from the control to the user plane (UPF responsibility). However, both protocols can and need to be used to deliver configuration via their options.

### Multiple Sessions - 3, 4 and 5G
One of the more significant features of using NAS signalling is the support of multiple user plane sessions. Each session can be considered a virtual circuit between the RG and the operator's network core. The terminology varies with each generation starting with PDP context for 3G through to PDU session for 5G. Each session instance can be assigned IP addresses, QoS rules and even guaranteed bit rates. This leads to applications requiring:

* Separate IP sessions.
* Preferential data paths within the operator's network.
* Traffic separation for security.
* Guaranteed bit rates for a given application.

TR-470 Section 6.2 [@TR-470] provides examples of multiple PDU scenarios for a 5G-RG.

### Quality of Service (QoS) - 3G, 4G and 5G
QoS as implemented in a 3GPP based system is heavily influenced by the needs of the radio bearer. In particular the familiar packet marking techniques such as DSCP and PCP are ineffective over radio.
Instead a focus on packet prioritization is the foundation of 3GPP QoS.

#### 3G QoS
Capabilities:
* Guaranteed and non-guaranteed bit rates
* Packets in a PDP context are mapped to a single traffic class (e.g., conversational, streaming, interactive, and background)
* Each PDP Context has its own bearer

#### 4G QoS
Capabilities:
* Guaranteed and non-guaranteed bit rates
* Increased granularity with QCI offering predefined QoS capabilities such as priorty, packet delay and error rate. In addition to the standard 3GPP defined values, operators can define their own QCI capabilities.
* Allocation and Retention Policy (ARP).
* Traffic for each QCI and ARP combination within a PDN will be mapped to its own bearer.


#### 5G QoS
Unlike the previous generations, 5G QoS marking is merely a label called a QoS Flow Indicator (QFI). End-to-end QoS as documented in TR-470 Section 5.1 [@TR-470] is a key outcome of policy. As part of PDU establishment, a set of QoS rules is supplied specific to that PDU. Consequently, the access network specifies not only the supported QFI labels but also the properties of the QoS profile. A QoS profile consists of the following properties:

* 5G QoS Identifier (5QI). Unlike a QFI, 5QI does have a defined set of properties such as priority and whether its bit rate is guaranteed.
* Allocation and Retention Policy (ARP).
* For Guaranteed Bit Rate (GBR) profiles the guaranteed and maximum upload and download bit rates.
* GBR profiles may also specify a maximum packet loss.

### Multiple Access Networks -5G

Whilst FN-RGs are perfectly capable of supporting multiple access networks, each access network operates independently with separate IP addresses and an inability to seamlessly switch traffic between them. A 5G-RG can modify a PDU and switch traffic to another supported access network and maintain all the PDU properties including IP addresses. An operator can optimize its network usage by sending policy rules to a 5G-RG, indicating the preferred access and data networks. TR-470 Section 4.4 [@TR-470] provides a more in-depth description of hybrid access.

### Network Slicing - 5G

An operator may choose to partition their network infrastructure for the purposes of resiliency or merely to optimize for a particular function such as IoT. Each instance of the partitioned network is called a network slice. Operators will provide slice information as part of URSP policy rules. Every PDU at the time of establishment must specify a network slice. Slicing is further documented in TS 23.501 Clause 5.15 [@3GPP-TS.23.501].

## Data Model elements
### Data Model
#### Device.SessionManagement - 3G, 4G and 5G
The logical connection between an RG and a data network using 3GPP technologies (FN-RG cellular and 5G-RG ALL) are considered data sessions. The Device.SessionManagement subtree describes each sessions properties together with the QoS rules specific to that access technology.

:Device.SessionManagement objects

| Object                  | Description
|-------------------------|-----------------------------------------------
| Device.SessionManagement| Base object for 3GPP sessions.
| Device.SessionManagement.Session.{i}    | Contains all the properties of a 3GPP session instance common to all generations.
| Device.SessionManagement.Session.{i}.PCO|
| Device.SessionManagement.Session.{i}.PDP| Contains all 3G specific attributes needed to establish a PDP context.
| Device.SessionManagement.Session.{i}.PDN| Contains all 4G specific attributes needed to establish a PDN session.
| Device.SessionManagement.Session.{i}.PDU| Contains all 5G specific attributes needed to establish a PDU session.
| Device.SessionManagement.Session.{i}.PDU.NetworkSlice              | Describes all the components of a Single -Network Slice Selection Assistance Information (S-NSSAI). The S-NSSAI identifies the network slice a PDU session has been established on.
| Device.SessionManagement.Session.{i}.PDU.QoSFlow.{i}               | Table of all QoS Flow Indicators (QFI) and their properties supported by the access network for this particular PDU.
| Device.SessionManagement.Session.{i}.PDU.QoSRule.{i}               | Set of rules used to select the QFI label for a given packet.
| Device.SessionManagement.Session.{i}.PDU.QoSRule.{i}.QoSRuleFilter.{i} | Table of filters to select a QoS rule. Typical filters include destination IP and ports.

![Device.WWC objects](/images/device.sessionmanagement-objects.png)

#### Device.WWC - 5G

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

#### Device.FWE - 5G

5G Wireless Wireline Convergence User Plane Encapsulation [@RFC8822] is used to separate each PDU session when multiplexed over a PHY. A Device.FWE.Link object is inserted into the interface stack, providing PDU session id as well as 5G QoS markings (QFI, RQI). This is also the level at which fixed QoS rules are applied in order to traverse access networks that do not natively support 5G QoS (QFI) markings. An instance of this object will be created by a 5G-RG whenever a PDU is established.

:Device.FWE objects

| Object                     | Description
|----------------------------|---------------------------------------------------------------------------------------
| Device.FWE                 | Base object for 5WE.
| Device.FWE.Link.{i}        | 5WE link layer table describing the link layer supporting the 5WE protocol.
| Device.FWE.Link.{i}.Stats  | Throughput statistics for this link layer

![Device.FWE objects](/images/device.fwe-objects.png)

### Interface Stack - 3G, 4G and 5G
The ability to provide multiple user sessions using 3GPP NAS signalling makes some subtle changes to how the interface stack is viewed. The most significant are the multiple PDP/PDN/PDU sessions shown in parallel but linked to a common access technology. This is not to be confused with features such as bonding as the traffic for each session is segregated on the radio interface.

All 3GPP based interface stacks require an OSI layer to segregate multiplexed traffic.
The OSI layer model (see @fig:osi-layers-and-interface-objects) represents all 3GPP technologies (Cellular and 5G fixed) at 'L2\-\-\-' and the previous 'L2\-\-' pushed down to 'L2\-\-\-'.

The scenarios below show 5G PDU examples. However, the cellular interface mapping is equally applicable for 3G PDP and 4G PDN sessions.

#### Scenario #1 - Fixed access network only

This example shows two PDU sessions using a VDSL access network. As this is a fixed service, the 5WE protocol is used to multiplex the PDU traffic over the VDSL service. NAS traffic is separate from the PDU traffic and is carried as PPPoE over the VDSL service. All LAN traffic remains unchanged on a 5G-RG.

![Fixed access only example](/images/fixed-access-only-example.png)

#### Scenario #2 - Cellular access network only

This example shows two PDU sessions using a cellular access network. In this case the 5G-RG does not to need to multiplex the PDU traffic as the cellular module handles that internally. NAS traffic does not appear in this diagram as the requests are made directly to the cellular module. Depending on the cellular module, each PDU may need to be carried over a VLAN (this has been omitted for the moment). All LAN traffic remains unchanged on a 5G-RG.

![Cellular access only example](/images/cellular-access-only-example.png)

#### Scenario #3 - Hybrid (Fixed and Cellular) access

This example shows two PDU sessions using both VDSL and cellular access networks. Either access network is capable for carrying either PDU or both. A PDU in this situation can only be carried on a single access network at a time. Fixed traffic is multiplexed using 5WE (even if only one PDU is present) whilst PDU traffic to the cellular network is multiplexed by the cellular module. NAS traffic using the PPP interface is for the fixed component only as cellular requests are made directly to the cellular module. Depending on the cellular module, each PDU may need to be carried over a VLAN (this has been omitted for the moment). All LAN traffic remains unchanged on a 5G-RG.

![Hybrid access example](/images/hybrid-access-example.png)

### Examples

There are a multitude of combinations of 3GPP generations and access technologies. The following scenarios will be explored:
* 3G PDP - Cellular - General purpose internet traffic.
* 4G PDN - Cellular - General purpose internet traffic, IMS VoIP
* 5G PDU - Cellular - General purpose internet traffic, IMS VoIP, traffic marking for VoWiFi
* 5G PDU  - Fixed - General purpose internet traffic
* 5G PDU - WWC - General purpose internet traffic, IMS VoIP, traffic marking for VoWiFi

#### Scenario #1 - 3G PDP - Cellular - General purpose internet traffic

    Device.SessionManagement.
        SessionNumberOfEntries = 1
    Device.SessionManagement.1.
        Alias = "cpe-pdp1"
        Interface = Device.IP.Interface.1
        SessionID = 1
        SessionType = IPv4v6
        APN = "provider.internet"
    Device.SessionManagement.1.PCO
        IPv6DNS = "2001:db8::1,2001:db8::2"
        IPv4DNS = "203.0.113.1,203.0.113.2"
    Device.SessionManagement.1.PDP
        TrafficClass = "Interactive"
        DownstreamMaxBitRate = 1000
        UpstreamMaxBitRate = 1000

#### Scenario #2 - 4G PDN - Cellular - General purpose internet traffic, IMS VoIP

    Device.SessionManagement.
        SessionNumberOfEntries = 3
    Device.SessionManagement.1.
        Alias = "cpe-pdn1"
        Interface = Device.IP.Interface.1
        SessionID = 1
        SessionType = IPv4v6
        APN = "provider.internet"
    Device.SessionManagement.1.PCO
        IPv6DNS = "2001:db8::1,2001:db8::2"
        IPv4DNS = "203.0.113.1,203.0.113.2"
    Device.SessionManagement.1.PDN
        QCI = 9
        DownstreamMaxBitRate = 1000
        UpstreamMaxBitRate = 1000
    Device.SessionManagement.2.
        Alias = "cpe-pdn2"
        Interface = Device.IP.Interface.2
        SessionID = 2
        SessionType = IPv4v6
        APN = "provider.ims"
    Device.SessionManagement.2.PCO
        IPv6DNS = "2001:db8::1,2001:db8::2"
        IPv4DNS = "203.0.113.1,203.0.113.2"
    Device.SessionManagement.2.PDN
        QCI = 1
        DownstreamMaxBitRate = 1000
        UpstreamMaxBitRate = 1000
    Device.SessionManagement.3.
        Alias = "cpe-pdn3"
        Interface = Device.IP.Interface.2
        SessionID = 3
        SessionType = IPv4v6
        APN = "provider.ims"
    Device.SessionManagement.2.PCO
        IPv6DNS = "2001:db8::1,2001:db8::2"
        IPv4DNS = "203.0.113.1,203.0.113.2"
    Device.SessionManagement.2.PDN
        QCI = 5
        DownstreamMaxBitRate = 1000
        UpstreamMaxBitRate = 1000


#### Scenario #3 - 5G PDU - Cellular - General purpose internet traffic, IMS VoIP, traffic marking for VoWiFi

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
    Device.SessionManagement.
        SessionNumberOfEntries = 2
    Device.SessionManagement.Session.1.
        Alias = "cpe-pdu1"
        Interface = Device.IP.Interface.1
        SessionType = IPv4v6
        SessionId = 1
        APN = "provider.internet"
    Device.SessionManagement.Session.1.PCO
        IPv6DNS = "2001:db8::1,2001:db8::2"
        IPv4DNS = "203.0.113.1,203.0.113.2"
    Device.SessionManagement.Session.1.PDU
        PTI = 63
        SSC = 1
        SessionAMBRDownlink = 100000000
        SessionAMBRUplink = 40000000
        QoSRuleNumberOfEntries = 2
        QoSFlowNumberOfEntries = 2
    Device.SessionManagement.Session.1.PDU.NetworkSlice
        SliceServiceType = "eMBB"
        SliceDifferentiator = 4
    Device.SessionManagement.Session.1.PDU.QoSRule.1.
        Alias = "cpe-pdu11"
        Identifier = 1
        Precedence = 100
        Segregation = false
        QFI = 1
        DQR = true
        FilterNumberOfEntries = 1
    Device.SessionManagement.Session.1.PDU.QoSRule.1.Filter.1.
        Alias = "cpe-pdu111"
        Direction = "bidirectional"
        Type = 1                   # Match all
    Device.SessionManagement.Session.1.PDU.QoSRule.2.
        Alias = "cpe-pdu12"
        Identifier = 2
        Precedence = 10
        Segregation = false
        QFI = 32
        DQR = true
        FilterNumberOfEntries = 1
    Device.SessionManagement.Session.1.PDU.QoSRule.2.Filter.1.
        Alias = "cpe-pdu121"
        Direction = "bidirectional"
        Type = 33                  # Destination IPv6
        Value = "2001:db8::2:1"    # VoWiFi ePDG
    Device.SessionManagement.Session.1.PDU.QoSFlow.1.
        Alias = "cpe-pdu11"
        QFI = 1
        FiveQI = 8
    Device.SessionManagement.Session.1.PDU.QoSFlow.2.
        Alias = "cpe-pdu11"
        QFI = 32
        FiveQI = 1
        GFBRUplink = 150000
        GFBRDownlink = 150000
    Device.SessionManagement.Session.2.
        Alias = "cpe-pdu2"
        Interface = Device.IP.Interface.2
        SessionType = IPv4v6
        SessionId = 6
        DNN = "provider.ims"
    Device.SessionManagement.Session.2.PDU.
        PTI = 34
        SSC = 1
        SessionAMBRDownlink = 150000
        SessionAMBRUplink = 150000
        QoSRuleNumberOfEntries = 2
        QoSFlowNumberOfEntries = 1
    Device.SessionManagement.Session.2.PCO.
        IPv6PCSCF = "2001:db8::1:1"
        IPv6DNS = "2001:db8::1,2001:db8::2"
        IPv4DNS = "203.0.113.1,203.0.113.2"
        IPv4PCSCF = "203.0.113.100"
    Device.SessionManagement.Session.2.PDU.NetworkSlice
        SliceServiceType = "eMBB"
        SliceDifferentiator = 4
    Device.SessionManagement.Session.2.PDU.QoSRule.1.
        Alias = "cpe-pdu21"
        Identifier = 1
        Precedence = 100
        Segregation = false
        QFI = 32
        DQR = true
        FilterNumberOfEntries = 1
    Device.SessionManagement.Session.2.PDU.QoSRule.1.Filter.1.
        Alias = "cpe-pdu211"
        Direction = "bidirectional"
        Type = 1            # Match all
    Device.SessionManagement.Session.2.PDU.QoSFlow.1.
        Alias = "cpe-pdu21"
        QFI = 32
        FiveQI = 1
        GFBRUplink = 150000
        GFBRDownlink = 150000

#### Scenario #4 - 5G PDU  - Fixed - General purpose internet traffic

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
    Device.SessionManagement.
        SessionNumberOfEntries = 2
    Device.SessionManagement.Session.1
        Alias = "cpe-pdu1"
        Interface = Device.IP.Interface.1
        SessionId = 1
        SessionType = IPv4v6
    Device.PDU.Session.1.PCO
        IPv6DNS = "2001:db8::1,2001:db8::2"
        IPv4DNS = "203.0.113.1,203.0.113.2"
    Device.SessionManagement.Session.1.PDU
        PTI = 63
        SSC = 1
        SessionAMBRDownlink = 100000000
        SessionAMBRUplink = 40000000
        DNN = "provider.internet"
        QoSRuleNumberOfEntries = 2
        QoSFlowNumberOfEntries = 2
    Device.SessionManagement.Session.1.PDU.NetworkSlice
        SliceServiceType = "eMBB"
        SliceDifferentiator = 4
    Device.SessionManagement.Session.1.PDU.QoSRule.1.
        Alias = "cpe-pdu11"
        Identifier = 1
        Precedence = 100
        Segregation = false
        QFI = 1
        DQR = true
        FilterNumberOfEntries = 1
    Device.SessionManagement.Session.1.PDU.QoSRule.1.Filter.1.
        Alias = "cpe-pdu111"
        Direction = "bidirectional"
        Type = 1                  # Match all
    Device.SessionManagement.Session.1.PDU.QoSRule.2.
        Alias = "cpe-pdu12"
        Identifier = 2
        Precedence = 10
        Segregation = false
        QFI = 32
        DQR = true
        FilterNumberOfEntries = 1
    Device.SessionManagement.Session.1.PDU.QoSRule.2.Filter.1.
        Alias = "cpe-pdu121"
        Direction = "bidirectional"
        Type = 33                  # Destination IPv6
        Value = "2001:db8::2:1"    # VoWiFi ePDG
    Device.SessionManagement.Session.1.PDU.QoSFlow.1.
        Alias = "cpe-pdu11"
        QFI = 1
        FiveQI = 8
    Device.SessionManagement.Session.1.PDU.QoSFlow.2.
        Alias = "cpe-pdu11"
        QFI = 32
        FiveQI = 1
        GFBRUplink = 150000
        GFBRDownlink = 150000
    Device.SessionManagement.Session.2.
        Alias = "cpe-pdu2"
        Interface = Device.IP.Interface.2
        SessionId = 6
        SessionType = IPv4v6
    Device.SessionManagement.Session.2.PCO
        IPv6PCSCF = "2001:db8::1:1"
        IPv6DNS = "2001:db8::1,2001:db8::2"
        IPv4DNS = "203.0.113.1,203.0.113.2"
        IPv4PCSCF = "203.0.113.100"
    Device.SessionManagement.Session.2.PDU
        PTI = 34
        SSC = 1
        SessionAMBRDownlink = 150000
        SessionAMBRUplink = 150000
        DNN = "provider.ims"
        QoSRuleNumberOfEntries = 2
        QoSFlowNumberOfEntries = 1
    Device.SessionManagement.Session.2.PDU.NetworkSlice
        SliceServiceType = "eMBB"
        SliceDifferentiator = 4
    Device.SessionManagement.Session.2.PDU.QoSRule.1.
        Alias = "cpe-pdu21"
        Identifier = 1
        Precedence = 100
        Segregation = false
        QFI = 32
        DQR = true
        FilterNumberOfEntries = 1
    Device.SessionManagement.Session.2.PDU.QoSRule.1.Filter.1.
        Alias = "cpe-pdu211"
        Direction = "bidirectional"
        Type = 1            # Match all
    Device.SessionManagement.Session.2.PDU.QoSFlow.1.
        Alias = "cpe-pdu21"
        QFI = 32
        FiveQI = 1
        GFBRUplink = 150000
        GFBRDownlink = 150000
    Device.FWE.
        LinkNumberOfEntries = 1
    Device.FWE.Link.1.
        Alias = "cpe-fwe1"
        Name = "cpe-fwe1"
        Status = "Up"
        LowerLayers = "Device.Ethernet.5"
    Device.FWE.Link.1.Stats
        BytesSent = 478945789
        BytesReceived = 589545478

#### Scenario #5 - 5G PDU - WWC - General purpose internet traffic, IMS VoIP, traffic marking for VoWiFi

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
    Device.SessionManagement.
        SessionNumberOfEntries = 2
    Device.SessionManagement.Session.1.
        Alias = "cpe-pdu1"
        Interface = Device.IP.Interface.1
        SessionType = IPv4v6
        SessionId = 1
        APN = "provider.internet"
    Device.SessionManagement.Session.1.PCO
        IPv6DNS = "2001:db8::1,2001:db8::2"
        IPv4DNS = "203.0.113.1,203.0.113.2"
    Device.SessionManagement.Session.1.PDU
        PTI = 63
        SSC = 1
        SessionAMBRDownlink = 100000000
        SessionAMBRUplink = 40000000
        QoSRuleNumberOfEntries = 2
        QoSFlowNumberOfEntries = 2
    Device.SessionManagement.Session.1.PDU.NetworkSlice
        SliceServiceType = "eMBB"
        SliceDifferentiator = 4
    Device.SessionManagement.Session.1.PDU.QoSRule.1.
        Alias = "cpe-pdu11"
        Identifier = 1
        Precedence = 100
        Segregation = false
        QFI = 1
        DQR = true
        FilterNumberOfEntries = 1
    Device.SessionManagement.Session.1.PDU.QoSRule.1.Filter.1.
        Alias = "cpe-pdu111"
        Direction = "bidirectional"
        Type = 1                   # Match all
    Device.SessionManagement.Session.1.PDU.QoSRule.2.
        Alias = "cpe-pdu12"
        Identifier = 2
        Precedence = 10
        Segregation = false
        QFI = 32
        DQR = true
        FilterNumberOfEntries = 1
    Device.SessionManagement.Session.1.PDU.QoSRule.2.Filter.1.
        Alias = "cpe-pdu121"
        Direction = "bidirectional"
        Type = 33                  # Destination IPv6
        Value = "2001:db8::2:1"    # VoWiFi ePDG
    Device.SessionManagement.Session.1.PDU.QoSFlow.1.
        Alias = "cpe-pdu11"
        QFI = 1
        FiveQI = 8
    Device.SessionManagement.Session.1.PDU.QoSFlow.2.
        Alias = "cpe-pdu11"
        QFI = 32
        FiveQI = 1
        GFBRUplink = 150000
        GFBRDownlink = 150000
    Device.SessionManagement.Session.2.
        Alias = "cpe-pdu2"
        Interface = Device.IP.Interface.2
        SessionType = IPv4v6
        SessionId = 6
        DNN = "provider.ims"
    Device.SessionManagement.Session.2.PDU.
        PTI = 34
        SSC = 1
        SessionAMBRDownlink = 150000
        SessionAMBRUplink = 150000
        QoSRuleNumberOfEntries = 2
        QoSFlowNumberOfEntries = 1
    Device.SessionManagement.Session.2.PCO.
        IPv6PCSCF = "2001:db8::1:1"
        IPv6DNS = "2001:db8::1,2001:db8::2"
        IPv4DNS = "203.0.113.1,203.0.113.2"
        IPv4PCSCF = "203.0.113.100"
    Device.SessionManagement.Session.2.PDU.NetworkSlice
        SliceServiceType = "eMBB"
        SliceDifferentiator = 4
    Device.SessionManagement.Session.2.PDU.QoSRule.1.
        Alias = "cpe-pdu21"
        Identifier = 1
        Precedence = 100
        Segregation = false
        QFI = 32
        DQR = true
        FilterNumberOfEntries = 1
    Device.SessionManagement.Session.2.PDU.QoSRule.1.Filter.1.
        Alias = "cpe-pdu211"
        Direction = "bidirectional"
        Type = 1            # Match all
    Device.SessionManagement.Session.2.PDU.QoSFlow.1.
        Alias = "cpe-pdu21"
        QFI = 32
        FiveQI = 1
        GFBRUplink = 150000
        GFBRDownlink = 150000
    Device.FWE.
        LinkNumberOfEntries = 1
    Device.FWE.Link.1.
        Alias = "cpe-fwe1"
        Name = "cpe-fwe1"
        Status = "Up"
        LowerLayers = Device.Ethernet.5
    Device.FWE.Link.1.Stats
        BytesSent = 478945789
        BytesReceived = 589545478
