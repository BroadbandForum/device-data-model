# Use Cases {.appendix .same-file}

This section presents a number of management-related use cases that correspond to typical Controller activities.

## Create a WAN Connection

The Controller can create the objects in the interface stack bottom-up. Each time a new higher-layer object is created, the link with the underlying interface object needs to be set. The layer 1 interface, in this case a DSL.Channel and DSL.Line object, will already exist (A Controller cannot create physical interfaces).

#. The Controller creates a new ATM.Link object, a new Ethernet.Link object, a new PPP.Interface object, and a new IP.Interface object.

#. The LowerLayers parameter in an existing DSL.Channel object is already linked to an existing DSL.Line object (A Controller cannot configure this linkage).

#. The Controller configures the new objects including enabling the objects and using the LowerLayers parameters as follows:

    * Setting the LowerLayers parameter in the ATM.Link object to link it to an existing DSL.Channel object that is configured with ATM encapsulation (i.e., the read-only LinkEncapsulationUsed parameter in the DSL.Channel object is set to one of the ATM-related enumeration values).
    * Setting the LowerLayers parameter in the Ethernet.Link object to link it to the ATM.Link object.
    * Setting the LowerLayers parameter in PPP.Interface object to link it to the Ethernet.Link object.
    * Setting the LowerLayers parameter in IP.Interface object to link it to the PPP.Interface object.

#. The CPE updates the InterfaceStack table automatically. The stack looks like this: IP.Interface &rarr; PPP.Interface &rarr; Ethernet.Link &rarr; ATM.Link &rarr; DSL.Channel &rarr; DSL.Line.

#. Note that the Controller might also want to update other related objects, including the NAT object, the Routing.Router object, or various QoS and Bridging tables. VLANs might also need to be created.

## Modify a WAN Connection

In this use case, the Controller needs to modify an existing WAN connection, in order to insert a new layer in the stack or to change some portion of the interface stack. This is not the management WAN connection. For the purposes of this example, the Controller is changing the WAN connection in the *[Create a WAN Connection]* use case to make use of PTM rather than ATM-based aggregation.

#. The Controller creates a new PTM.Link object.

#. The Controller configures the objects, including enabling the new PTM.Link object and using the LowerLayers parameter as follows:

    * Setting the LowerLayers parameter in the PTM.Link object to link it to an existing DSL.Channel object that is configured with PTM encapsulation (i.e., the read-only LinkEncapsulationUsed parameter in the DSL.Channel object is set to one of the PTM-related enumeration values).
    * Setting the LowerLayers parameter in the Ethernet.Link object to refer to the PTM.Link object rather than the ATM.Link object.
    * Setting the LowerLayers parameter in the IP.Interface object to refer to the Ethernet.Link object rather than the PPP.Interface object.

#. The CPE updates the InterfaceStack table automatically. The stack looks like this: IP.Interface &rarr; Ethernet.Link &rarr; PTM.Link &rarr; DSL.Channel &rarr; DSL.Line.

#. Note that the Controller might also want to update other related objects, including the Bridging table. The Controller might also want to delete the existing PPP.Interface and ATM.Link objects.

## Delete a WAN Connection

Assume that we want to delete the WAN connection as it is configured in the *[Create a WAN Connection]* use case.

#. The Controller deletes the IP.Interface object.

#. The Controller deletes the PPP.Interface object.

#. The Controller deletes the Ethernet.Link object.

#. As each of these objects is deleted, the InterfaceStack is adjusted automatically by the CPE.

#. Any strong references to the deleted objects, e.g., in Device.QoS classification rules, will automatically be set to empty strings.

## Discover whether the Device is a Gateway

Many operators want to determine if a particular device is a "gateway" or not. The term "gateway", however, is rather vague; usually the operator wants to know one (or more) of the following things:

#. If the device terminates the WAN connection(s).

#. If the device is responsible for providing DHCP addresses to the other devices in the home.

#. If the device provides functionality such as NAT or routing capabilities.

In order to determine if the device terminates a WAN connection, the Controller might look for an interface object with a technology that is by definition WAN (such as DSL) or for a technology that could be a WAN termination technology (such as Ethernet or MoCA).

In order to determine if the device is responsible for providing addresses to other devices in the home, the Controller could check for the existence of the DHCP Server object. The existence of the Host table also indicates that the device is aware of Hosts, by whatever means they're addressed.

