#  Architecture {.new-page}

## Interface Layers

This %bbfType% models network interfaces and protocol layers as independent data objects, generally referred to as interface objects (or interfaces). Interface objects can be stacked, one on top of the other, using path references in order to dynamically define the relationships between interfaces.

The interface object and interface stack are concepts inspired by RFC 2863 [@RFC2863].

Within the Device:2 data model, interface objects are arbitrarily restricted to definitions that operate at or below the IP network layer (i.e., layers 1 through 3 of the OSI model [@X.200]). However, vendor-specific interface objects MAY be defined which fall outside this restricted scope.

@fig:osi-layers-and-interface-objects lists the interface objects defined in the Device:2 data model.
The indicated OSI layer is non-normative; it serves as a guide only, illustrating at what level in the stack an interface object is expected to appear. However, a CPE need not support or use all interfaces, which means that the figure does not reflect all possible stacking combinations and restrictions. For example, one CPE stack might exclude DSL Bonding, while another CPE stack might include DSL Bonding but exclude Bridging, while still another might include VLANTermination under PPP, or VLANTermination under IP with no PPP, or even Ethernet Link under IP with no VLANTermination and no PPP.

::: note
Throughout this %bbfType%, object names are often abbreviated in order to improve readability. For example, Device.Ethernet.VLANTermination.{i}. is the full name of a Device:2 object, but might casually be referred to as Ethernet.VLANTermination.{i} or VLANTermination.{i} or VLANTermination, just so long as the abbreviation is unambiguous (with respect to similarly named objects defined elsewhere within the data model).
:::

::: note
The Bridge.{i}.Port.{i} object models both management (upwards facing) Bridge Ports and non-management (downwards facing) Bridge Ports, where each instance is configured as one or the other. Management Bridge Ports are stacked above non-management Bridge Ports.
:::

![OSI Layers and Interface Objects](/images/osi-layers-and-interface-objects.png)

## Interface objects

An interface object is a type of network interface or protocol layer. Each type of interface is modeled by a Device:2 data model table, with a row per interface instance (e.g., IP.Interface.{i} for IP Interfaces).

Each interface object contains a core set of parameters and objects, which serves as the template for defining interface objects within the data model. Interface objects can also contain other parameters and sub-objects specific to the type of interface.

The core set of parameters consists of:

::: borderless
|                             |
|-----------------------------|--------------------------------------------------------------------------
| Enable                      | The administrative state of the interface (i.e., boolean indicating enabled or disabled)
| Status                      | The operational state of the interface (i.e., Up, Down, Unknown, Dormant, NotPresent, LowerLayerDown, Error)
| Alias                       | An alternate name used to identify the interface, which is assigned an initial value by the CPE but can later be chosen by the Controller
| Name                        | The textual name used to identify the interface, which is chosen by the CPE
| LastChange                  | The accumulated time in seconds since the interface entered its current operational state
| LowerLayers                 | A list of path references to interface objects that are stacked immediately below the interface
:::

Also, a core set of statistics parameters is contained within a Stats sub-object. The definition of these parameters MAY be customized for each interface type. The core set of parameters within the Stats sub-object consists of:

::: borderless
|                             |
|-----------------------------|--------------------------------------------------------------------------
| BytesSent                   | The total number of bytes transmitted out of the interface, including framing characters.
| BytesReceived               | The total number of bytes received on the interface, including framing characters.
| PacketsSent                 | The total number of packets transmitted out of the interface.
| PacketsReceived             | The total number of packets received on the interface.
| ErrorsSent                  | The total number of outbound packets that could not be transmitted because of errors.
| ErrorsReceived              | The total number of inbound packets that contained errors preventing them from being delivered to a higher-layer protocol.
| UnicastPacketsSent          | The total number of packets requested for transmission, which were not addressed to a multicast or broadcast address at this layer, including those that were discarded or not sent.
| UnicastPacketsReceived      | The total number of received packets, delivered by this layer to a higher layer, which were not addressed to a multicast or broadcast address at this layer.
| DiscardPacketsSent          | The total number of outbound packets, which were chosen to be discarded even though no errors had been detected to prevent their being transmitted.
| DiscardPacketsReceived      | The total number of inbound packets, which were chosen to be discarded even though no errors had been detected to prevent their being delivered.
| MulticastPacketsSent        | The total number of packets that higher-layer protocols requested for transmission and which were addressed to a multicast address at this layer, including those that were discarded or not sent.
| MulticastPacketsReceived    | The total number of received packets, delivered by this layer to a higher layer, which were addressed to a multicast address at this layer.
| BroadcastPacketsSent        | The total number of packets that higher-level protocols requested for transmission and which were addressed to a broadcast address at this layer, including those that were discarded or not sent.
| BroadcastPacketsReceived    | The total number of received packets, delivered by this layer to a higher layer, which were addressed to a broadcast address at this layer.
| UnknownProtoPacketsReceived | The total number of packets received via the interface, which were discarded because of an unknown or unsupported protocol.
:::

