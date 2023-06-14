# Purpose and Scope {.new-page}

## Purpose

This %bbfType% defines version 2 of the Device data model (Device:2). The Device:2 data model applies to all types of TR-069 or USP enabled devices, including End Devices, Residential Gateways, and other Network Infrastructure Devices.

## Scope

The Device:2 data model defined in this %bbfType% consists of a set of data objects covering things like basic device information, time-of-day configuration, network interface and protocol stack configuration, routing and bridging management, throughput statistics, and diagnostic tests. It also defines a baseline profile that specifies a minimum level of data model support.

The cornerstone of the Device:2 data model is the interface stacking mechanism. Network interfaces and protocol layers are modeled as independent data objects (a.k.a. interface objects) that can be stacked, one on top of the other, into whatever configuration a device might support.

Because the Device:2 data model can be used with either the USP or the CWMP (TR-069) protocol, it contains some objects and parameters which only apply if the specific protocol is used.

@{fig:cwmp-specific-device2-data-model-structure--overview} illustrates the top-level Device:2 data model structure for CWMP, @{fig:usp-specific-device2-data-model-structure--overview} the top-level Device:2 data model structure for USP.

![CWMP-specific Device:2 Data Model Structure -- Overview](/images/tr-181-2-cwmp-overview.png)

![USP-specific Device:2 Data Model Structure -- Overview](/images/tr-181-2-usp-overview.png)

### Detailed structure for common elements {.new-page}

The next figures illustrate the data model structure of the common parts in greater detail. This structure applies equally for USP and CWMP. See *[Parameter Definitions]* for the complete list of objects.

![Device:2 Data Model Structure -- Device Level](/images/tr-181-2-usp-device.png)

![Device:2 Data Model Structure -- Common Interface Stack and Networking Technologies](/images/tr-181-2-usp-ifstack.png)

![Device:2 Data Model Structure -- Common Applications and Protocols](/images/tr-181-2-usp-protocols.png)

### Detailed structure for CWMP specific elements

The next figures illustrate the data model structure of the CWMP specific parts in greater detail. See *[Parameter Definitions]* for the complete list of objects.

![Device:2 Data Model Structure -- CWMP Management](/images/tr-181-2-cwmp-cwmp-management.png)

![Device:2 Data Model Structure -- CWMP-specific applications and protocols](/images/tr-181-2-cwmp-cwmp-protocols.png)

### Detailed structure for USP specific elements {.new-page}

The next figures illustrate the data model structure of the USP specific parts in greater detail. See *[Parameter Definitions]* for the complete list of objects.

![Device:2 Data Model Structure -- USP Management](/images/tr-181-2-usp-usp-management.png)

![Device:2 Data Model Structure -- USP-specific applications and protocols](/images/tr-181-2-usp-usp-protocols.png)

