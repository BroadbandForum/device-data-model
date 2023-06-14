# Tunneling {.annex}

## Overview

Consider a device that provides a layer 3 tunnel endpoint. Some packets will need to be en-tunneled and then will leave the device in the tunnel. Other packets will arrive at the device in the tunnel and will need to be de-tunneled. This is illustrated in @fig:tunneling-overview, in which green indicates application traffic, yellow indicates an IP interface, and pink indicates a tunnel (carrying green application traffic).

![Tunneling Overview](/images/tunneling-overview.png)

The Figure highlights three decisions:

#. Whether to en-tunnel an upstream packet.
#. Whether to de-tunnel a downstream packet.
#. To which egress interface to send an outgoing packet.

This egress interface decision is just a normal forwarding decision. By separately modeling the *Tunnel interface* and the *Tunnel*, the Device:2 data model is able to present the en-tunnel decision as also being a forwarding decision. The de-tunnel decision is not really a decision at all, because it happens automatically as a result of normal packet processing.

This modeling approach imposes no restrictions on the device implementation; it is just how the en-tunnel and de-tunnel decisions are modeled.

* Each *Tunnel* instance models a tunnel and has one or more *Tunnel interface* children, each of which models a flow / session within that tunnel. These *Tunnel interface* children are stackable interface objects.

* Upstream traffic that is to be en-tunneled is routed to a *Tunnel interface* instance, is passed to the parent *Tunnel* instance, is encapsulated, and then arrives on the *Tunnel* instance.

* Downstream traffic that is to be de-tunneled is passed to a *Tunnel* instance, is de-encapsulated, and then arrives on the appropriate child *Tunnel interface* instance.

* Traffic arriving on a *Tunnel* or on a *Tunnel* *interface* is classified, marked, policed, bridged, routed and queued in the same way as traffic arriving on any other interface.

::: note
A Tunnel is not a stackable interface object, because it breaks the layering order and can be regarded as separating two different protocol stacks, one of which acts as a carrier for the other. This is clearly illustrated in @fig:general-layer-3-tunneling-interface-stack and the other interface stack Figures.
:::

::: note
Even though a Tunnel is not an interface, it can be referenced by QoS classification rules. Traffic arriving on a Tunnel instance, i.e., packets that have just been encapsulated, is conceptually similar to locally-generated traffic.
:::

In summary, the decision to en-tunnel a packet is a forwarding decision to send a packet to an IP interface that is stacked above a *Tunnel* *interface* instance, and the decision to de-tunnel a packet is a consequence of the fact that it is addressed to the CPE and is therefore passed to a *Tunnel* instance. @fig:tunneling-overview-showing-forwarding-decisions extends @fig:tunneling-overview by expanding the tunnel into a *Tunnel IP interface*, a *Tunnel interface*, and the *Tunnel* instance, thereby showing where these two decisions are made.

![Tunneling Overview (Showing Forwarding Decisions)](/images/tunneling-overview-showing-forwarding-decisions.png)

::: note
The existing 6rd, DS-Lite and IPsec data models use a less flexible approach in which the Tunnel interfaces are not explicitly modeled, and a separate non-stackable Tunnel table references auto-created Tunnel/Tunneled IP interface pairs. See *[Details](#tunneling-details)* for further details.
:::

::: note
The Tunnel interface and Tunnel approach is more flexible because (a) it supports multiple flows / sessions with a tunnel (e.g., GRE traffic flows or L2TP sessions), (b) it supports additional encapsulation layers between the Tunnel IP interface and the Tunnel interface (e.g., PPP for L2TP), and (c) it supports layer 2 tunneling use cases (traffic is bridged directly to the Tunnel interface and there is no Tunnel IP interface). See *[Details](#tunneling-details)* for further details.
:::

[@fig:sample-flow-of-upstream-tunneled-traffic-through-the-device; @fig:sample-flow-of-downstream-tunneled-traffic-through-the-device] show upstream and downstream examples of how the *Tunnel interface* and *Tunnel* instances are used to describe the traffic path through the device for both untunneled and tunneled packets.

![Sample Flow of Upstream Tunneled Traffic through the Device](/images/sample-flow-of-upstream-tunneled-traffic-through-the-device.png)

![Sample Flow of Downstream Tunneled Traffic through the Device](/images/sample-flow-of-downstream-tunneled-traffic-through-the-device.png)

The less flexible (*Tunnel,Tunneled*) IP interface mechanism is used in the following three cases:

* [IPv6rd][6rd Theory of Operation] *Device.IPv6rd*.
* [DS-Lite][Dual-Stack Lite Theory of Operation] *Device.DSLite*.
* [IPsec][IPsec Theory of Operation] *Device.IPsec*.

The flexible *Tunnel interface* and *Tunnel* mechanism is used for the following two cases and will be used for modeling all future tunneling scenarios:

* [GRE][GRE Tunnel Theory of Operation] *Device.GRE*.
* [MAP][MAP Theory of Operation] *Device.MAP*.

## Details {#tunneling-details}

@fig:general-layer-3-tunneling-interface-stack shows the interface stack for a general layer 3 tunneling scenario. Compare with @fig:general-layer-3-tunneling-from-tunneling-overview), which is derived from @fig:tunneling-overview-showing-forwarding-decisions. It can be seen that each Figure presents a different view of the same thing.

![General Layer 3 Tunneling Interface Stack](/images/general-layer-3-tunneling-interface-stack.png)

![General Layer 3 Tunneling (from Tunneling Overview)](/images/general-layer-3-tunneling-from-tunneling-overview.png)

::: note
IP.Interface.3 is labeled as Type=Normal in @fig:general-layer-3-tunneling-interface-stack but as Tunnel IP interface in @fig:general-layer-3-tunneling-from-tunneling-overview. IP interface Type=Tunnel was defined specifically for the (Tunnel,Tunneled) IP interface mechanism and is not needed because IP.Interface.3 is stacked above TT.Tunnel.1.Interface.1.
:::

@fig:general-layer-3-tunneling-interface-stack is general in that it is independent of the tunnel technology, but it doesn't illustrate all the possibilities. If supported by the tunnel technology:

* A Tunnel can have multiple Tunnel interface children, each of which models a flow or session. In this case the Tunnel interface object is multi-instance.

* There can be additional encapsulation layers between the Tunnel IP interface(s) and the Tunnel interface(s).

@fig:l2tp-interface-stack-example shows an L2TP [@RFC2661] example that illustrates both of the above.

![L2TP Interface Stack Example](/images/l2tp-interface-stack-example.png)

Some tunneling technologies support layer 2 tunnels, in which the tunnel payload is a layer 2 packet. @fig:general-layer-2-tunneling-interface-stack shows the interface stack for a general layer 2 tunneling scenario. This is conceptually similar to the layer 3 case, but a bridge port rather than an IP interface is stacked above the *Tunnel interface*.

![General Layer 2 Tunneling Interface Stack](/images/general-layer-2-tunneling-interface-stack.png)

