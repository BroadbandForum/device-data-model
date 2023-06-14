# GRE Tunnel Theory of Operation {.appendix .same-file}

See [Tunneling] for general information on how tunneling is modeled.

RFC 2784 [@RFC2784] defines a generic mechanism to encapsulate a packet of protocol A (known as the payload protocol) in a GRE packet. The resulting GRE packet is then encapsulated into a protocol B (known as the delivery protocol). The result of this operation is a payload packet that is encapsulated in a GRE tunnel delivered via protocol B. RFC 2890 [@RFC2890] extends the GRE header with two optional fields. The Key field provides an identifier to identify flows within the GRE tunnel. The Sequence Number field is used to maintain the sequence of packets within the GRE tunnel.

Device:2 models a GRE tunnel using the *GRE.Tunnel* object. Multiple GRE flows to the same remote endpoint are possible by defining multiple *GRE.Tunnel.{i}.Interface* instances within the same *GRE.Tunnel* instance.

This Appendix describes the usage of GRE for two scenarios: L2 payload over GRE and L3 payload over GRE.

## L2 Payload over GRE

For this example consider a Provider Edge Bridge that discriminates 2 separate VLANs as shown in @fig:vlan-traffic-over-gre. In this case the service provider does not support a VLAN infrastructure at the access node, but does at the core network.

A GRE tunnel is used to preserve the VLAN tagging at the edge to further interconnect the other VLAN segments. In this scenario, as the remote endpoint is the same in both cases, the VLANs are modeled as two flows within a single instance of the *GRE.Tunnel.{i}* object.

In addition, the *DSCPMarkPolicy* parameter can be used to assign DSCP values to each *GRE.Tunnel.{i}.Interface* instance for QoS treatment in the access network and towards the GRE concentrator.

![VLAN Traffic over GRE](/images/vlan-traffic-over-gre.png)

The GRE Tunnel interface layout is shown in @fig:l2-over-gre-tunnel.

![L2 over GRE Tunnel](/images/l2-over-gre-tunnel.png)

The configuration for this scenario assumes that the WAN Ethernet interface, Ethernet Link and IP interface objects have been previously configured; likewise the LAN Ethernet and Bridging objects have been previously configured. This section focuses on the association and configuration of the GRE tunnel with the WAN IP interface and the Bridge Ports.

The example configuration uses the RFC 2890 [@RFC2890] Key field to determine the GRE tunnel interface to which the GRE tunnel will forward packets.

::: code
| [***GRE Tunnel***]{.underline}
| **Device.GRE.Tunnel.1.Enable = True**
| **Device.GRE.Tunnel.1.RemoteEndPoints = GRE-IPAddress**
| **Device.GRE.Tunnel.1.DeliveryHeaderProtocol = IPv4**
|
| [***GRE Tunnel Interface 1***]{.underline}
| **Device.GRE.Tunnel.1.Interface.1**
| **Device.GRE.Tunnel.1.Interface.1.Enable = True**
| **Device.GRE.Tunnel.1.Interface.1.KeyIdentifierGenerationPolicy = Provisioned**
| **Device.GRE.Tunnel.1.Interface.1.KeyIdentifier = 1**
|
| [***GRE Tunnel Interface 2***]{.underline}
| **Device.GRE.Tunnel.1.Interface.2**
| **Device.GRE.Tunnel.1.Interface.2.Enable = True**
| **Device.GRE.Tunnel.1.Interface.2.KeyIdentifierGenerationPolicy = Provisioned**
| **Device.GRE.Tunnel.1.Interface.2.KeyIdentifier = 2**
|
| [***Associate Bridge Ports with GRE Tunnel Interfaces***]{.underline}
| **Device.Bridging.Bridge.1.Port.1.LowerLayers = Device.GRE.Tunnel.1.Interface.1**
| **Device.Bridging.Bridge.1.Port.2.LowerLayers = Device.GRE.Tunnel.1.Interface.2**
|
| [***Assign the DSCP value to each GRE Tunnel Interface using the GRE.Filter***]{.underline}
| **Device.GRE.Filter.1**
| **Device.GRE.Filter.1.Enable = True**
| **Device.GRE.Filter.1.Order = 1**
| **Device.GRE.Filter.1.Interface = Device.GRE.Tunnel.1.Interface.1**
| **Device.GRE.Filter.1.DSCPMarkPolicy = DSCP1**
| **Device.GRE.Filter.2**
| **Device.GRE.Filter.2.Enable = True**
| **Device.GRE.Filter.2.Order = 2**
| **Device.GRE.Filter.2.Interface = Device.GRE.Tunnel.1.Interface.2**
| **Device.GRE.Filter.2.DSCPMarkPolicy = DSCP2**
:::

## L3 Payload over GRE

This example describes an IP in IP encapsulation where a GRE tunnel takes IPv4 payload and encapsulates over IPv6.

@fig:ip-over-ip-gre-encapsulation shows the scenario where an IPv4 LAN network is tunneled in an IPv6 GRE tunnel that uses IPv6 global addresses.

The GRE tunnels use the default IPv6 WAN interface of the CPE.

![IP over IP GRE Encapsulation](/images/ip-over-ip-gre-encapsulation.png)

@fig:l3-over-gre-tunnel shows the configuration of a GRE tunnel for an IPv4 Private network attached to a LAN interface that is encapsulated in the IPv6 packet.

![L3 over GRE Tunnel](/images/l3-over-gre-tunnel.png)

The configuration for this scenario assumes that the WAN and LAN Ethernet interface, Ethernet Link and IP interface objects have been previously configured. This section focuses on the association and configuration of the GRE tunnel with the WAN and Tunnel IP interfaces.

::: code
| [***GRE Tunnel***]{.underline}
| **Device.GRE.Tunnel.1.Enable = True**
| **Device.GRE.Tunnel.1.RemoteEndPoints = GRE-IPAddress**
| **Device.GRE.Tunnel.1.DeliveryHeaderProtocol = IPv6**
|
| [***GRE Tunnel Interface 1***]{.underline}
| **Device.GRE.Tunnel.1.Interface.1**
| **Device.GRE.Tunnel.1.Interface.1.Enable = True**
|
| [***Associate Tunnel IPv4 Interface with GRE Tunnel Interface***]{.underline}
| **Device.IP.Interface.3.LowerLayers = Device.GRE.Tunnel.1.Interface.1**
:::

