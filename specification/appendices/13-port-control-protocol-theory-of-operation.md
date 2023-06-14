# Port Control Protocol Theory of Operation {.appendix .same-file}

The Port Control Protocol (PCP) allows an IPv6 or IPv4 host to control how incoming IPv6 or IPv4 packets are translated and forwarded by a Network Address Translator (NAT) or simple firewall (generically referred to as the "PCP-controlled device"), and also allows a host to optimize its outgoing NAT keepalive messages.

When a PCP client is embedded in a device, the PCP client can be invoked by:

* Applications running on the device itself (remote access, VoIP...),
* The device GUI,
* The Controller,
* Interworking functions [@RFC6970] and the PCP proxy that allow applications running on other end-devices connected to the device to manage the PCP-controlled device.

![Example of a PCP Client embedded in the RG using CWMP](/images/example-of-a-pcp-client-embedded-in-the-rg-using-cwmp.png)

![Example of a PCP Client embedded in a device using CWMP, with PCP Proxy in the RG](/images/example-of-a-pcp-client-embedded-in-a-device-using-cwmp-with-pcp-proxy-in-the-rg.png)

Defining a PCP data model allows the Controller to remotely manage the PCP client including:

* Configuration and monitoring of the PCP client itself,
* Configuration and monitoring of the PCP servers interacting with the client,
* Monitoring PCP Interworking Functions,
* Monitoring and setting rules in the PCP-controlled device from the PCP client.

Whereas the description of objects themselves is enough to understand how to proceed, some operations need further explanation about the way to manage the objects.

This theory of operation relies on IETF RFCs and drafts:

* RFC 6887 Port Control Protocol (PCP) [@RFC6887],
* RFC 6970 UPnP IGD-PCP Interworking Function [@RFC6970],
* DHCP Options for the Port Control Protocol (PCP) [@RFC7291],
* Port Control Protocol (PCP) Proxy Function [@RFC7648],
* PCP Server Selection [@RFC7488],
* PCP Flow Examples [@draft-boucadair-pcp-flow-examples].

The data model allows for more than one PCP client, but those clients operate independently. Therefore, the text below considers only one PCP client.

## Configuration and monitoring of the PCP Server

Prior to sending its first PCP message, the PCP client determines which server to use as described in [@RFC7488]. To do so the PCP client of the CPE can be configured statically (GUI or CWMP) or via DHCP (v4 or v6).

* When configured via DHCP, the CPE receives a list (at least one) of PCP server addresses in one or more *OPTION_V4_PCP_SERVER* or *OPTION_V6_PCP_SERVER* DHCP options. Based on the content of these DHCP options, the CPE creates one or more instances of *PCP.Client.{i}.Server* (see [@RFC7291]). The list of addresses provided for each PCP server is stored in the *ServerNameOrAddress* and *AdditionalServerAddresses* parameters and the *Origin* parameter is set to either "DHCPv4" or "DHCPv6".

* When statically configured, one instance of *PCP.Client.{i}.Server* is created per server, with the *Origin* parameter set to "Static". The server is defined by either an FQDN or an IP address in *ServerNameOrAddress*.

Based on these server definitions, the PCP client follows the procedures specified in [@RFC7488] to determine the IP Address to be used for each configured PCP server.

* While the PCP client is trying to connect to a PCP server on a given IP address, the *PCP.Client.{i}.Server* object's *ServerAddressInUse* holds that IP address and its *Status* is "Connecting".

* When the PCP client has successfully received a response from a server, *Status* becomes "Enabled" and server-discovered properties (*CurrentVersion*, *Capabilities*...) are stored in the corresponding parameters.

* If the PCP client fails to connect to a given PCP server, *ServerAddressInUse* remains the last IP address tried and *Status* reflects the appropriate error condition.

No conflict or doubt can arise between DHCP and static configurations, because they are represented in separate *PCP.Client.{i}.Server* instances, with *Origin* to record the origin of the configuration. *ServerNameOrAddress* is writable by the Controller only if *Origin* is "Static".

## Monitoring and setting rules set by the PCP client

