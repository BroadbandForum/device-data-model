# References and Terminology {.new-page}

## Conventions

In this %bbfType%, several words are used to signify the requirements of the specification. These words are always capitalized. More information can be found in RFC 2119 [@RFC2119].

::: borderless
|                |
|----------------|--------------------------------------------------------------------------------
| **MUST**       | This word, or the term "REQUIRED", means that the definition is an absolute requirement of the specification.
| **MUST NOT**   | This phrase means that the definition is an absolute prohibition of the specification.
| **SHOULD**     | This word, or the term "RECOMMENDED", means that there could exist valid reasons in particular circumstances to ignore this item, but the full implications need to be understood and carefully weighed before choosing a different course.
| **SHOULD NOT** | This phrase, or the phrase "NOT RECOMMENDED" means that there could exist valid reasons in particular circumstances when the particular behavior is acceptable or even useful, but the full implications need to be understood and the case carefully weighed before implementing any behavior described with this label.
| **MAY**        | This word, or the term "OPTIONAL", means that this item is one of an allowed set of alternatives. An implementation that does not include this option MUST be prepared to inter-operate with another implementation that does include the option.
:::

The key words "DEPRECATED" and "OBSOLETED" in this %bbfType% are to be interpreted as defined in TR-106 [@TR-106].

## References

The following references are of relevance to this %bbfType%. At the time of publication, the editions indicated were valid. All references are subject to revision; users of this %bbfType% are therefore encouraged to investigate the possibility of applying the most recent edition of the references listed below.

A list of currently valid Broadband Forum Technical Reports is published at <https://www.broadband-forum.org>.

