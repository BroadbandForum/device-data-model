# ZigBee Theory of Operation {.appendix .same-file}

This section explains how the ZigBee Device:2 data model can be used for the management of ZigBee devices.

::: note
This Theory of Operation is explained using CWMP but the same principles also apply for USP.
:::

## CWMP management using the ZigBee data model

[@fig:usage-of-the-data-model-to-manage-zigbee-devices-with-tr-069; @fig:example-sequence-diagram-of-zigbee-management-with-tr-069] present the principle and an example basic sequence for the management of ZigBee devices using the Device:2 ZigBee data model. The ZigBee protocol is specified in [@ZigBee2007].

The ZigBee devices reside behind a CPE proxy and communicate with the ACS via this CPE proxy. The CPE proxy normally resides in a device such as a broadband router, i.e., a home gateway or an enterprise gateway, and it has a proxy function to translate CWMP messages to ZDO (ZigBee Device Object) function invocations based on the ZigBee data model. The proxy function translates the messages by using a mapping of ZigBee data model objects and CWMP methods to ZDO functions and their parameters. A ZigBee device management example using CWMP is shown in @fig:usage-of-the-data-model-to-manage-zigbee-devices-with-tr-069.

![Usage of the data model to manage ZigBee devices with TR-069](/images/usage-of-the-data-model-to-manage-zigbee-devices-with-tr-069.png)

![Example sequence diagram of ZigBee management with TR-069](/images/example-sequence-diagram-of-zigbee-management-with-tr-069.png)

This example shows how the ACS gets the network address of a ZigBee device by using TR-069 communication based on the ZigBee data model. The ACS performs a "GetParameterValues" CWMP method call containing the parameter "Device.ZigBee.ZDO.{i}.NetworkAddress" of the ZigBee data model, which refers to the ZigBee network address. The proxy function in the CPE proxy changes the received message to a ZDO message that calls some ZDO function on the ZigBee Coordinator. The ZigBee Coordinator manages the ZigBee devices according to the called ZDO function and sends the result (the searched network address, in this case) to the proxy. The proxy function changes the ZDO management result to a CWMP message which is denoted in @fig:example-sequence-diagram-of-zigbee-management-with-tr-069 as "GetParameterValuesResponse". The parameter name inside the parameter list is "Device.ZigBee.ZDO.{i}.NetworkAddress" and the corresponding value is "0x0fE3" (network address instance).

##  CWMP proxying mechanisms and the ZigBee data model

The following two issues related to the proxying of ZigBee devices with the standard TR-069 proxying mechanisms are out of scope of this document:

* Mapping of TR-069 methods plus data model objects/parameters to ZDO functions.
* Description of the exact approaches (and their differences) for proxying a ZigBee device (i) as a Virtual Device or (ii) as an Embedded Device.

However, the following example explains how the main needs of the proxying mechanisms have been taken into account and are covered by the designed data model.

Imagine, for example, a ZigBee coordinator that controls a network which contains, among others, a ZigBee device that is used in a home automation system, i.e., implements the Home Automation Application Profile (0104). Then, the instantiation of the data model for the CPE contains, among others, the following two parameter values (note that "ZC" stands for ZigBee coordinator):

    Device.ZigBee.ZDO.1.NodeDescriptor.LogicalType = "ZC"
    Device.ZigBee.ZDO.2.ApplicationEndpoint.1.ApplicationProfileId = "0104"

In order to reference and manage these devices with the EmbeddedDevice mechanism, the CPE instance would simply also include, among others, the following entries:

`Device.ManagementServer.EmbeddedDevice.1.Reference`

* (*pointing to*) `Device.DeviceInfo.TemperatureStatus.TemperatureSensor.2`

`Device.ManagementServer.EmbeddedDevice.1.ProtocolReference`

* (*pointing to*) `Device.ZigBee.ZDO.2.ApplicationEndpoint.1`

`Device.ManagementServer.EmbeddedDevice.2.DiscoveryReference`

* (*pointing to*) `Device.ZigBee.ZDO.1`

For setting the temperature for TemperatureSensor.2, for example, the TR-069 proxy would send a request through the ZigBee coordinator to the Application endpoint referenced by the ProxyReference parameter on the EmbeddedDevice instance. As indicated by the value of `Device.ManagementServer.EmbeddedDevice.1.Reference` in the above example`,` multiple sensors integrated in the same ZigBee device (i.e., same ZDO instance) can be modeled as different Embedded or Virtual devices while referring to the same ZDO object.

According to the ZigBee protocol, the discovery of ZigBee devices is the responsibility of the ZigBee coordinator. Thus, a ZDO instance that has a LogicalType="ZC" can be made a DiscoveryReference of the various EmbeddedDevice and VirtualDevice instances.