For CWMP managed CPEs, the existence of the ManageableDevice table within the ManagementServer object also indicates that the device serves as the DHCP server for the TR-069 managed device exchange defined in TR-069 [@TR-069] Annex F, which is also often an indication of "gateway" functionality.

In order to determine if the device provides functionality such as NAT or a router, the Controller would check for the existence of an enabled NAT or Routing.Router object.

## Provide Extended Home Networking Topology View

Another use case is to determine the topology of the home network behind the gateway. For a generic understanding of the network, the Host table provides information such as the layer 2 and layer 3 interfaces via which the Host is connected as well as DHCP lease information for each connected Host.

If the operator is interested in UPnP devices in the home network, the UPnP.Discovery tables (RootDevice, Device, and Service) provide that information in addition to the Host table entries that correspond to a particular UPnP Root Device, Device, or Service.

Finally for CWMP enabled CPEs, the ManageableDevice table within the ManagementServer object provides information about the CWMP managed devices that the CPE has learned about through the DHCP message exchange defined in TR-069 [@TR-069] Annex F.

## Determine Current Interfaces Configuration

One of the most fundamental Controller tasks is to determine the general picture of the interfaces for a device so that it can understand which WAN and LAN side connections exist.

In the Device:2 data model managed with CWMP, it would work this way:

#. The ACS would issue a GetParameterValues for the InterfaceStack table. This table would provide a list of all the Interface connections. The ACS could use this table to build up the general picture of the Interfaces that are part of the current configuration.

#. If the ACS is interested in the specifics of an individual interface, it can then go and issue GetParameterNames or GetParameterValues for the interfaces of interest.

If the CPE is managed by USP:

#. The USP Controller would issue a Get request for the InterfaceStack table. This table would provide a list of all the Interface connections. The USP Controller could use this table to build up the general picture of the Interfaces that are part of the current configuration.

#. If the USP Controller is interested in the specifics of an individual interface, it can then go and issue a filtered Get request message for the interfaces of interest.

## Create a WLAN Connection

In this use case the Controller creates a new WLAN connection. For the purposes of illustration, in this example the Controller will create a new SSID object to link to an existing radio (a new SSID object implies a different SSID value than those used by existing WiFi connections). The layer 1 interface, in this case a WiFi.Radio object, will already exist (Controller can not create physical interfaces).

#. The Controller creates a new WiFi.SSID object and WiFi.AccessPoint object.

#. The Controller configures the new WiFi.SSID object, including enabling it and setting the value of the LowerLayers parameter to reference the device's WiFi.Radio object.

#. The Controller adds the new WiFi.SSID object to the LowerLayers parameter of an existing non-management Bridging.Bridge.{i}.Port object, as appropriate.

   ::: note
   A non-management bridge port is indicated when its ManagementPort parameter is set to false.
   :::

#. The Controller configures the new WiFi.AccessPoint object, including enabling it and sets the value of its SSIDReference parameter to reference the WiFi.SSID object.

#. The CPE updates the InterfaceStack table automatically.

#. Note that the Controller might also want to update other related objects; also, if there were no appropriate existing bridge port to which to connect the SSID, the Controller might need to create that object as well.

## Delete a WLAN Connection

In this use case the Controller deletes the SSID created in the *[Create a WLAN Connection]* use case.

#. The Controller deletes the WiFi.SSID object and the WiFi.AccessPoint object.

#. The CPE automatically updates the InterfaceStack table.

#. Note that if the radio has no other SSIDs configured, this would operationally disable the wireless interface.

## Configure a DHCP Client and Server

In this use case, the Controller wants to configure a DHCP server to provide private 192.168.1.x IP addresses to most home network (HN) devices, but to obtain IP addresses from the network for HN devices that present an option 60 (vendor class ID) value that begins with "ACME".

The ACME devices are remotely managed, so the Controller will also configure the DHCP clients on those devices and the DHCP server on the gateway.

### DHCP Client Configuration (ACME devices)

The ACME devices are quite simple. Each has a single wired Ethernet port and a single IP interface.

A DHCP Client object is created and configured as follows:

|                                                  |
|--------------------------------------------------|-----------------------------
| DHCPv4.Client.1.Enable                           | *true*
| DHCPv4.Client.1.Interface                        | Device.IP.Interface.1
|                                                  |
| DHCPv4.Client.1.SentOption.1.Enable              | *true*
| DHCPv4.Client.1.SentOption.1.Tag                 | 60
| DHCPv4.Client.1.SentOption.1.Value               | "ACME Widget" (as hexBinary)

