# MTU configuration Theory of Operations {.appendix .same-file}
## Introduction - Understanding MTU in Layer 2 and Layer 3 Networks
The Maximum Transmission Unit (MTU) defines the maximum size of data packets that can be transmitted across a network segment without fragmentation. MTU values are crucial for efficient data transmissions.

Two layers where MTU considerations are paramount are Layer 2 (Data Link Layer) and Layer 3 (Network Layer). Ethernet MTU, fundamental to Layer 2 networks, determines the maximum payload size within Ethernet frames. In contrast, IP MTU, governing Layer 3, defines the maximum size of IP packets, including headers and payloads. While both share a standard size of 1500 bytes.


:::{.list-table aligns=l,l}
  * - []{colspan=2} TR-181 MTU definitions

  * - Layer 2: `Ethernet.Link.{i}.MTU`
    - Maximum Transmission Unit for this interface (expressed in bytes).

  * - Layer 3: `IP.Interface.{i}.MaxMTUSize`
    - The maximum transmission unit (MTU); the largest allowed size of an IP packet (including IP
      headers, but excluding lower layer headers such as Ethernet, PPP, or PPPoE headers) that is allowed to be transmitted by or through this device.
:::
Typically the Layer 2 and Layer 3 is set to 1500 bytes.

## Use cases
Dynamic MTU Assignment: An upstream DHCP server may include MTU information in DHCP lease offers. When the Device or Gateway requests an IP address lease from the DHCP server, along with the IP address, subnet mask, default gateway, DNS server information, the DHCP server also provides the MTU size.

Jumbo Frames Support: Some network devices and applications support jumbo frames, which are frames with an MTU larger than the standard Ethernet MTU of 1500 bytes. Enabling jumbo frames by increasing the MTU size can improve throughput and reduce CPU overhead on networking equipment, particularly in high-performance computing environments.

Avoiding Fragmentation: In networks where packet fragmentation occurs frequently due to mismatched MTU sizes between different network segments, adjusting the MTU to a common size can help avoid fragmentation. Fragmentation can degrade performance and increase the processing overhead on routers and switches.



::: spacer :::
:::

## Interface example

:::{.list-table aligns=l,l}
  * - []{colspan=2}Simple Interface example (InterfaceStack table)
  * - Higher Layer Interface
    - Lower Layer Interface
  * - Device.Logical.Interface.1
    - Device.IP.Interface.1
  * - Device.IP.Interface.1
    - Device.Ethernet.Link.1
  * - Device.Ethernet.Link.1
    - Device.Ethernet.Interface.1
  * - []{colspan=2}Device.Ethernet.Interface.1
:::                                       

::: spacer :::
:::


## Simple Linux bridge example
:::{.list-table aligns=l,l}
  * - []{colspan=4}Simple Linux LAN Bridge example (InterfaceStack table)
  * - []{colspan=2}Higher Layer Interface
    - []{colspan=2}Lower Layer Interface
  * - []{colspan=2}Device.Logical.Interface.1
    - []{colspan=2}Device.IP.Interface.1
  * - []{colspan=2}Device.IP.Interface.1
    - []{colspan=2}Device.Ethernet.Link.1
  * - []{colspan=2}Device.Ethernet.Link.1
    - []{colspan=2}Device.Bridging.Bridge.1.Port.1
  * - []{colspan=2}Device.Bridging.Bridge.1.Port.1
    - []{colspan=2}Device.Bridging.Bridge.1.Port.2,
      Device.Bridging.Bridge.1.Port.3,
      Device.Bridging.Bridge.1.Port.4,
      Device.Bridging.Bridge.1.Port.5
  * - Device.Bridging.Bridge.1.Port.2
    - Device.Bridging.Bridge.1.Port.3
    - Device.Bridging.Bridge.1.Port.4
    - Device.Bridging.Bridge.1.Port.5
  * - Device.Ethernet.Link.2
    - Device.Ethernet.Link.3
    - Device.Ethernet.Link.4
    - Device.Ethernet.Link.5
  * - Device.Ethernet.Interface.1
    - Device.Ethernet.Interface.2
    - Device.Ethernet.Interface.3
    - Device.Ethernet.Interface.4    
:::                                       

::: spacer :::
:::
