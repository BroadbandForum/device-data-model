# Logical Interfaces Theory of Operations {.appendix .same-file}
## Introduction
The intention of the logical interface concept is to simplify the configuration management of individual TR-181 services. Instead of configuring the individual network service with a physical or IP interface and dealing with reconfiguration problems that can occur during auto detection of WAN interfaces, the network interface can be configured with a logical interface. This allows the configuration of the network service to stay unchanged when switching between WAN interfaces. The software service responsible for managing WAN interface changes then only needs to care about rewriting the `LowerLayers` parameter of the `LogicalInterface` Objects.

![Logical interfaces problem statement](/images/logicalinterfaces-problem.png)

## Concept
The idea of the logical interface is that it represents simple arbitrary concepts such as:

* lan -> the LAN bridge interface
* wan -> the WAN interface
* data ->  interface to send data traffic (can be seen as a wan too)
* iptv -> interface used for only IPTV traffic
* voip -> interface used only for VoIP traffic
* mgmt -> interface used only for management traffic

Traditionally a network service such as a time server is configured by pointing  `Time.Server.{i}.Interface.` to a `Device.IP.Interface.{i}` object.

Now with logical interfaces, these types of services can be configured by using a Logical Interface instead of using an IP interface. For example:

`Time.Server.{i}.Interface = Device.Logical.Interface.1.`

And `Device.Logical.Interface.1.` would in this example be the WAN interface. And its LowerLayers parameter would be pointing to a stackable IP interface

## WAN mode changes
Requirement IF.WAN.ETH of TR-124 describes at a high-level what an internal service responsible for detecting the correct WAN interface must do. The logical interface concept avoids the need for a WAN mode manager that must be aware of all the specificities of the internal network services.

Logical interfaces significantly reduce the complexity of the WAN mode manager. Without it the WAN mode manager needs to be aware of all the network services, and how to configure them and maybe trigger a restart. By using the concept of the logical interfaces, the WAN mode manager only needs to reconfigure the network stack, and update the LowerLayers parameter of the logical interfaces.

Each individual internal network service must subscribe to the interface status updates.

When the interface is disabled and re-enabled, it is the responsibility of the internal service to retrieve the new lower interface and the associated IP address.

![Solution using logical interfaces](/images/logicalinterfaces-solution.png){typst-scale=0.6}

## How to use
A logical interface can be used on top of one or more stackable interfaces. [IPv4 and IPv6 on a different network interface](#sec:ipv4-and-ipv6-on-a-different-network-interface) is an example where a logical interface is layered on top of multiple IP interfaces. Most of the time a logical interface will just be layered on top of one IP interface. In theory a logical interface could be layered anywhere in the interface stack topology.

When a logical interface is used for configuring an `Interface` parameter, the logical interface will inherit the parameter type that has been declared in the data model. Meaning when the expected parameter type is `IP.Interface` the logical interface must resolve to an existing `IP.Interface`.

`Device.SSH.Server.2.Interface = "Device.Logical.Interface.1."`

:::{.list-table aligns=c,c}
  * - []{colspan=2} WAN Interface

  * - Interface
    - Logical.Interface.1

  * - LowerLayers
    - IP.Interface.2

  * - LowerLayers
    - Ethernet.Link.1

  * - LowerLayers
    - Ethernet.Interface.1

:::

::: spacer :::
:::

## Examples
### Tagged - untagged Ethernet switching
In this example the WAN mode manager decides to switch the network configuration from an untagged Ethernet traffic configuration to a tagged Ethernet configuration. This is a similar problem to when the WAN mode manager decides to switch between mono VC and a multi VC xDSL configuration.

#### Untagged Ethernet configuration
|WAN interface             |VOIP interface            |MGMT interface            |IPTV interface
|--------------------------|--------------------------|--------------------------|--------------------
|Logical.Interface.1       |Logical.Interface.2       |Logical.Interface.3       |Logical.Interface.4
|IP.Interface.1            |IP.Interface.1            |IP.Interface.1            |IP.Interface.1
|Ethernet.Link.1           |Ethernet.Link.1           |Ethernet.Link.1           |Ethernet.Link.1
|Ethernet.Interface.1      |Ethernet.Interface.1      |Ethernet.Interface.1      |Ethernet.Interface.1


::: spacer :::
:::

|Time server configuration |
|--------------------------|-------------------
|Time.Server.{i}.Interface |Logical.Interface.3

::: spacer :::
:::

#### Tagged Ethernet configuration
|WAN interface             |VOIP interface            |MGMT interface            |IPTV interface
|--------------------------|--------------------------|--------------------------|--------------------
|Logical.Interface.1       |Logical.Interface.2       |Logical.Interface.3       |Logical.Interface.4
|IP.Interface.1            |IP.Interface.2            |IP.Interface.3            |IP.Interface.4
|Ethernet.VLANTermination.1|Ethernet.VLANTermination.2|Ethernet.VLANTermination.3|Ethernet.VLANTermination.4
|Ethernet.Link.1           |Ethernet.Link.1           |Ethernet.Link.1           |Ethernet.Link.1
|Ethernet.Interface.1      |Ethernet.Interface.1      |Ethernet.Interface.1      |Ethernet.Interface.1

::: spacer :::
:::

|Time server configuration |
|--------------------------|-------------------
|Time.Server.{i}.Interface |Logical.Interface.3

::: spacer :::
:::

By using the logical interface method, it is not necessary any more to update the configuration of the time server when the WAN mode manager switches between a tagged and untagged WAN mode.

### IPv4 and IPv6 on a different network interface
In this example the Time server needs to use the IPv4 and IPv6 addresses of the WAN interfaces. In more traditional scenarios the IPv4 and IPv6 addresses are available on the same network interface, but in this example the IPv4 and IPv6 addresses are on different network interfaces.

:::{.list-table .valign-top aligns=c,c,c,c,c}
   * - []{colspan=2} WAN Interface
     - VOIP Interface
     - MGMT Interface
     - IPTV Interface

   * - []{colspan=2} Logical.Interface.1
     - Logical.Interface.2
     - Logical.Interface.3
     - Logical.Interface.4

   * - IP.Interface.1 (IPv4)
     - []{rowspan=2} IP.Interface.2 (IPv6)
     - []{rowspan=2} IP.Interface.3
     - []{rowspan=2} IP.Interface.4
     - []{rowspan=2} IP.Interface.5

  * - PPP.Interface.1

  * - []{colspan=2} Ethernet.VLANTermination.1
    - Ethernet.VLANTermination.2
    - Ethernet.VLANTermination.3
    - Ethernet.VLANTermination.4

  * - []{colspan=5} Ethernet.Link.1

  * - []{colspan=5} Ethernet.Interface.1
:::

::: spacer :::
:::

|Time server configuration |
|--------------------------|-------------------
|Time.Server.{i}.Interface |Logical.Interface.1

::: spacer :::
:::

With the help of the Logical Interface, the Time server can automatically retrieve the correct IPv4 or IPv6 address from the TR-181 data model without having to know all the details that come from a certain WAN mode or network configuration.

![Logical interfaces example: IPv4 and IPv6 are on different network interface](/images/logicalinterfaces-example2.png){typst-scale=0.6}
