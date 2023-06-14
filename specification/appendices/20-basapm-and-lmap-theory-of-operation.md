# BASAPM and LMAP Theory of Operation {.appendix .same-file}

Broadband Access Service Attributes and Performance Metrics (BASAPM) and Large-Scale Measurement of Broadband Performance (LMAP) data model components are derived from TR-304 [@TR-304] and the IETF LMAP information model [@RFC8193], respectively.

## TR-069 Family of Specifications in the Context of TR-304

This section describes possible deployment scenarios where the CWMP and IPDR protocols are used for the respective TR-304 protocols.

### TR-304 and IETF LMAP Frameworks

The IETF (LMAP) and BBF (TR-304) use a similar framework for diagnostics where each framework consists of a Measurement Controller, Data Collector and Measurement Agent. While there are differences between TR-304 and LMAP elements in various deployment scenarios, in residential scenarios the behavior of Measurement Agent in the home is consistent between the IETF LMAP and BBF TR-304 frameworks.

#### TR-304 Framework

The TR-304 framework consists of a Management Server that is used to manage and configure the Measurement Agent. This would also include receiving logging and status information as well as the capability to schedule the Measurement Agent for tests. The TR-304 framework also has a Measurement Controller with the responsibility to schedule the Measurement Agent for tests to be performed provide test admin control. TR-304 framework also has multiple channels where a Measurement Agent can send reports to the different Data Collectors.

![TR-304 Framework](/images/tr-304-framework.png)

#### IETF LMAP Framework

The IETF LMAP framework, like the BBF TR-304 framework, consists of a Management Server that is used to pre-configure the Measurement Agent. Note that this also could be done at the manufacturing stage of the device. The LMAP framework also has a Measurement Controller with the responsibility to configure the Measurement Agent for tests to be performed; provide instructions about the test and receive status and logging information the Measurement agents. In the IETF LMAP framework these functions are treated as individual channels that can be assigned to different Measurement Controllers. Likewise the Reporting interface also has multiple channels where a Measurement Agent can send reports to the different Data Collectors.

![LMAP Framework](/images/lmap-framework.png)

### CWMP for Pre-configuration

In the IETF LMAP and TR-304 frameworks, CWMP can be used to pre-configure the Measurement Agent; where the Controller and Data Collector could use other protocols (e.g., IETF LMAP protocol).

![CWMP for Pre-configuration](/images/cwmp-for-pre-configuration.png)

Note that in the TR-304 framework the Status and Logging functions have not been explicitly identified as capabilities of the Controller.

### CWMP for Control and Pre-configuration, IPDR for Reporting

In the IETF LMAP and TR-304 frameworks, CWMP can be used to pre-configure the Measurement Agent and manage/schedule the tests. Likewise the IPDR protocol can be used to report the test results. In this scenario, the ACS would act as the Management Server and Measurement Controller. This scenario would place a constraint on the IETF LMAP framework in that there would be allowed only 1 Measurement Controller per Measurement Agent. See *[Bulk Data Collection in the Context of LMAP]* for additional information on use of the BulkData.Profile object in the context of LMAP.

![CWMP for Control and Pre-configuration, IPDR for Reporting](/images/cwmp-for-control-and-pre-configuration-ipdr-for-reporting.png)

### CWMP as a Proxier, IPDR for Reporting

In scenarios where Measurement Agent does not have connectivity with the Measurement Controller, CWMP can be used to act as a proxy between the Measurement Controller and Measurement Agent. In this scenario, if the CWMP Proxy is an Embedded Device then both Measurement Agents are associated with the same ACS. If the Measurement Agents need to be associated with different Measurement Controllers then the CWMP Virtual Device mechanism is to be used.

![CWMP Proxy Device Deployment](/images/cwmp-proxy-device-deployment.png)

### Multi-ACS Deployment

In the IETF LMAP framework, the Measurement Agent could interact with different elements that implement the functionality of the Management Server and Measurement Controller. In addition, the IETF LMAP framework also permits the functionality of the Measurement Controller to be implemented in multiple elements.

For a CWMP framework, this would require a different CWMP Agent for each application. As such this type of scenario is not realistically supported by CWMP.

![CWMP Multi-ACS Deployment](/images/cwmp-multi-acs-deployment.png)

## Derivation of Data Model Elements

### Device.BASAPM

Device.BASAPM provides a TR-304 [@TR-304] wrapper for a Device.LMAP. MeasurementAgent instance. Device.BASAPM provides parameters related to the operational domain, device ownership, device identification, geographic location, and measurement reference point of a referenced Device.LMAP.MeasurementAgent instance.

### Device.LMAP.MeasurementAgent

