# MAP Theory of Operation {.appendix .same-file}

See [Tunneling] for general information on how tunneling is modeled.

MAP (Mapping of Address and Port) is a mechanism for transporting IPv4 packets across an IPv6 network, and a generic mechanism for mapping between IPv6 addresses and IPv4 addresses and ports. There are two mutually exclusive MAP transport modes, both of which use NAPT44 (modified to use a restricted port range):

* MAP-E (Encapsulation) [@RFC7597] uses an IPv4-in-IPv6 tunnel.
* MAP-T (Translation) [@RFC7599] uses stateless NAT64.

Many aspects of the MAP configuration are the same for both MAP-E and MAP-T. [@RFC7598] defines DHCPv6 options for configuring MAP parameters, and the Device:2 data model parameters correspond closely to these parameters.

## MAP Configuration Parameters

The MAP-T architecture is illustrated in @fig:map-t-architecture. The MAP-E architecture diagram looks very similar, but differs as follows:

* The CPE's MAP function involves 6-4 encapsulation rather than 6-4 translation.
* The CPE uses a Border Router (BR) IPv6 address rather than a prefix.
* Non MAP-aware servers (i.e., native IPv6 servers) can't be reached by IPv4 devices behind the CPE (i.e., can't be part of the MAP domain).

![MAP-T Architecture](/images/map-t-architecture.png)

The Device:2 data model models each MAP domain as an instance of the corresponding *MAP.Domain* table. The most important domain parameters are:

* *TransportMode*: "Encapsulation" (MAP-E) or "Translation" (MAP-T).
* *WANInterface*: the WAN IP interface through which all MAP traffic will flow.
* *IPv6Prefix*: end-user IPv6 prefix; one of this interface's prefixes, typically assigned via DHCPv6 Prefix Delegation.
* *BRIPv6Prefix*: the Border Router IPv6 prefix (MAP-T mode) or IPv6 address (MAP-E mode).
* *DSCPMarkPolicy*: governs DSCP selection when encapsulating / translating.
* *PSIDOffset* etc: parameters defining Port-sets ([@RFC7597] Section 5.1).

Each domain has a set of mapping rules ([@RFC7597] Section 5) with each rule having the following parameters:

* *IPv6Prefix*: the IPv6 prefix for this rule.
* *IPv4Prefix*: the IPv4 prefix for this rule.
* *EABitsLength*: the length of the EA (Embedded Address) bits for this rule.
* *IsFMR*: whether this rule is an FMR (Forwarding Mapping Rule).

The mapping rule with the longest match between its *IPv6Prefix* and the end-user IPv6 prefix is the BMR (Basic Mapping Rule). This is used to determine the MAP IPv6 address, which is one of *Interface*'s addresses and is used for all MAP traffic.

## Internal Treatment of IPv4 Packets

Since a device can have multiple upstream and multiple downstream interfaces, the model supports a logical representation of the internal virtual MAP IPv4 interface according to the general pattern described in [Tunneling]. The *IPv4Forwarding* entries will route traffic between the LAN IPv4 interface and the MAP IPv4 interface.

@fig:sample-map-routing-and-forwarding shows the flow of MAP traffic through the various interfaces. Noted in the figure are sample values for the various *IP.Interface* entries that would be needed.

![Sample MAP Routing and Forwarding](/images/sample-map-routing-and-forwarding.png)

@fig:sample-map-routing-and-forwarding-interface-stack shows the corresponding MAP interface stack.

![Sample MAP Routing and Forwarding (Interface Stack)](/images/sample-map-routing-and-forwarding-interface-stack.png)

