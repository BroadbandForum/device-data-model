# IPsec Theory of Operation {.appendix .same-file}

See [Tunneling] for general information on how tunneling is modeled.

The Device:2 data model includes an IPsec (RFC 4301 [@RFC4301]) object that supports the configuration of Encapsulating Security Payload (ESP; RFC 4303 [@RFC4303]) and Authentication Header (AH; RFC 4302 [@RFC4302]) in tunnel mode (Section 3.2/RFC 4301). Use of IKEv2 (RFC 5996 [@RFC5996]) is assumed. The IPsec object does not currently support static configuration of tunnels and child Security Associations (SAs).

@fig:ipsec-data-model-objects illustrates the main IPsec objects and their relationships.

![IPsec Data Model Objects](/images/ipsec-data-model-objects.png)

In the Figure, instances of the colored objects (*Filter.{i}* and *Profile.{i}*) are created and populated by the Controller. Instances of all other objects are handled by the CPE as IPsec tunnels are created and deleted. References between objects are shown:

* Solid lines indicate references that are populated by the Controller, and dashed lines indicate references that are handled by the CPE.
* A reference marked "(U)" is a unique key, which implies a 1-1 relationship, e.g., only one *Tunnel* instance can reference a given (*Tunnel,Tunneled*) *IP.Interface* pair.
* Other references imply n-1 relationships, e.g., multiple *Filter* instances can reference a given *Profile* instance.

Typical usage is as follows:

* The factory default configuration can contain static instances of the various objects.
* The Controller creates and configures *Filter* and *Profile* instances. *Filter* instances model IPsec Security Policy Database (SPD) selection criteria and *Profile* instances model SPD processing info. Each *Filter* instance references a *Profile* instance so a single *Profile* instance can, if desired, be shared by several *Filter* instances.
* When the Controller enables a *Filter* instance, the CPE determines whether a new tunnel is needed in order to carry the traffic that matches that filter. It is possible that an existing tunnel can carry the traffic.
* If a new tunnel is needed, the CPE immediately creates a *Tunnel* instance that references a newly-created (*Tunnel,Tunneled*) *IP Interface* pair. This corresponds exactly to the general tunneling approach that is described in [Tunneling].
* Each *Tunnel* instance also references all of the currently-enabled *Filter* instances that require it to exist.
* Classification and forwarding rules can now be defined, regardless of whether the tunnels have yet been established. *ForwardingPolicy* is both a QoS *Classification* result and an IPsec *Filter* result (it's in the *Policy* table), and so can, as explained in [Tunneling], affect the forwarding decision and thus whether or not a given packet will be en-tunneled or de-tunneled.
* When a tunnel needs to become active, e.g., as a result of traffic that matches one of the *Filter* instances, the CPE will establish it and will create the appropriate *IKEv2SA* and *ChildSA* objects.
* When a tunnel no longer needs to be active, the CPE will delete the *ChildSA* and *IKEv2SA* objects. This will affect the status of the *Tunnel* instance and (*Tunnel,Tunneled*) *IP Interface* pair but will not delete them.

The remainder of this Appendix consists of a brief summary of the various IPsec data model objects.

## IPsec

The top-level object has an *Enable* parameter that enables and disables the IPsec sub-system, various capability parameters, e.g., supported encryption algorithms, and global IPsec statistics.

## IPsec.Filter

The *Filter* table models IPsec Security Policy Database (SPD) selection criteria. Refer to Section 4.4.1/RFC 4301 [@RFC4301] for further details.

SPD filtering is performed for all packets that might need to cross the IPsec boundary. Refer to Section 3.1/RFC4301 for further details. Given that IPsec operates at the IP level, this means that SPD filtering conceptually occurs after bridging and before routing.

This table is conceptually quite similar to the QoS Classification table in that entries are ordered, associated with an ingress interface, include selection criteria, and specify the action to be taken for matching packets.

Instances of the *Filter* table can be created statically by the CPE, or can be created and deleted by the Controller as needed. Each instance includes the following (this is not a complete list):

* *Enable*: to enable and disable the entry.
* *Status*: to indicate the status of the entry.
* *Order*: to control and indicate the order of the entry.
* *Interface*, *AllInterfaces*: to control and indicate with which interfaces the entry is associated.
* *DestIP*: to select packets by destination IP address.
* *SourceIP*: to select packets by source IP address.
* *Protocol*: to select packets by IP protocol.
* *DestPort*: to select packets by destination port.
* *SourcePort*: to select packets by source port.
* *Discard*: whether to discard matching packets.
* *Profile*: the Profile instance that governs how non-discarded matching packets will be treated.

## IPsec.Profile

The *Profile* table models IPsec Security Policy Database (SPD) processing info. Refer to Section 4.4.1/RFC 4301 [@RFC4301] for further details. Each *Filter* instance references a *Profile* instance. It would be possible to include the processing info directly in each *Filter* instance, but use of a separate table allows *Profile* entries to be shared between *Filter* instances.

Instances of the *Profile* table can be created statically by the CPE, or can be created and deleted by the Controller as needed. Each instance includes the following (this is not a complete list):

* *MaxChildSAs*: the maximum number of Child SAs per IKEv2 session (and therefore per IPsec tunnel); this provides a simple way of controlling the extent to which existing tunnels can be re-used.
* *RemoteEndpoints*: an ordered list of remote tunnel endpoints that are to be used when establishing an IPsec tunnel corresponding to this *Profile* instance.
* *ForwardingPolicy*: an opaque (Controller-chosen) value that provides a feed-forward mechanism that allows the SPD filtering decision to affect the forwarding decision. QoS classification uses the same mechanism.
* *Protocol*: the "child" security protocol, i.e., AH or ESP.
* *IKEv2AuthenticationMethod*: a reference to a CPE certificate or other CPE credentials.
* *IKEv2AllowedEncryptionAlgorithms* (etc): encryption algorithm that IKEv2 is permitted to negotiate; also several other "allowed" parameters that define acceptable IKEv2, AH and ESP algorithms.
* *DSCPMarkPolicy* (etc): various settings that govern how packets should be tunneled.

## IPsec.Tunnel

The *Tunnel* table that models IPsec tunnels. Instances are created and deleted by the CPE as needed. A (*Tunnel,Tunneled*) *IP* *Interface* pair is always created at the same time as an IPsec *Tunnel* instance and has the same lifetime; the *Tunnel IP Interface* contains generic IP interface settings, e.g., *Enable*, *Status* and generic *Stats*, and the IPSec *Tunnel* instance contains IPsec-specific settings, e.g., additional *Stats*.

::: note
A (*Tunnel,Tunneled*) *IP* *Interface* pair consists of an IP Interface instance with Type = "Tunnel", and another IP Interface instance with Type = "Tunneled".
:::

## IPsec.IKEv2SA

Each entry in the *IKEv2SA* table models a single IKEv2 SA pair and uniquely references a *Tunnel* instance. Unlike *Tunnel* instances, which exist regardless of whether the tunnel is active, *IKEv2SA* instances exist only when the IKEv2 SA pair exists, i.e., they exist only when the tunnel is active.

## IPsec.IKEv2SA.ChildSA

The *ChildSA* table models child SA pairs. It is a child of the corresponding *IKEv2SA* instance and so exists only when the *IKEv2SA* instance exists.

