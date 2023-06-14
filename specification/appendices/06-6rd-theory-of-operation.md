# 6rd Theory of Operation {.appendix .same-file}

See [Tunneling] for general information on how tunneling is modeled.

## RFC 5969 Configuration Parameters

RFC 5969 [@RFC5969] describes the general operation of the 6rd protocol and configuration of external parameters needed to do the protocol. @tbl:rfc-5969-configuration-parameter-mapping shows the 6rd configuration parameters defined in RFC 5969 and their mapping into the Device:2 data model. Refer to RFC 5969 for further description on use of these parameters.

Note that while RFC 5969 allows for multiple Border Relay (BR) IPv4 addresses, it does not describe how a device selects from among these. The device will need to have internal logic to handle this case, but service providers might wish to ensure that they know what the behavior will be, if they intend to supply multiple BR addresses.

:RFC 5969 Configuration Parameter Mapping

| RFC 5969 (Section 7) Configuration Parameter | Device:2 (IPv6rd.InterfaceSetting.{i}) Parameter
|----------------------------------------------|--------------------------------------------------------
| IPv4MaskLen                                  | IPv4MaskLength
| 6rdPrefix, 6rdPrefixLen                      | SPIPv6Prefix (expressed with prefix length)
| 6rdBRIPv4Address                             | BorderRelayIPv4Addresses

## Internal Configuration Parameters

*AddressSource*, *TunnelInterface*, *TunneledInterface*, and *AllTrafficToBorderRelay* parameters are used to define internal device operation. *AddressSource* allows the desired source IPv4 address to be selected (to be embedded in the 6rd IPv6 address, after removing IPv4MaskLength bits from the beginning of the address, and as the source IPv4 address of the encapsulating IPv4 header). *TunnelInterface* and *TunneledInterface* allow for internal forwarding, routing, encapsulation, classification and marking of IPv6 packets. *AllTrafficToBorderRelay* impacts determination of the IPv4 destination address of the encapsulating IPv4 header.

## IPv4 Address Source

In general, it is expected that the device will use the IPv4 address obtained on the upstream interface as the address that is embedded in the 6rd IPv6 address, and used as the encapsulating source IPv4 address. However, there could be cases where the device has other public IPv4 addresses assigned to it, and it would be preferable to use one of these. For example, if the device has a public static IP address assigned to a different interface, it could be desired to use that address instead of the address assigned to the upstream interface.

If this parameter is not present, or if it is an empty string, the device will use internal logic to determine the source IPv4 address. In cases where there is a single upstream interface with an assigned (e.g., DHCPv4, IPCP, static) IPv4 address, that is the address that will be used.

Note that service providers need to be careful when using alternate addresses. If the alternate address does not have the same higher order IPv4 bits as other devices that will be supported by the same 6rd prefix, then the IPv4 mask will need to be zero. Masked IPv4 bits will be the same for all IPv4 addresses within a 6rd domain, per RFC 5969 [@RFC5969].

## Sending All Traffic to the Border Relay Server

The default behavior of a 6rd client device is that all IPv6 packets are encapsulated in IPv4 packets with destination address of a 6rd border relay server, ***except*** when the IPv6 destination address begins with *SPIPv6Prefix*. When the destination IPv6 address begins with *SPIPv6Prefix*, then the encapsulating IPv4 destination address is derived from the IPv6 destination address by taking the next 32 - *IPv4MaskLength* bits, pre-pending the bits that are masked (as determined by its own WAN IPv4 address), and using the resulting IPv4 address as the encapsulating destination IPv4 address.

For example, if

* the IPv6 destination address is 2001:db8:64c8:200:x:x:x:x [note 64 hex = 100 decimal, c8 hex = 200 decimal, leading zeroes between colons are not shown]
* the *SPIPv6Prefix* is 2001:db8::/32
* the device's WAN IPv4 address is 10.100.100.1
* *IPv4MaskLength*  is 8
* advertised-to-LAN SLAAC prefix of 2001:db8:6464:100::/64

...then the encapsulation destination IPv4 address becomes the first 8 bits of the device's WAN IPv4 address (10 for an address of 10.100.200.2), plus the next 24 bits (32-8=24) after the *SPIPv6Prefix* (next 24 bits are 64c802 hex = 100.200.2 binary). The source encapsulating IPv4 address is 10.100.100.1. The source IPv6 address begins with the prefix 2001:db8:6464:100::/64.

However, if *AllTrafficToBorderRelay* is True, then all external-bound IPv6 traffic is sent to the border relay.

This Boolean field is reflected in the routing table. If the value is False (default behavior), then the IPv6 routing table for this example (with a border relay IPv4 address of 10.0.0.1) would include the following entries:

::: code
| ::/0 -> 6rd-tunnel-interface-int0 via 2001:db8:0:100::
|     (default route to border relay)
| 2001:db8::/32 -> 6rd-tunnel-interface-int0
|     (direct connect to 6rd tunnel interface if the first 32 bits of destination address match *SPIPv6Prefix*)
| 2001:db8:6464:100::/64 -> Ethernet0 (downstream interface)
:::

If the *AllTrafficToBorderRelay* field is true, then the 2nd entry above does not exist.

## Internal Treatment of IPv6 Packets

Since a device can have multiple upstream and multiple downstream interfaces, the model supports a logical representation of the internal virtual 6rd IPv6 interface according to the general pattern described in [Tunneling].

The internal virtual 6rd IPv6 interface is modeled as (*TunnelInterface,TunneledInterface*).

The IPv6Forwarding entries (which correspond to the routing table entries mentioned above) will route traffic between the downstream IPv6 interfaces and the 6rd IPv6 interface. IPv4Forwarding entries are unaffected.

@fig:sample-6rd-routing-and-forwarding shows the flow of tunneled 6rd traffic through the downstream, upstream, and the logical tunnel interfaces. Noted in the figure are sample values for the various *IP.Interface* entries that would be needed.

![Sample 6rd Routing and Forwarding](/images/sample-6rd-routing-and-forwarding.png)

