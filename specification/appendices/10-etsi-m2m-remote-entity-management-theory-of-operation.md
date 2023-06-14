# ETSI M2M Remote Entity Management Theory of Operation {.appendix .same-file}

::: note
ETSI currently only endorses TR-069 [@TR-069] for management of M2M devices, but the principles would also apply for USP, even if the protocol is not mentioned in this appendix.
:::

@fig:etsi-high-level-functional-architecture below depicts the high level ETSI M2M functional architecture defined in section 4 of ETSI TS 102 690 [@ETSIM2MFA]. The Data Models defined [@ETSIM2MInterfaces] are used within CWMP enabled Devices and Gateways within the Device and Gateway domain.

![ETSI High Level Functional Architecture](/images/etsi-high-level-functional-architecture.png)

Within the Device and Gateway Domain, the M2M Device and Gateway contains 2 functional components as defined in the ETSI M2M Functional Architecture [@ETSIM2MFA]:

* M2M Service Capabilities: M2M functions that are to be shared by different M2M Applications.
* M2M Applications: Applications that run the service logic and use M2M Service Capabilities.

Interactions between components within the ETSI architecture are defined using reference points. @fig:m2m-scl-functional-architecture-framework below illustrates the Service Capability Layer (SCL) mId reference point that is of interest. A full explanation of the SCL reference points is provided in section 5 of the ETSI M2M Functional Architecture [@ETSIM2MFA].

![M2M SCL Functional Architecture Framework](/images/m2m-scl-functional-architecture-framework.png)

The M2M Device or Gateway SCL provides capabilities (functionality) for the following areas:

* Application Enablement (xAE)
* Generic Communication (xGC)
* Reachability, Addressing and Repository (xRAR)
* Communication Selection (xCS)
* Remote Entity Management (xREM)
* SECurity (xSEC)
* History and Data Retention (xHDR)
* Transaction Management (xTM)
* Compensation Broker (xCB)
* Telco Operator Exposure (xTOE)
* Interworking Proxy (xIP)

::: note
The «\ x\ » designates a capability is used in the context of the Device (D) or Gateway (G).
:::

The Data Model in [@ETSIM2MInterfaces] reflects the device management objects and parameters necessary to implement xREM functionality across the mId reference point as defined in Annex E of the ETSI Functional Architecture [@ETSIM2MFA] is depicted in @fig:m2m-rem-service-capability. In this instance, the Device Mgmt Client is considered a CWMP endpoint interface and the Device Mgmt Server is considered the ACS interface. In most situations, these endpoints and servers have an interface between the native Device, Gateway or Server environment and the SCL. In addition, the dIa reference point, using RESTful procedures, is used to discover M2M D' Devices and M2M Applications as well as proxy selected xREM management functions.

![M2M REM Service Capability](/images/m2m-rem-service-capability.png)

::: note
The mId reference point in this scenario would support CWMP for the exchange of "mgmtObjs" using the xREM procedures between SCLs while continuing to support the ETSI RESTful procedures (e.g., container management) for the exchange of other resources across the mId reference point.
:::

Within the ESTI M2M Functional Architecture, the xREM is responsible for the following management functions:

* General Management: Provides retrieval of information related to the M2M Device or Gateway that hosts the ETSI M2M Service Capability Layer (SCL).
* Configuration Management: Provides configuration of the M2M Device or Gateway's capabilities in order to support ETSI M2M Services and Applications.
* Diagnostics and Monitoring Management: Provides diagnostic tests and retrieves/receives alerts associated with the M2M Device or Gateway that hosts the SCL.
* Software Management: Maintains software associated with the SCL and M2M services.
* Firmware Management: Maintain firmware associated with the M2M Device or Gateway that hosts the SCL.
* Area Network Management: Maintains devices on the M2M Area Network associated with the SCL.
* SCL Administration: Provides administration capabilities in order to configure and maintain a SCL within the M2M Device or Gateway.

Within the customer premises, equipment is categorized within the ETSI M2M framework as a:

* M2M Gateway: A Gateway that runs M2M Application(s) using M2M Service Capabilities.
* M2M Device: A Device that runs applications using M2M capabilities and network domain functions. Depending on M2M capabilities of the M2M Device, the M2M Device is defined as a:
    * Device (D): provides M2M Service Capabilities (DSCL) that communicates to an NSCL using the mId reference point and to DA using the dIa reference point
    * Device' (D'): hosts a Device Application (DA) that communicates to a GSCL using the dIa reference point. D' does not implement ETSI M2M Service Capabilities