Once a PCP server has been successfully contacted, the PCP client is ready to set rules in the corresponding PCP-controlled device. Depending on the use case, the PCP client selects the appropriate PCP server based on its *Capabilities*, as described in Section 10 of [@RFC6887]. It is possible to define the following mappings:

[Inbound Mapping without filters]{.underline}\
An inbound mapping is defined by an instance of the *PCP.Client.{i}.Server.{i}.InboundMapping* table. It is created by a PCP request with the MAP OpCode, as described in Section 11 of [@RFC6887]. This is allowed only if *PCP.Client.{i}.MAPEnable* is "true".

[Inbound Mapping with filters]{.underline}\
As above, but additional filters are defined by instances of the *PCP.Client.{i}.Server.{i}.InboundMapping.{i}.Filter* table. Filters are specified in the PCP request using the FILTER option, as described in Section 13.3 of [@RFC6887]. This is allowed only if *PCP.Client.{i}.FILTEREnable* is "true".

[Outbound Mapping]{.underline}\
An outbound mapping is defined by an instance of the *PCP.Client.{i}.Server.{i}.OutboundMapping* table. It is created by a PCP request with the PEER OpCode, as described in Section 12 of [@RFC6887]. This is allowed only if *PCP.Client.{i}.PEEREnable* is "true".

It is possible to define a mapping on behalf of another device. The PCP request uses the THIRD_PARTY option to create the mapping, as described in Section 13.1 of [@RFC6887]. This is allowed only if *PCP.Client.{i}.THIRDPARTYStatus* is "Enabled".

These operations can be requested by the device itself (embedded applications, GUI, CWMP...) or by another device through the UPnP IGD interworking function [@RFC6970] (if *PCP.Client.{i}.UPnPIWF.Status* is "Enabled") or the PCP Proxy [@RFC7648] (if *PCP.Client.{i}.PCPProxy.Status* is "Enabled").

[@draft-boucadair-pcp-flow-examples] provides a set of examples to illustrate PCP operations. These operations can be monitored by getting *PCP.Client.{i}.Server.{i}.InboundMapping* and *PCP.Client.{i}.Server.{i}.OutboundMapping* objects*.* The parameters sent by the PCP client in MAP or PEER requests are represented in corresponding parameters *(Lifetime, SuggestedExternalIPAddress, SuggestedExternalPort, SuggestedExternalPortEndRange, ProtocolNumber, InternalPort*...) of *PCP.Client.Server.{i}.InboundMapping* and *PCP.Client.Server.{i}.OutboundMapping.* The *Origin* parameter denotes which mechanism triggered the request:

* "Internal" for an embedded application,
* "Static" for a request issued from the GUI or set using CWMP (see next paragraph),
* "UPnP_IWF" for a UPnP IGD device,
* "PCP_Proxy" for a PCP device.

The parameters received when the PCP-controlled device has processed the request are represented in corresponding parameters *(Lifetime, AssignedExternalIPAddress, AssignedExternalPort, AssignedExternalPortEndRange*...) of *PCP.Client.{i}.Server.{i}.InboundMapping* and *PCP.Client.{i}.Server.{i}.OutboundMapping.*

To remotely create rules using CWMP or USP, the Controller configures the request to be sent by the PCP Client. To do so the Controller creates the necessary objects and sets, depending on the operation, the *Lifetime, SuggestedExternalIPAddress, SuggestedExternalPort, SuggestedExternalPortEndRange, ProtocolNumber, InternalPort* parameters of *PCP.Client.{i}.Server.{i}.InboundMapping* or of *PCP.Client.{i}.Server.{i}.OutboundMapping.* To monitor the result, the Controller will get *PCP.Client.{i}.Server.{i}.InboundMapping* and *PCP.Client.{i}.Server.{i}.OutboundMapping* objects to retrieve the parameters received from the PCP-controlled device.

## Rapid recovery

A recovery mechanism for situations where the PCP server loses its state is described in Section 14 of [@RFC6887]. This is usable only if *PCP.Client.{i}.ANNOUNCEEnable* is "true".