::: {#refs}
:::

## Definitions

The following terminology is used throughout this %bbfType%.

::: borderless
|                   |
|-------------------|----------------------------------------------------------
| **5G Residential Gateway** | A CPE that uses native 5G control plane N1 signaling.
| **ACS**           | Auto-Configuration Server. This is a component in the broadband network responsible for *CWMP* auto-configuration of the *CPE* for advanced services.
| **Agent**         | A generic term that refers (as appropriate) to either a CWMP Endpoint or to a USP Agent.
| **AGF**           | A function connecting wireline access networks to the 5GC. AGF-CP is the control plane while AGF-UP is the user plane of the AGF.
| **AMF**           | The AMF is a 5G control plane function that terminates N1 and N2. It is responsible for mobility and access related functions.
| **CPE**           | Customer Premises Equipment; refers (as appropriate) to any *CWMP*-enabled [@TR-069] or *USP*-enabled [@TR-369] device and therefore covers both Internet Gateway devices and LAN-side end devices.
| **Command**       | A named element allowing a USP Controller to execute an operation on a USP Agent. This concept does not apply to CWMP, which uses Objects and/or Parameters to simulate operations.
| **Component**     | A named collection of *Objects* and/or *Parameters* and/or Profiles that can be included anywhere within a *Data Model*.
| **Controller**    | A generic term that refers (as appropriate) to either a CWMP ACS or a USP Controller.
| **CWMP**          | *CPE* WAN Management Protocol. Defined in TR-069 [@TR-069], CWMP is a communication protocol between an *ACS* and a CWMP-enabled *CPE* that defines a mechanism for secure auto-configuration of a *CPE* and other *CPE* management functions in a common framework.
| **CWMP Endpoint** | A CWMP termination point used by a CWMP-enabled CPE for communication with the ACS*.*
| **Data Model**    | A hierarchical set of *Objects,* *Parameters, Commands and/or Events* that define the managed objects accessible via a particular *Agent*.
| **Device**        | Used here as a synonym for *CPE*.
| **DM Instance**   | Data Model Schema instance document. This is an XML document that conforms to the *DM Schema* and to any additional rules specified in or referenced by the *DM Schema*.
| **DM Schema**     | Data Model Schema. This is the XML Schema [@REC-xmlschema-0-20041028] that is used for defining data models for use with *CWMP and USP*.
| **Downstream Interface** | A physical interface object whose Upstream parameter is set to *false*, or an interface that is associated with such a physical interface via the InterfaceStack. For example, a downstream IP Interface is an IP.Interface object that is associated with an Upstream=false physical layer interface.
| **Event**         | An indication that something of interest has happened that requires the Agent to notify the Controller.
| **Fixed Network Residential Gateway** | A CPE connecting a home LAN to the WAN, which does not exchange N1 signaling with the 5GC.
| **Interface Object** | A type of *Object* that models a network interface or protocol layer. Commonly referred to as an interface. They can be stacked, one on top of the other, using *Path References* in order to dynamically define the relationships between interfaces.
| **N1**            | Reference point between the 5G-RG and the AMF and between the AGF and AMF in case of FN-RG.
| **N2**            | Reference point between W-5GAN and AMF. On the W-5GAN side, the termination point is the AGF-CP.
| **N3**            | Reference point between W-5GAN and UPF. On the W-5GAN side, the termination point is the AGF-UP.
| **Object**        | An internal node in the name hierarchy, i.e., a node that can have Object, Parameter, Command and/or Event children. An Object name is a Path Name.
| **Parameter**     | A name-value pair that represents part of a CPE or USP Agent's configuration or status. A Parameter name is a Path Name.
| **Path Name**     | A name that has a hierarchical structure similar to files in a directory, with each level separated by a "." (dot). References an Object, Parameter, Command or Event.
| **Path Reference** | Describes how a parameter can reference another parameter or object via its path name (A.2.3.4/TR-106 [@TR-106]). Such a reference can be weak or strong (Section A.2.3.6/TR-106 [@TR-106]).
| **Upstream Interface** | A physical interface object whose Upstream parameter is set to *true*, or an interface that is associated with such a physical interface via the InterfaceStack. For example, an upstream IP Interface is an IP.Interface object that is associated with an Upstream=true physical layer interface.
| **USP**           | User Services Platform. Defined in TR-369 [@TR-369], USP is an evolution of CWMP that allows applications to manipulate Service Elements in a network of Controllers and Agents.
| **USP Agent**     | A USP Agent is a USP Endpoint that exposes Service Elements to one or more USP Controllers.
| **USP Controller** | A USP Controller is a USP Endpoint that manipulates Service Elements through one or more USP Agents.
| **USP Endpoint**  | A USP Endpoint is a termination point for a USP message.
| **Wireline 5G Access Network** | This is a wireline AN that can connect to a 5G core via the AGF. The egress interfaces of a W-5GAN form the border between access and core. The interfaces are N2 for the control plane and N3 for the user plane.
:::

## Abbreviations

This %bbfType% uses the following abbreviations:

::: borderless
|                  |
|------------------|-----------------------------------------------------------
| 3GPP             | Third Generation Partnership Project
| 5G-RG            | 5G Residential Gateway
| 5QI              | 5G QoS Indicator
| 5WE              | 5G Wireline Encapsulation
| AAA              | Authentication, Authorization and Accounting
| AGF              | Access Gateway Function
| ARP              | Allocation and Retention Priority
| ATM              | Asynchronous Transfer Mode
| ATSSS            | Access Traffic Steering Switching and Splitting
| BNG              | Broadband Network Gateway
| CGN              | Carrier Grade NAT
| CUPS             | Control User Plane Separation
| DHCP             | Dynamic Host Configuration Protocol
| DHCPv6           | Dynamic Host Configuration Protocol for IPv6
| DNN              | Data Network Name
| DSCP             | Differentiated Services Code Point
| DSL              | Digital Subscriber Line
| FMIF             | Fixed Mobile Interworking Function
| FN-RG            | Fixed Network Residential Gateway
| GBR              | Guaranteed Bit Rate
| IoT              | Internet of Things
| IP               | Internet Protocol
| IPsec            | Internet Protocol Security
| LCP              | Link Control Protocol
| M2M              | Machine to Machine
| NAS              | Non Access Stratum
| NAT              | Network Address Translation
| NSCL             | Network Service Capability Layer
| OSI              | Open Systems Interconnection
| PCF              | Policy Control Function
| PCO              | Protocol Configuration Options
| PCP              | Port Control Protocol
| PDU              | Protocol Data Unit
| PPP              | Point-to-Point Protocol
| PPPoE            | Point-to-Point Protocol over Ethernet
| PTM              | Packet Transfer Mode
| QFI              | QoS Flow Indicator
| QoS              | Quality of Service
| REM              | Remote Entity Management
| RG               | Residential Gateway
| RPC              | Remote Procedure Call
| RQI              | Reflective QoS Indicator
| SCL              | Service Capability Layer
| S-NSSAI          | Single Network Slice Selection Assistance Information
| SSID             | Service Set Identifier
| TR               | Technical Report
| UPF              | User Plane Function
| URI              | Uniform Resource Identifier [@RFC3986]
| URL              | Uniform Resource Locator [@RFC3986]
| URSP             | User equipment Route Selection Policy
| USB              | Universal Serial Bus
| UUID             | Universally Unique IDentifier
| VLAN             | Virtual Local Area Network
| W-5GAN           | Wireline 5G Access Network
| WFA              | Wi-Fi Alliance
| WWC              | Wireline Wireless Convergence
| xREM             | x (Device or Gateway) Remote Entity Management
| ZDO              | ZigBee Device Object
:::