### DHCP Server Configuration (gateway)

The gateway is also relatively simple. Its downstream IP interface is IP.Interface.1.

A DHCP Server object is created and configured as follows:


|                                                  |
|--------------------------------------------------|-----------------------------
| DHCPv4.Server.Enable                             | *true*
| DHCPv4.Relay.Enable                              | *true*
|                                                  |
| DHCPv4.Relay.Forwarding.1.Enable                 | *true*
| DHCPv4.Relay.Forwarding.1.Interface              | Device.IP.Interface.1
| DHCPv4.Relay.Forwarding.1.VendorClassID          | "ACME"
| DHCPv4.Relay.Forwarding.1.VendorClassIDMode      | "Prefix"
| DHCPv4.Relay.Forwarding.1.LocallyServed          | *false*
| DHCPv4.Relay.Forwarding.1.DHCPServerIPAddress    | 1.2.3.4
|                                                  |
| DHCPv4.Server.Pool.1.Enable                      | *true*
| DHCPv4.Server.Pool.1.Interface                   | Device.IP.Interface.1
| DHCPv4.Server.Pool.1.MinAddress                  | 192.168.1.64
| DHCPv4.Server.Pool.1.MaxAddress                  | 192.168.1.254
| DHCPv4.Server.Pool.1.ReservedAddresses           | 192.168.1.128, 192.168.1.129
| DHCPv4.Server.Pool.1.SubnetMask                  | 255.255.255.0

If a DHCP request includes an option 60 value that begins with "ACME", the request is forwarded to the DHCP server at 1.2.3.4. All other requests are served locally from the pool 192.168.1.64 - 192.168.1.254 (excluding 192.168.1.128 and 192.168.1.129).

## Reconfigure an Existing Interface

The Controller might want to reconfigure an existing Interface to provide alternate routing functionality. For the purposes of this illustration, an existing Ethernet Interface that is configured for the downstream-side will be reconfigured as an upstream Ethernet Interface replacing an existing DSL Interface.

The current configuration on the upstream side looks like:

IP.Interface.1 &rarr; Ethernet.Link.1 &rarr; ATM.Link.1 &rarr; DSL.Channel.1 &rarr; DSL.Line.1

The current configuration on the downstream side contains:

* IP.Interface.2 &rarr; Ethernet.Link.2 &rarr; Bridging.Bridge.1.Port.1 (ManagementPort=true)
* Bridging.Bridge.1.Port.1 LowerLayers parameter has two references:
    * Bridging.Bridge.1.Port.2
    * Bridging.Bridge.1.Port.3
* Bridging.Bridge.1.Port.2 LowerLayers parameter has a reference of Ethernet.Interface.1
* Bridging.Bridge.1.Port.3 LowerLayers parameter has a reference of Ethernet.Interface.2

The Controller would follow these steps to reconfigure the Ethernet.Interface:

#. Determine which Ethernet.Interface is to be reconfigured. For the purpose of this illustration we will use Ethernet.Interface.1.

#. Retrieve the InterfaceStack.

#. Find the higher-layer Interface of Ethernet.Interface.1 by finding the InterfaceStack entry that has Ethernet.Interface.1 as the LowerLayer. The HigherLayer parameter of the identified InterfaceStack instance will be the Interface we are interested in, for the purpose of this illustration we found Bridging.Bridge.1.Port.2.

#. Remove the Bridging.Bridge.1.Port.2. This removal will automatically clean up the InterfaceStack instances that connect Bridging.Bridge.1.Port.1 &rarr; Bridging.Bridge.1.Port.2 and Bridging.Bridge.1.Port.2 &rarr; Ethernet.Interface.1. Also, it will remove Bridging.Bridge.1.Port.2 from the LowerLayers parameter contained within Bridging.Bridge.1.Port.1.

#. Find the DSL.Line reference within the LowerLayer parameter of the InterfaceStack.

#. Follow the InterfaceStack up to the Ethernet.Link reference by looking at the HigherLayer parameter in the current InterfaceStack instance and then finding the InterfaceStack instance containing that Interface within the LowerLayer parameter until the HigherLayer reference is the Ethernet.Link Interface. For the purpose of this illustration, we found Ethernet.Link.1.