::: note
The CPE MUST reset an interface's Stats parameters (unless otherwise stated in individual object or parameter descriptions) either when the interface becomes operationally down due to a previous administrative down (i.e., the interface's Status parameter transitions to a down state after the interface is disabled) or when the interface becomes administratively up (i.e., the interface's Enable parameter transitions from false to true). Administrative and operational status are discussed in *[Administrative and Operational Status]*.
:::

### Lower Layers

Each interface object can be stacked on top of zero or more other interface objects, which MUST be specified using its LowerLayers parameter. By having each interface object, in turn, reference the interface objects in its lower layer; a logical hierarchy of all interface relationships is built up.

The LowerLayers parameter is a comma-separated list of path references to interface objects. Each item in the list represents an interface object that is stacked immediately below the referencing interface. If a referenced interface is deleted, the CPE MUST remove the corresponding item from this list (i.e., items in the LowerLayers parameter are strong references).

These relationships between interface objects can either be set by management action, in order to specify new interface configurations, or be pre-configured within the CPE.

A CPE MUST reject any attempt to set LowerLayers values that would result in an invalid or unsupported configuration. The corresponding fault response from the CPE MUST indicate this, using the appropriate protocol response.

The lowest layer in a fully configured and operational stack is generally the physical interface (e.g., DSL Line instance representing a DSL physical link). Within these physical interface objects the LowerLayers parameter will be an empty list, unless some lower layer vendor-specific interface objects are defined and present. Higher layer interface objects MAY operate without a physical layer being modeled, however this is a local matter to the CPE.

@fig:interface-lowerlayers illustrates the use of the LowerLayers parameter. A, B, C, and D represent interface objects. Interface A's LowerLayers parameter references interfaces B and C. Interface B's LowerLayers parameter references interface D. Interfaces C and D have no interface references specified in their LowerLayers parameters. In this way, a multi-layered interface stack is configured. If the Controller were to delete interface B, then the CPE would update interface A's LowerLayers parameter to no longer reference interface B (and interface D would be stranded, no longer referenced by the now deleted interface B).

![Interface LowerLayers](/images/interface-lowerlayers.png){typst-scale=0.5}

### Administrative and Operational Status

::: note
Many of the requirements outlined in this section were derived from Section 3.1.13/RFC 2863 [@RFC2863].
:::

An interface object's Enable and Status parameters specify the current administrative and operational status of the interface, respectively. Valid values for the Status parameter are: Up, Down, Unknown, Dormant, NotPresent, LowerLayerDown, and Error.

The CPE MUST do everything possible in order to follow the operational state transitions as described below. In some cases, these requirements are defined as SHOULD; this is not an indication that they are optional. These transitions, and the relationship between the Enable parameter and the Status parameter, are required behavior -- it is simply the timing of how long these state transitions take that is implementation specific.

When the Enable parameter is *false* the Status parameter SHOULD normally be *Down* (or *NotPresent* or *Error* if there is a fault condition on the interface). Note that when the Enable parameter transitions to *false*, it is possible that the Status parameter's transition to *Down* might occur after a small time lag if the CPE needs to first complete certain operations (e.g., finish transmitting a packet).

When the Enable parameter is changed to *true*, the Status SHOULD do one of the following:

* Change to *Up* if and only if the interface is able to transmit and receive network traffic.
* Change to *Dormant* if and only if the interface is operable, but is waiting for external actions before it can transmit and receive network traffic.
* Change to *LowerLayerDown* if and only if the interface is prevented from entering the *Up* state because one or more of the interfaces beneath it is down.
* Remain in the *Error* state if there is an error or other fault condition detected on the interface.
* Remain in the *NotPresent* state if the interface has missing (typically hardware) components.
* Change to *Unknown* if the state of the interface cannot be determined for some reason.

The *Dormant* state indicates that the interface is operable, but it is waiting for external events to occur before it can transmit/receive traffic. When such events occur, and the interface is then able to transmit/receive traffic, the Status SHOULD change to the *Up* state. Note that both the *Up* and *Dormant* states are considered healthy states.

The *Down*, *NotPresent*, *LowerLayerDown,* and *Error* states all indicate that the interface is down. The *NotPresent* state indicates that the interface is down specifically because of a missing (typically hardware) component. The *LowerLayerDown* state indicates that the interface is stacked on top of one or more other interfaces, and that this interface is down specifically because one or more of these lower-layer interfaces is down.

The *Error* state indicates that the interface is down because an error or other fault condition was detected on the interface.

### Stacking and Operational Status

::: note
The requirements outlined in this section were derived from Section 3.1.14/RFC 2863 [@RFC2863].
:::

When an interface object is stacked on top of lower-layer interfaces (i.e., is not a bottommost layer in the stack), then:

* The interface SHOULD be *Up* if it is able to transmit/receive traffic due to one or more interfaces lower down in the stack being *Up*, irrespective of whether other interfaces below it are in a non-*Up* state (i.e., the interface is functioning in conjunction with at least some of its lower-layered interfaces).
* The interface MAY be *Up* or *Dormant* if one or more interfaces lower down in the stack are *Dormant* and all other interfaces below it are in a non-*Up* state.
* The interface is expected to be *LowerLayerDown* while all interfaces lower down in the stack are either *Down*, *NotPresent*, *LowerLayerDown,* or *Error*.

### Vendor-specific Interface Objects

Vendor-specific interface objects MAY be defined and used. If such objects are specified by vendors, they MUST be preceded by *X_<VENDOR>_* and follow the syntax for vendor extensions used for parameter names (as defined in Section 3.3/TR-106 [@TR-106]).

If the Controller encounters an unknown vendor-specific interface object within a CPE's interface stack, rather than responding with a fault, the Controller MUST proceed as if this object's upper-layer interfaces were directly linked to its lower-layer interfaces. This applies whether the Controller encounters such an object via the [InterfaceStack table] or via an interface object's LowerLayers parameter.

@fig:ignoring-a-vendor-specific-interface-object-in-the-stack illustrates a stacked vendor-specific interface object being bypassed by the Controller, where there is just one object below the vendor-specific object.

![Ignoring a Vendor-specific Interface Object in the Stack](/images/ignoring-a-vendor-specific-interface-object-in-the-stack.png){typst-scale=0.5}

@fig:ignoring-a-vendor-specific-interface-object-in-the-stack-multiple-sub-objects illustrates a stacked vendor-specific interface object being bypassed by the Controller, where there are multiple objects below the vendor-specific object.

![Ignoring a Vendor-specific Interface Object in the Stack (multiple sub-objects)](/images/ignoring-a-vendor-specific-interface-object-in-the-stack-multiple-sub-objects.png){typst-scale=0.5}

## InterfaceStack Table

Although the interface stack can be traversed via [LowerLayers parameters][Lower Layers], an alternate mechanism is provided to aid in visualizing the overall stacking relationships and to quickly access objects within the stack.

The InterfaceStack table is a Device:2 data model object, namely *Device.InterfaceStack.{i}*. This is a read-only table whose rows are auto-generated by the CPE based on the current relationships that are configured between interface objects (via each interface instance's LowerLayers parameter). Each table row represents a "link" between a higher-layer interface object (referenced by its HigherLayer parameter) and a lower-layer interface object (referenced by its LowerLayer parameter). This means that an InterfaceStack table row's HigherLayer and LowerLayer parameters will always both be non-null.

::: note
As a consequence, interface instances that have been stranded will not be represented within the InterfaceStack table. It is also likely that multiple, disjoint groups of stacked interface objects will coexist within the table (for example, each IP interface will be the root of a disjoint group; unused "fragments", e.g., a secondary DSL channel with a configured ATM PVC that isn't attached to anything above, will linger if they remain interconnected; and finally, partially configured "fragments" can be present when an interface stack is being set up).
:::

::: note
An interface instance is considered stranded when it has no lower layer references to or from other interface instances. Stranded interface instances will be omitted from the InterfaceStack table until such time as they are stacked, above or below another interface instance, via a LowerLayers parameter reference.
:::

A CPE MUST autonomously add or remove rows in the InterfaceStack table in response to the following circumstances:

* An interface's LowerLayers parameter was updated to remove a reference to another interface (i.e., a "link" is being removed from the stack).
* An interface's LowerLayers parameter was updated to add a reference to another interface (i.e., a "link" is being added to the stack).
* An interface was deleted that had referenced, or been referenced by, one other interface (i.e., a "link" is being removed from the stack).
* An interface was deleted that had referenced, or been referenced by, multiple interfaces (i.e., multiple "links" are being removed from the stack).

Once the CPE issues the response to the Controller request, all autonomous InterfaceStack table changes associated with the corresponding request (as described in the preceding paragraph) MUST be available for subsequent commands to operate on, regardless of whether or not these changes have been applied by the CPE.

As an example, @tbl:simple-router-example-interfacestack-table lists an InterfaceStack table configuration imagined for a fictitious, simple router. Each row in this table corresponds to a row in the InterfaceStack table. The specified objects and instance numbers are manufactured for the sake of this example; real world configurations will likely differ.

:Simple Router Example (InterfaceStack table)

| Row/Instance     | Higher Layer Interface                | Lower Layer Interface
|------------------|---------------------------------------|-----------------------------------------
| 1                | Device.IP.Interface.1                 | Device.PPP.Interface.1
| 2                | Device.PPP.Interface.1                | Device.Ethernet.Link.1
| 3                | Device.Ethernet.Link.1                | Device.ATM.Link.1
| 4                | Device.ATM.Link.1                     | Device.DSL.Channel.1
| 5                | Device.DSL.Channel.1                  | Device.DSL.Line.1
| 6                | Device.IP.Interface.2                 | Device.Ethernet.Link.2
| 7                | Device.Ethernet.Link.2                | Device.ATM.Link.2
| 8                | Device.ATM.Link.2                     | Device.DSL.Channel.1
| 9                | Device.IP.Interface.3                 | Device.Ethernet.Link.3
| 10               | Device.Ethernet.Link.3                | Device.Bridging.Bridge.1.Port.1
| 11               | Device.Bridging.Bridge.1.Port.1       | Device.Bridging.Bridge.1.Port.2
| 12               | Device.Bridging.Bridge.1.Port.2       | Device.Ethernet.Interface.1
| 13               | Device.Bridging.Bridge.1.Port.1       | Device.Bridging.Bridge.1.Port.3
| 14               | Device.Bridging.Bridge.1.Port.3       | Device.Ethernet.Interface.2
| 15               | Device.Bridging.Bridge.1.Port.1       | Device.Bridging.Bridge.1.Port.4
| 16               | Device.Bridging.Bridge.1.Port.4       | Device.WiFi.SSID.1
| 17               | Device.WiFi.SSID.1                    | Device.WiFi.Radio.1

By looking at the rows from the example InterfaceStack table as a whole, we can visualize the overall stack configuration. @fig:simple-router-example-interfaces-visualized shows how this information can be pictured. Interface instances are represented by colored boxes, while InterfaceStack instances are represented by numbered circles.

![Simple Router Example (Interfaces Visualized)](/images/simple-router-example-interfaces-visualized.png)

::: note
"Device." should be considered prepended to each parameter name in @fig:simple-router-example-interfaces-visualized. It is left off to make the figure more legible.
:::

Finally, @tbl:simple-router-example-interface-lowerlayers completes the example by listing each interface instance and its corresponding LowerLayers parameter value.

:Simple Router Example (Interface LowerLayers)

| Interface                       | LowerLayers value
|---------------------------------|-------------------------------------------------------------------
| Device.IP.Interface.1           | Device.PPP.Interface.1
| Device.IP.Interface.2           | Device.Ethernet.Link.2
| Device.IP.Interface.3           | Device.Ethernet.Link.3
| Device.PPP.Interface.1          | Device.Ethernet.Link.1
| Device.Ethernet.Link.1          | Device.ATM.Link.1
| Device.Ethernet.Link.2          | Device.ATM.Link.2
| Device.Ethernet.Link.3          | Device.Bridging.Bridge.1.Port.1
| Device.Bridging.Bridge.1.Port.1 | Device.Bridging.Bridge.1.Port.2, Device.Bridging.Bridge.1.Port.3, Device.Bridging.Bridge.1.Port.4
| Device.Bridging.Bridge.1.Port.2 | Device.Ethernet.Interface.1
| Device.Bridging.Bridge.1.Port.3 | Device.Ethernet.Interface.2
| Device.Bridging.Bridge.1.Port.4 | Device.WiFi.SSID.1
| Device.ATM.Link.1               | Device.DSL.Channel.1
| Device.ATM.Link.2               | Device.DSL.Channel.1
| Device.DSL.Channel.1            | Device.DSL.Line.1
| Device.DSL.Line.1               |
| Device.Ethernet.Interface.1     |
| Device.Ethernet.Interface.2     |
| Device.WiFi.SSID.1              | Device.WiFi.Radio.1
| Device.WiFi.Radio.1             |