The Device.LMAP objects and parameters are mostly described in the IETF LMAP information model [@RFC8193]. That document serves as the primary vehicle for describing theory of operations for Device.LMAP.MeasurementAgent.

The base Device.LMAP.MeasurementAgent.{i} object contains parameters defined in LMAP information model ma-config-obj, ma-status-obj, and ma-capability-obj. The ma-preconfig-obj parameters are not modeled in Device:2 data model , because there is no need for pre-configuration values in a CWMP/USP-managed Measurement Agent. The information model parameters map to Device:2 data model parameters as shown in @tbl:mapping-lmap-information-model-parameters-to-data-model-parameters:

:Mapping LMAP Information Model Parameters to Data Model Parameters

| IETF LMAP Information Model\
Parameter  | Device:2 data model parameter \
(in Device.LMAP.MeasurementAgent.{i})
|------------------------------------|-----------------------------------------------------------
| ma-config-agent-id                 | Identifier
| ma-config-credentials              | PublicCredential, PrivateCredential
| ma-config-group-id                 | GroupIdentifier
| ma-config-measurement-point        | MeasurementPoint
| ma-config-report-agent-id          | UseAgentIdentifierInReports
| ma-config-report-group-id          | UseGroupIdentifierInReports
| ma-config-report-measurement-point | UseMeasurementPointInReports
| ma-config-controller-timeout       | Controller. ControllerTimeout
| ma-status-last-started             | LastStarted
| ma-capability-hardware             | not included in Device.LMAP because it duplicates Device.DeviceInfo.HardwareVersion
| ma-capability-firmware             | not included in Device.LMAP because it duplicates Device.DeviceInfo.SoftwareVersion
| ma-capability-version              | Version
| ma-capability-tags                 | CapabilityTags

All of the other IETF LMAP information model parameters can be readily mapped to objects and parameters in Device.LMAP.MeasurementAgent.{i}.

## Bulk Data Collection in the Context of LMAP

The TR-069 family of specifications has defined protocols that can be used for the collection of bulk data between a CWMP Agent and an ACS. These protocols are defined for IPDR [@TR-232] and HTTP [@TR-069]. The Device:2 data model described in *[Derivation of Data Model Elements]* includes the ability to use these protocols for transferring test results between a Measurement Agent and a Data Collector.

When integrating the test results of the Device:2 data model (i.e., LMAP.Report object instance) into the bulk data objects and parameters provided by the Device:2 data model, the LMAP.Report object instance becomes the referenced parameter of the Bulk Data Profile (BulkData.Profile object instance). In addition, there is a linkage needed within the LMAP data model to identify the BulkData.Profile object instance. This is done through the reference of the BulkData.Profile object instance from the LMAP data model's Communication Channel for a Scheduled Action.

![Integration of Bulk Data Profiles with LMAP](/images/integration-of-bulk-data-profiles-with-lmap.png)

## TR-143 Diagnostics in LMAP

TR-143 [@TR-143] describes a set of tests that can be used within the context of TR-304 based on the IETF LMAP framework [@RFC7594] and Information Model [@RFC8193] and implemented using the Device:2 data model in *[Derivation of Data Model Elements]*. These tests could be defined using the following procedure:

#. The TR-143 diagnostic needs to be identified as a URI in the registry entry (Device.LMAP.MeasurementAgent.{i}.TaskCapability.{i}.Registry.{i}.RegistryEntry):
    * The URI is in the form of: urn:bbf:lmap:<BBF TR>:<DiagnosticProfileName>
    * For example a TR-143 upload diagnostic could be: "urn:bbf:lmap:tr-181-2-11-0:UploadDiagnostics-1"

#. The TR-143 diagnostic's parameters and objects that are modifiable by the Controller/Measurement Controller are encoded in the Device.LMAP.MeasurementAgent.{i}.Task.{i}.Option.{i}. or Device.LMAP.MeasurementAgent.{i}.Schedule.{i}.Action.{i}.Option.{i} objects.
    * For example: Device.IP.Diagnostics.UploadDiagnostics.DiagnosticsState=requested

#. The TR-143 diagnostic's parameters and objects that are read-only are encoded in the Device.LMAP.Report.{i}.Task.{i}.Result.{i}.Values where each parameter name is encoded in the Device.LMAP.Report.{i}.Task.{i}.ColumnLabels parameter.
    * For example:\
    ColumnLabels:\
    Device.IP.Diagnostics.UploadDiagnostics.PerConnectionResult.{1}.TotalBytesSent
    * Value: 30

::: note
These fully qualified names could be shortened or even specified as a different name based on the specification behind the RegistryEntry URN.
:::