#. Reconfigure the LowerLayers parameter of Ethernet.Link.1 such that its value is "Device.Ethernet.Interface.1" instead of "Device.ATM.Link.1".

#. The CPE updates the InterfaceStack table and sets the Upstream parameter to true on the Ethernet.Interface.1 instance automatically.

#. Note that the Controller might also want to update other related objects, including the NAT object, the Routing.Router object, or various QoS and Bridging tables. VLANs might also need to be created.

After the CWMP Session is completed and the CPE commits the configuration, the upstream side will look like:

* IP.Interface.1 &rarr; Ethernet.Link.1 &rarr; Ethernet.Interface.1

## Backup / Restore Using Vendor Configuration Files

::: note
This use case is written from a CWMP perspective, but would also apply to USP.
:::

In certain troubleshooting scenarios, a Device that has its user configuration modified in a manner that cannot be easily restored by setting individual parameters can have the Device's user configuration restored by applying a previous user configuration to the Device. When performing a backup and restoration of configuration files, the Controller can correlate the instance number of the VendorConfigFile retrieved during backup (Upload RPC) operation with the URL of the restore (Download) operation. The following sequence diagrams depict a backup and restoration scenario that correlates these attributes of a configuration file.

@fig:device-user-configuration-backup depicts a message sequence scenario where a configuration is **backed up** from the Device to the ACS using CWMP.

![Device User Configuration Backup](/images/device-user-configuration-backup.png)

Step 1: Retrieve instances and values of VendorConfigFile and DeviceInfo:

The parameter values of the DeviceInfo and VendorConfigFile provide the information necessary to restore a Device to a point in time. Minimally the information needed to create a snapshot includes:

* Device.DeviceInfo.ManufacturerOUI
* Device.DeviceInfo.ProductClass
* Device.DeviceInfo.SerialNumber
* Device.DeviceInfo.HardwareVersion
* Device.DeviceInfo.SoftwareVersion
* Device.DeviceInfo.VendorConfigFile.{i}. (Entire object)
* Device.SoftwareModules.DeploymentUnit.{i}.UUID
* Device.SoftwareModules.DeploymentUnit.{i}.Alias
* Device.SoftwareModules.DeploymentUnit.{i}.Name
* Device.SoftwareModules.DeploymentUnit.{i}.Version
* Device.SoftwareModules.DeploymentUnit.{i}.VendorConfigList

::: note
Only instances of DeploymentUnit with VendorConfigFile instances with the UseForBackupRestore parameter set to the value true as items in the instance's VendorConfigList parameter will need to be backed up.
:::

This information is necessary as restoring Device configurations with different hardware versions, software versions or deployment units that existed at the time of the backup can result in a failed restoration attempt or a corrupted Device.

Step 1a: The parameters returned by the Device in the GetParameterValuesResponse are used to create a "snapshot" of the Device. The definition of what is needed to create a snapshot and how a snapshot is administered in an ACS is implementation specific.

Step 2: Backup each configuration file defined by the Device in the VendorConfigFile table with the UseForBackupRestore parameter set to the value "true" using the Upload RPC with a File Type "3 Vendor Configuration File x" where "x" is the instance number of the file in the VendorConfigFile table.

::: note
An ACS can also have additional information, outside step 1, to discern which configuration files are necessary to restore a Device, as well as the order in which the configuration files need to be restored where dependencies exist between the configuration files within the potential snapshot.
:::

Step 3, 3a: Upon completion of the transfer for each file via the Transfer Complete event, the ACS will update the state of the snapshot. The lifecycle and state management of the snapshot by an ACS is implementation specific.

At this point a Device snapshot exists that can be used to restore a Device to this point in time.

@fig:device-user-configuration-restore depicts a message sequence scenario where a configuration is **restored** to the Device from the ACS

![Device User Configuration Restore](/images/device-user-configuration-restore.png)

Step 1: For each user configuration file in the snapshot, retrieve the information for the location of the configuration file.

Step 2, 2a: Download the configuration using the File Type "3 Vendor Configuration File" and the location of the configuration file.

::: note
Other elements (e.g., credentials) might be required but are outside the scope of this sequence. When downloaded, a VendorConfigFile instance with the same value for Name or Alias (if supported and present) will update the corresponding instance in the VendorConfigFile table and will not create a new entry within the table.
:::

Step 3, 3a: The Device performs the download of each configuration file and responds with a Transfer Complete event.