* Non-ETSI M2M compliant device (d): A device that connects to a SCL through the SCL's Interworking Proxy capability.

![ETSI M2M Devices and Gateways](/images/etsi-m2m-devices-and-gateways.png)

## ETSI M2M Area Networks

In the ETSI framework D' and d Devices that connect to a SCL within a M2M Device or Gateway are said to be "attached devices" and are organized by M2M Area Networks within the SCL. The mechanism that a M2M Gateway uses to identify M2M Area Networks and their associated devices is implementation specific.

## Device:2 Data Model and Functionality for ETSI M2M REM

Annex B of the ETSI M2M Functional Architecture [@ETSIM2MFA] provides a cross reference between the xREM management functions and the object instances and RPCs required to implement the management functionality. The following is a summary of the objects, services, components, RPCs and optional TR-069 functionality required by the ETSI M2M xREM solution.

The ETSI M2M xREM solution in Annex E of the ETSI M2M Managed Objects [[@ETSIM2MInterfaces] defines a cross reference of the following ETSI resources to the existing  Device:2 Data Model objects. These ETSI resources are:

* etsiDeviceInfo
* etsiDeviceCapability
* etsiMemory
* etsiTrapEvent
* etsiPerformanceLog
* etsiFirmware
* etsiSoftware
* etsiReboot

The implementation of these resources the use of the following objects from the data model:

* DeviceInfo.
* WiFi.
* SmartCardReaders.
* USB.
* HomePlug.
* MoCA.
* UPA.
* UPnP.
* Hosts.
* SoftwareModules.
* FaultMgmt. (Use for etsiTrapEvent)
* SelfTestDiagnostics.
* DeviceInfo.VendorLogFile. (Use for etsiPerformanceLog)
* ManagementServer.EmbeddedDevice.
* ManagementServer.VirtualDevice.

### TR-069 Functionality for ETSI M2M REM

In addition to the mandatory RPCs defined in TR-069 [@TR-069], the ETSI M2M xREM solution requires that a M2M Device or Gateway implement the following optional RPCs according to Section 9.2.1.11 of [@ETSIM2MFA]:

* Upload method
* ScheduleDownload method
* ScheduleInform method
* ChangeDUState method
* FactoryReset method

## Device:2 Data Model and Functionality for ETSI M2M REM

In addition to reusing objects and parameters, the ETSI M2M xREM solution defines extensions to the resource model for the following ETSI resources by defining extensions to the data model for the following ETSI resources:

* etsiSclMo
* etsiAreaNwkInfo
* etsiAreaNwkDeviceInfo

These resources provide administration of the SCL in order for the SCL in the Device or Gateway to communicate with SCLs in the network. In addition, these resources provide administration of the SCL for M2M Devices within the local M2M area network attached to a Device or Gateway in order to communicate with associated network SCLs.

The ETSI M2M Services Device model defines the ETSIM2M service in support of the xREM functionality.

### M2M Service SCL Execution Environment

CPEs that provide software execution capabilities have the option to implement the Gateway Service Capabilities Layer and Gateway Applications as software modules. When a SCL is implemented as a software module, each instance of the GSCL and GA would be represented as individual Deployment Units with the associated software and configuration files. For the GSCL the vendor configuration file could contain configuration elements (e.g., M2M Node Id, NSCL List) that would be returned from or necessary to perform the M2M Service Bootstrap and Service Connection Procedures.

### ETSIM2M Object

The ETSIM2M objects provide administration of the SCL instantiated within a Device or Gateway.

The primary administration functions of the service are to:

* Maintain the set of Network SCLs (NSCL) that the M2M Device or Gateway SCL is registered.
* Maintain the set of NSCLs to which the M2M Device or Gateway will "announce" local resources.
* Maintain a list of Store and Forward (SAF) policies associated with the access network provider for message handling between M2M Devices in the area network and the NSCL.
* Maintain a list of Store and Forward (SAF) policies associated with the access network provider for message handling between the gateway and the NSCL.
* Maintain a list of Store and Forward (SAF) policies associated with the M2M service provider for message handling between M2M Devices in the area network and the NSCL.
* Maintain a list of Store and Forward (SAF) policies associated with the M2M service provider for message handling between the gateway and the NSCL.
* Discovery and Maintenance of M2M Area Networks.
* Discovery and Maintenance of M2M Devices.

::: note
As a SCL instance within a M2M Device or Gateway is associated with one M2M service provider, the M2M Device or Gateway is capable of maintaining multiple SCL instances.
:::

#### M2M Service Bootstrap and Service Connection Procedures

In the ETSI M2M system, the M2M (Device or Gateway) Node must establish the capability to connect with a M2M Network Node before the SCLs are permitted to be registered using M2M Service Bootstrap and Service Connection procedures.

The M2M Service Bootstrap and Service Connection procedures are defined in section 8.2 of the ETSI M2M Functional Architecture [@ETSIM2MFA] and describe how some of the credentials are shared and obtained in order to establish a connections (e.g, HTTP TLS-PSK) during the exchange of RESTFul information over the mId reference point.

#### Rules for Instantiating a SCL Instance

A M2M Node is not modeled as a device management entity but is considered a logical representation of the M2M components in the M2M Device, M2M Gateway or the M2M Core. Such components include:

* One instance of a SCL
* An optional M2M Service Bootstrap procedure
* A M2M Service Connection procedure

A M2M Node is identified by a globally unique identifier, the M2M-Node-ID.

In addition to the logical representation of a M2M Node, the following are constraints of a M2M Node that reflect on why a M2M Device or Gateway would instantiate multiple SCL instances:

* A M2M Node is owned by one M2M Service Provider.
* A M2M Node is instantiated upon M2M Bootstrap procedure or pre-provisioning the M2M Device or Gateway with a M2M Service Provider.
* Multiple M2M Nodes MAY be instantiated on the same M2M Device or Gateway by performing multiple M2M Bootstrap procedures either with the same M2M Service Provider or with different M2M Service Providers.

#### SCL Addressing

When a SCL is instantiated the SCL is provided a SCL-ID using the M2M Service Bootstrap procedure or through an out-of-band mechanism. Table 7.1 of the ETSI M2M Functional Architecture [@ETSIM2MFA] describes the characteristics of the SCL-ID.

When a M2M Device or Gateway SCL registers with a NSCL, the NSCL maintains the following information in its resource tree for the SCL that allows the NSCL to identify and contact the M2M Device or Gateway SCL:

* SCL-ID that globally unique and MAY be the same as the M2M-Node-ID.
* M2MPoCs contactInfo of the M2M Device or Gateway SCL -- This MAY be the FQDN, IP Address and port information or it MAY be other information that the M2M Service Provider can use to ask the network access provider for an IP Address.

#### SCL Registration

In order to communicate requests between the M2M Device or Gateway SCL and the NSCL, the M2M Device or Gateway SCL registers with the NSCL. Section 9.3.2.6.2 of the ETSI M2M Functional Architecture [@ETSIM2MFA] describes the registration process including how attributes such as the SCLID, search strings and expiration times are provisioned. In order for a M2M Device or Gateway SCL to register with the NSCL, the M2M Device or Gateway SCL must be provisioned with a list of potential NSCLs that the M2M Device or Gateway SCL is registered. In addition to the list of NSCLs, the M2M Device or Gateway SCL also has parameters to manage when a M2M Device or Gateway SCL re-registers with the NSCL. The M2M Device or Gateway SCL also has the capability to be requested to re-register with the NSCL through its TR-069 interface.

#### Discovery of M2M Devices through the SCL

Using the control plane, the M2M Device or Gateway SCL provides the capability to return a list of resources that the M2M Device or Gateway has discovered. Filtering MUST be performed on a subset of the offered resources' attributes using a query string. A match, that MAY include ranges, is performed on the query string, and a successful response is returned with a URI(s) list for resources that contains the matching attributes. Section 9.3.2.27 of the ETSI M2M Functional Architecture [@ETSIM2MFA] describes this procedure. The M2M Device or Gateway MAY be provisioned through the TR-069 interface to either limit the number of URIs discovered by the device or define the maximum size allowed for a discovery result.

#### De/Announcing M2M Devices through the SCL

One capability of the M2M Device or Gateway SCL control plane is to announce or de-announce M2M resources (e.g., access rights, applications) to NSCL(s) to which the M2M Device or Gateway SCL has registered if the SCL is contained within the "AnnounceToSCLList". Section 9.3.2.28 of the ETSI M2M Functional Architecture [@ETSIM2MFA] describes this procedure. The "AnnouncedToSCLList" is maintained through the TR-069 interface.

#### SCL Store and Forward Policies

The M2M Device or Gateway SCL is responsible for handling requests from an attached M2M Device or itself and the NSCL. The handling of the requests is based on criteria within the request (e.g., Request category [RCAT], Tolerable Request Processing Delay [TRPDT]) as well as conditions within the M2M Device or Gateway SCL (e.g., pending requests, access network availability).

There are two types of SCL store and forward (SAF) policies:

* Access Network Provider SAF Policies
* Service Provider SAF Policies

The SAF policies are organized into instances of Policy sets. The selection of which Policy sets are used by the M2M Device or Gateway SCL is determined by the PolicyScope attribute of the Policy set.

Section 9.3.1.5 of the ETSI M2M Functional Architecture [@ETSIM2MFA] describes this procedure. These policies are maintained through the TR-069 interface.

##### Access Network Provider SAF Policies

Access Network Provider SAF policies are used by M2M Device or Gateway SCLs to determine if an Access Network is to be used when forwarding requests from the M2M Device or Gateway SCL to the NSCL. The determination of which Access network to use is based on:

* Schedule of RCAT values versus time: The M2M Device or Gateway SCL is provisioned with information from the NSCL for the access network provider regarding when it is appropriate to forward requests of a given RCAT value.
* Blocking of access attempts after failure to establish connectivity: The M2M Device or Gateway SCL is provisioned with information from the NSCL for the access network provider regarding the period of time over which attempts to establish connectivity over its access network are not appropriate after the previous attempt to establish connectivity over the corresponding access network has failed. The period of time to block attempts to establish connectivity can be a function of the number of consecutive previous attempts to establish connectivity over this access network.

::: note
An Access Network Provider SAF is identified from the Access Network Provider name parameter.
:::

##### M2M Service Provider SAF Policies

M2M Service Provider Store and Forward (SAF) policies are used by M2M Device or Gateway SCLs to determine to forward a request to NSCL. The determination if the request is forwarded is based on the:

* Wait time as function of number of pending requests: The M2M Device or Gateway SCL is provisioned with information from the NSCL for the service provider regarding how many pending requests of a given range of RCAT values are sufficient to forward the aggregated request to the NSCL. The ranges of RCAT values for different policies cannot overlap.
* Wait time as function of amount of pending request data: The M2M Device or Gateway SCL is provisioned with information from the NSCL for the service provider regarding a threshold of consumed storage (memory) in the M2M Device or Gateway SCL that is needed to buffer data for pending requests of a given range of RCAT values. The ranges of RCAT values for different policies cannot overlap.
* Selection among appropriate access networks: The M2M Device or Gateway SCL is provisioned with information from the NSCL for the service provider regarding how to select an access network for making an attempt to establish connectivity from an ordered list of possible access networks for a given range of RCAT values. The ranges of RCAT values for different policies cannot overlap.
* Default values for TRPDT and RCAT: The M2M Device or Gateway SCL is provisioned with information from the NSCL for the service provider regarding the TRPDT and RCAT values to use if they are not provided by the request issuer.

#### Area Network Discovery and Maintenance

The M2M Device or Gateway SCL discovers properties of instances of M2M Area Networks as well as the Devices (D', d) associated with a M2M Area Network. A M2M Area Network is a logical entity in that an instance of an Area Network can span one or more physical interfaces of the M2M Device or Gateway. In addition, a M2M Gateway can provide connectivity to more than one instance of the same type of M2M Area Network. Examples of M2M Area Networks include: Personal Area Network technologies such as IEEE 802.15.x, Zigbee, Bluetooth, IETF ROLL, ISA100.11a or local networks such as PLC, M-BUS, Wireless M-BUS and KNX.

A M2M Area Network is maintained as instances of an AreaNwkInstance. Each AreaNwkInstance maintains opaque properties of the Area Network using Property instances of name/value pairs. In addition, the AreaNwkInstance also maintains a list of references to instances of AreaNwkDeviceInfoInstance table that are associated with the Area Network.

#### M2M Device Discovery and Maintenance

The M2M Device or Gateway maintains a list of discovered M2M Devices (D', d) that are attached to the SCL. A discovered M2M Device that is associated with more than one AreaNwkInstance is represented as multiple instances of AreaNwkDeviceInfoInstance objects.

![Example M2M Network](/images/example-m2m-network.png)

In @fig:example-m2m-network, an M2M Gateway has two (2) SCL instances that manage three (3) M2M Devices. Each M2M Device is represented in the Root Data Model's Hosts.Host table. The M2M Devices are represented by the AreaNwkDeviceInfoInstance object that was discovered within a context of an AreaNwkInstance of a SCL. As a M2M Device is capable of being discovered through multiple M2M Area Networks, different instances of the AreaNwkDeviceInfoInstance could reference the same or different Host table entry.

Each AreaNwkDeviceInfoInstance maintains a reference to an AreaNwkInstance object as well as properties specific to the device and area network association (e.g., SleepInterval). In addition, each AreaNwkDeviceInfoInstance maintains opaque properties of the device using Property instances of name/value pairs.

##### M2M Device Discovery and Maintenance

M2M Devices are able to be managed through the TR-069 Embedded Object and Virtual Device Proxy management capabilities. In these scenarios the AreaNwkDeviceInfoInstances are known as Discovered Devices.

In the scenario where a M2M Device (D', d) is discovered as part of an Embedded or Virtual Device, the AreaNwkDeviceInfoInstance is maintained as an item in the DiscoveryProtocolReference parameter of the Embedded or Virtual Device using one or more of the protocols listed in the DiscoveryProtocol parameter. @fig:m2m-device-discovery-for-proxy-management describes the scenario where the M2M Devices are discovered using the ETSI-M2M protocols.

![M2M Device Discovery for Proxy Management](/images/m2m-device-discovery-for-proxy-management.png)

#### SCL Configuration

The ETSI M2M Data Model includes the capability to provision the SCL with objects and parameters necessary for the SCL to host resources and transfer messages between M2M Devices and Gateway Applications and the NSCL. This section describes the minimal configuration necessary for an SCL to:

* Host resources
* Transfer messages

![ETSI M2M Data Model Structure](/images/etsi-m2m-data-model-structure.png)

@fig:etsi-m2m-data-model-structure depicts the objects within an ETSI SCL instance.

For deployments where the SCL will only host resources, the following resources must be provisioned:

    SCL.{1}.
        Enable = true

However for deployments where the SCL will transfer messages between M2M Applications and the NSCL, each SCL must have:

* An enabled SCL
* An enabled default SAFPolicySet
* At least 1 enabled ANPPolicy with an enabled Schedule for each of the enabled RequestCategory. There is one enabled RequestCategory instance for each possible RCAT value (e.g., 8 possible values in ETSI release 1.0)
* Within the M2MSPPolicy, there is one enabled RequestCategory instance for each possible RCAT value (e.g., 8 possible values in ETSI release 1.0)

As such the following resources must be provisioned:

    SCL.{1}.
        Enable = true
    SCL.{1}.SAFPolicySet.{1}.
        Enable = true
        PolicyScope= default
    SCL.{1}.SAFPolicySet.{1}.ANPPolicy.{1}.
        Enable = true
        ANName = *AccessNetworkProviderName*
    SCL.{1}.SAFPolicySet.{1}.ANPPolicy.{1}.RequestCategory.{1}.
        Enable = true
        RCAT = *RCAT1*
    SCL.{1}.SAFPolicySet.{1}.ANPPolicy.{1}.RequestCategory.{1}.Schedule.{1}.
        Enable = true
        Schedules = * * * * *
    .
    .
    SCL.{1}.SAFPolicySet.{1}.ANPPolicy.{1}.RequestCategory.{7}.
        Enable = true
        RCAT = *RCAT7*
    SCL.{1}.SAFPolicySet.{1}.ANPPolicy.{1}.RequestCategory.{7}.Schedule.{1}.
        Enable = true
        Schedules = * * * * *
    SCL.{1}.SAFPolicySet.{1}.M2MSPPolicy.RequestCategory.{1}.
        Enable = true
        RCAT = *RCAT7*
    *    *RankedANList = *AccessNetworkProviderName*
    .
    .
    SCL.{1}.SAFPolicySet.{1}.M2MSPPolicy.RequestCategory.{7}.
        Enable = true
        RCAT = *RCAT7*
        RankedANList = *AccessNetworkProviderName*

