# Wi-Fi Theory of Operation {.appendix .same-file}

This section discusses the theory of operations for various technologies in the Wi-Fi domain found within the Device:2 data model.

## Multi-radio and Multi-band Wi-Fi Radio Devices

The WiFi.Radio object description says "This object models an 802.11 wireless radio on a device. If the device can establish more than one connection simultaneously (e.g., a dual radio device), a separate WiFi.Radio instance will be used for representing each physical radio of the device."

The following sections clarify when multiple WiFi.Radio instances are needed, and the impact on their underlying parameters in the case of multi-radio and/or multi-band devices.

## Definitions

Each physical radio allows the transmission and reception of data on a single Wi-Fi channel at a given time. A single-radio device is able to transmit/receive a packet at a given time only on one Wi-Fi channel. Similarly, a dual-radio device is able to simultaneously transmit/receive data on two Wi-Fi channels. In general, a device with N radios is able to simultaneously transmit/receive data on N Wi-Fi channels.

An important point is that Wi-Fi can operate at different frequency bands, 2.4 GHz, 5 GHz and 6 GHz, as follows:

* Wi-Fi technologies based on IEEE 802.11b/g standard operate on the 2.4 GHz frequency band.
* Wi-Fi technologies based on IEEE 802.11a/ac standard operate on the 5 GHz frequency band.
* Wi-Fi technologies based on IEEE 802.11n standard operate on both the 2.4 and 5 GHz frequency bands.IEEE 802.11n is also called Wi-Fi 4 and High Throughput (HT).
* Wi-Fi technologies based on IEEE 802.11ac standard operate on the 5 GHz frequency band. IEEE 802.11ac is also called Wi-Fi 5 and Very High Throughput (VHT).
* Wi-Fi technologies based on IEEE 802.11ax standard operate on the 2.4, 5 and 6 GHz frequency bands. IEEE 802.11ax is also called Wi-Fi 6 and High Efficiency (HE).

Radios that operate at a single frequency band (e.g., 2.4 GHz only 802.11b/g devices) are called single-band radios. Radios that can operate in two frequency bands (e.g., 802.11a/b/g/n/ac/ax devices) are called dual-band radios, and radios that can operate in three bands (e.g., 802.11ax/Wi-Fi6E devices) are called tri-band radios.

A dual-band device can be a single-radio device if it can be configured to operate at 2.4 or 5 GHz frequency bands. However, only a single frequency band is used to transmit/receive at a given time. In such a case the device has a single physical radio that is dual-band.

Also, a dual-radio single-band device can exist (although uncommon) if both radios are single-band.

## Number of Instances of WiFi.Radio Object

Given the definitions above, a separate WiFi.Radio instance will be used for each physical radio of the device, i.e., one instance for a single-radio device, two instances for dual-radio devices, and so on. A single WiFi.Radio instance will therefore be used for a dual-band single-radio device.

Each WiFi.Radio instance is configured separately and is, in general, completely independent of other instances.

## SupportedFrequencyBands and OperatingFrequencyBand

The frequency band used by a WiFi device is an important parameter. With first generations of WiFi technologies, the specific frequency band was linked to the IEEE standard in use (i.e., 802.11b/g are 2.4 GHz standards, while 802.11a is a 5 GHz standard). With the introduction of the IEEE 802.11n standard, which can work both at 2.4 and 5 GHz, two specific parameters are used to indicate the supported frequency bands and the operating frequency band.

SupportedFrequencyBands is a list-valued parameter, containing one item for single-band radios (either 2.4GHz, 5GHz, or 6GHz) and two items for dual-band radios. 802.11ax can also operate in the 6 GHz band.

The OperatingFrequencyBand parameter specifies which frequency band is currently being used by a dual-band radio (i.e., set to one of the two items listed in the SupportedFrequencyBands parameter). For single-band radios, OperatingFrequencyBand always has the same value as SupportedFrequencyBands (since only one frequency band is supported).

## Behavior of Dual-band Radios when OperatingFrequencyBand Changed

When the configured operating frequency band of a dual-band radio is changed (i.e., the value of the OperatingFrequencyBand parameter is modified), this has an impact on other parameters within the WiFi.Radio object.

The Channel parameter has to be changed, since channels for the 2.4 GHz frequency band are in the range 1-14, while channels for the 5 GHz frequency band can be in the range of 36-165 (for example). The expected behavior is that, upon modifying the OperatingFrequencyBand parameter, the device automatically selects a new channel that is valid for the new frequency band (according to some vendor-specific selection procedure).

Other related parameters of significance for the Channel properties are AutoChannelEnable, OperatingChannelBandwidth and CurrentOperatingChannelBandwidth.

Persistence of the Channel parameter value for the previous frequency band is not required. For example, if OperatingFrequencyBand is later changed back to *5GHz*, a new valid value for the Channel parameter is automatically selected by the device, but this value need not be the same as was selected the last time OperatingFrequencyBand was set to *5GHz*.

Other parameters whose values can be impacted when the OperatingFrequencyBand changes, include: ExtensionChannel, PossibleChannels, SupportedStandards, OperatingStandards, IEEE80211hSupported, and IEEE80211hEnabled. If the current value is no longer valid, the device will automatically select a valid new value according to some vendor-specific procedure, and the old value need not persist.

## SupportedStandards and OperatingStandards

The SupportedStandards parameter is a list of all IEEE 802.11 physical layer modes supported by the devices. Wi-Fi is in general backward compatible, so 802.11g devices are also 802.11b devices, 802.11n devices are also 802.11b/g devices (if operating at 2.4 GHz), and 802.11n devices are also 802.11a devices (if operating at 5 GHz).

For dual-band radios, the OperatingFrequencyBand parameter is used for switching the operating frequency band. For this reason SupportedStandards only includes those values corresponding to operation in the frequency band indicated by the OperatingFrequencyBand parameter. For example, for dual-band 802.11a/b/g/n devices, SupportedStandards can be *b, g, n* when OperatingFrequencyBand is *2.4GHz* and *a, n, ac, ax* when OperatingFrequencyBand is *5GHz*. In addition an 802.11ax device can support tri-band operation in the 2.4, 5, and 6 GHz bands.

The OperatingStandards parameter is used to limit operation to a subset of physical modes supported. For example, an 802.11b/g/n radio will have *b, g, n* value for the SupportedStandards parameter, but can be configured to operate only with 802.11n by setting the OperatingStandards parameter to *n*.

## Different Types of WiFi Errors

This section first describes the different WiFi data units and the layers where they apply.

The MAC Service Data Unit (MSDU) is the service data unit that is received from the logical link control (LLC) sub-layer which lies above the medium access control (MAC) sub-layer in the protocol stack.

The MAC protocol data unit (MPDU) is a message exchanged between MAC entities in a communication system. "WiFi frames" refer to MPDUs and WiFi counters are counts of MPDUs.

The Physical Layer Convergence Procedure (PLCP) protocol data unit (PPDU) corresponds with the bits that are actually transmitted across the physical layer.

The MSDU is the frame that interfaces to higher layers, while the MPDU is the frame that is actually transmitted through the wireless medium, excluding the physical layer overhead. The MPDU is the MSDU plus MAC layer overhead (header, FCS, etc.). The PPDU is the MPDU plus physical layer overhead (preamble, PHY header, etc.).

The number of errored MPDUs is the number of MPDUs without corresponding ACKs. In most cases, the number of MSDUs is the same as the number of MPDUs. However, if fragmentation is enabled, then one MSDU can become multiple MPDUs, and there is one ACK per MPDU, hence multiple ACKs for one MSDU.

With frame aggregation in 802.11n, multiple MPDUs become one aggregated MPDU (A-MPDU). There is usually one block ACK for each A-MPDU, and only the errored MPDU(s) can be retransmitted selectively. In this case the WiFi counters will count the original MPDUs and not the A-MPDUs.

To avoid confusion that may be caused by fragmentation or frame aggregation, "WiFi frames" or packets are all considered here to be MPDUs and WiFi counters refer to MPDUs.

@fig:wifi-functions-within-layers explains the process of the MSDU/MPDU flow structure through the MAC layer of the WiFi receiver.

![WiFi functions within layers](/images/wifi-functions-within-layers.png)

PLCPErrorCount: This error occurs at point (1) in @fig:wifi-functions-within-layers, and is the first error type that can be counted. The PLCPErrorCount is the number of errors in the PLCP headers of the received MPDUs, which is the number of frames for which the parity check of the PLCP header failed.

There are two errors that happen at point (2) of the wireless reception:

* FCSErrorCount: This error occurs at point (2) in @fig:wifi-functions-within-layers. After the MPDU passes the PLCP header check, it is passed onto MAC layer validation. The FCSErrorCount is the number of frames for which the Frame Check Sequence (FCS) at the end of the MAC frame was in error.

* InvalidMACCount: This error also occurs at point (2) in @fig:wifi-functions-within-layers. The MAC header of the MPDU has a field called 'Protocol Version'. Currently, it is set to '0'. If this number is anything but 0, or the frame type is not data/control/management,' the InvalidMACCount is incremented.

After verifying that the frame was received without errors, the WiFi receiver will then check if the frame was designated for its own use or not (still MAC layer).

PacketsOtherReceived: This counter is used to catch those MPDUs that are not addressed to this radio. This can be assessed by checking if the 'Address 1' field of the 802.11 MAC header contains a MAC address that is associated with this radio, if not then 'PacketsOtherReceived' is incremented.

After this step, the AP can also discard duplicate frames or fragments among the frames addressed to it, to simplify higher-level processing.

The ErrorsReceived count is the sum of the PLCPErrorCount plus the FCSErrorCount plus the InvalidMACCount.

## Wi-Fi Data Elements

The Wi-Fi Alliance has specified Wi-Fi CERTIFIED Data Elements [@DataElements]. Wi-Fi Data Elements objects are under the Device.WiFi.DataElements. tree. Wi-Fi Data Elements Release 1.0 objects were put into Device:2.13, and Wi-Fi Data Elements Release 2.0 and Release 2.1 objects were put into Device:2.15.

In addition to Wi-Fi Data Elements, additional objects and parameters have been specified in TR-181 which are useful for managing Multi-AP Wi-Fi networks. These were originally in the Device.WiFi.MultiAP. tree, however the Device.WiFi.MultiAP. tree has been deprecated in Device:2.15, with some parameters deleted and other parameters moved into the structure of Wi-Fi Data Elements under the Device.WiFi.DataElements. tree. Objects whose titles contain “MultiAP” are not Wi-Fi Data Elements. These MultiAP objects are in the Device.WiFi.DataElements. tree to simplify the structure and avoid duplication, but they are not specified by the Wi-Fi Alliance.

The structure of Device.WiFi.DataElements. differs somewhat from that of the pre-existing Device.WiFi; and there is some overlap between these structures. Wi-Fi Native predates WiFi.DataElements, and Wi-Fi Native includes WiFi.Radio.{i}., WiFi.SSID.{i}, WiFi.AccessPoint.{i}. and WiFi.EndPoint.{i}. @tbl:objects-and-parameters-in-wi-fi-native-that-correspond-to-wi-fi-data-elements shows objects, parameters and commands in WiFi.DataElements which have a corresponding object or parameter in Wi-Fi Native. Note that many objects and parameters in WiFi.DataElements do not have any corresponding object or parameter in Wi-Fi Native and so are not listed in @tbl:objects-and-parameters-in-wi-fi-native-that-correspond-to-wi-fi-data-elements. Also, commands are only in the USP data model and are not in the CWMP data model. Further, Wi-Fi Data Elements' Network Device table, Device.WiFi.DataElements.Network.Device.{i}., represents all of the devices within Wi-Fi network while Device.WiFi represents only the Wi-Fi device that is being modeled. @tbl:objects-and-parameters-in-wi-fi-data-elements-that-correspond-to-wi-fi-native similarly shows objects and parameters in Wi-Fi Native which have a corresponding object or parameter in WiFi.DataElements.

::: {.list-table widths=50,50} :::

Objects and parameters in Wi-Fi Native that correspond to Wi-Fi Data Elements

- - Wi-Fi Data Elements
  - Wi-Fi Native

- []{.object}
  - Device.WiFi.DataElements.
  -

- []{.object}
  - Device.WiFi.DataElements.Network.
  -
- []{.command}
  - SetSSID()
  - Device.WiFi.SSID.{i}. (W)

- []{.object}
  - Device.WiFi.DataElements.Network.SSID.{i}.
  -
- - SSID
  - Device.WiFi.SSID.{i}. (W)

- []{.object}
  - Device.WiFi.DataElements.Network.Device.{i}.
  -
- - Manufacturer
  - Device.Manufacturer
- - SerialNumber
  - Device.SerialNumber
- - ManufacturerModel
  - Device.ModelName
- - SoftwareVersion
  - Device.SoftwareVersion
- - ExecutionEnv
  - Device.SoftwareModules.ExecEnv.{i}.
- - CountryCode
  - Device.WiFi.Radio.{i}.RegulatoryDomain

- []{.object}
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.
  -
- - Enabled
  - Device.WiFi.Radio.{i}.Enable (W)
- - Noise
  - Device.WiFi.Radio.{i}.Stats.Noise
- []{.command}
  - ChannelScanRequest()
  - Device.WiFi.Radio.{i}.ChannelScan() and .FullScan()
- []{.command}
  - RadioEnable()
  - Device.WiFi.Radio.{i}.Enable (W)
- []{.command}
  - WiFiRestart()
  - Device.WiFi.Reset()

- []{.object}
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.ScanResult.{i}.
  - Output of Device.WiFi.Radio.{i}.FullScan() and ChannelScan() are bigger

- []{.object}
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.Capabilities.AKMFrontHaul.{i}.
  -
- - Type
  - Device.WiFi.AccessPoint.{i}.Security.ModesSupported

- []{.object}
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.Capabilities.CapableOperatingClassProfile.{i}.
  -
- - MaxTxPower
  - Device.WiFi.Radio.{i}.TransmitPowerSupported
- - NonOperable
  - Device.WiFi.Radio.{i}.PossibleChannels

- []{.object}
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.CurrentOperatingClassProfile.{i}.
  -
- - Channel
  - Device.WiFi.Radio.{i}.ChannelsInUse
- - TxPower
  - Device.WiFi.Radio.{i}.TransmitPower

- []{.object}
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.DisAllowedOpClassChannels.{i}.
  -
- - ChannelList
  - Device.WiFi.Radio.{i}.Channel

- []{.object}
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.
  -
- - BSSID
  - Device.WiFi.SSID.{i}.BSSID
- - SSID
  - Device.WiFi.SSID.{i}.SSID (W)
- - Enabled
  - Device.WiFi.SSID.{i}.Enable (W)
- - LastChange
  - Device.WiFi.SSID.{i}.LastChange
- - FronthaulAKMsAllowed
  - Device.WiFi.AccessPoint.{i}.Security.ModesSupported, .ModeEnabled (W)

- []{.object}
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.STA.{i}.
  -
- - MACAddress
  - Device.WiFi.AccessPoint.{i}.AssociatedDevice.{i}.MACAddress
- - LastDataDownlinkRate
  - Device.WiFi.AccessPoint.{i}.AssociatedDevice.{i}.LastDataDownlinkRate
- - LastDataUplinkRate
  - Device.WiFi.AccessPoint.{i}.AssociatedDevice.{i}.LastDataUplinkRate
- - SignalStrength
  - Device.WiFi.AccessPoint.{i}.AssociatedDevice.{i}.SignalStrength
- - BytesSent
  - Device.WiFi.AccessPoint.{i}.AssociatedDevice.{i}.Stats.BytesSent
- - BytesReceived
  - Device.WiFi.AccessPoint.{i}.AssociatedDevice.{i}.BytesReceived
- - PacketsSent
  - Device.WiFi.AccessPoint.{i}.AssociatedDevice.{i}.PacketsSent
- - PacketsReceived
  - Device.WiFi.AccessPoint.{i}.AssociatedDevice.{i}.PacketsReceived
- - ErrorsSent
  - Device.WiFi.AccessPoint.{i}.AssociatedDevice.{i}.ErrorsSent
- - ErrorsReceived
  - Device.WiFi.AccessPoint.{i}.AssociatedDevice.{i}.ErrorsReceived
- - RetransCount
  - Device.WiFi.AccessPoint.{i}.AssociatedDevice.{i}.RetransCount

- []{.object}
  - Device.WiFi.DataElements.Network.Device.{i}.MultiAPDevice.
  - (not part of Wi-Fi Data Elements)
- - ManufacturerOUI
  - Device.ManufacturerOUI

- []{.object}
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.STA.{i}.MultiAPSTA.
  -
- - AssociationTime
  - Device.WiFi.AccessPoint.{i}.AssociatedDevice.{i}.AssociationTime
- - Noise
  - Device.WiFi.AccessPoint.{i}.AssociatedDevice.{i}.Noise

- []{.object}
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.MultiAPRadio.
  -
- []{.command}
  - FullScan()
  - Device.WiFi.Radio.{i}.FullScan()
- []{.command}
  - ChannelScan()
  - Device.WiFi.Radio.{i}.ChannelScan()

:::

::: spacer :::
:::

::: {.list-table widths=50,50} :::

Objects and parameters in Wi-Fi Data Elements that correspond to Wi-Fi Native

- []{.object}
  - Wi-Fi Native
  - Wi-Fi Data Elements

- []{.object}
  - Device.WiFi.Radio.{i}.
  -
- - Enable
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.Enabled
- - MaxBitRate
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.Capabilities.CapableOperatingClassProfile.{i}.
- - SupportedFrequencyBands
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.Capabilities.CapableOperatingClassProfile.{i}.
- - OperatingFrequencyBand
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.Capabilities.CurrentOperatingClassProfile
- - SupportedStandards
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.Capabilities.HTCapabilities,
    .VHTCapabilities, .HECapabilities
- - PossibleChannels
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.Capabilities.CapableOperatingClassProfile.{i}.
- - ChannelsInUse
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.Capabilities.CurrentOperatingClassProfile
- - Channel
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.Capabilities.CurrentOperatingClassProfile
- - FirmwareVersion
  - Device.WiFi.DataElements.Network.Device.{i}.SoftwareVersion
- - SupportedOperatingChannelBandwidths
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.Capabilities.CapableOperatingClassProfile.{i}.
- - OperatingChannelBandwidth
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.Capabilities.CurrentOperatingClassProfile
- - CurrentOperatingChannelBandwidth
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.Capabilities.CurrentOperatingClassProfile
- - TransmitPowerSupported
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.Capabilities.CapableOperatingClassProfile.{i}.MaxTxPower
- - TransmitPower
  - Device.WiFi.DataElements.Network.Device.{i}.MultiAPDevice.Backhaul.CurrentOperatingClassProfile.{i}.TxPower
- - RegulatoryDomain
  - Device.WiFi.DataElements.Network.Device.{i}.CountryCode
- []{.command}
  - FullScan()
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.ChannelScanRequest()
- []{.command}
  - ChannelScan()
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.ChannelScanRequest()

- []{.object}
  - Device.WiFi.Radio.{i}.Stats.
  -
- - Noise
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.Noise

- []{.object}
  - Device.WiFi.SSID.{i}.
  -
- - Enable
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.Enabled
- - LastChange
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.LastChange
- - BSSID
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.BSSID
- - SSID
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.SSID

- []{.object}
  - Device.WiFi.AccessPoint.{i}.
  -

- []{.object}
  - Device.WiFi.AccessPoint.{i}.Security.
  -
- - ModesSupported
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.Capabilities.AKMFrontHaul.{i}.
- - ModeEnabled
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.FronthaulAKMsAllowed
- - WEPKey
  - SetSSID(), Input PassPhrase
- - SAEPassphrase
  - SetSSID(), Input PassPhrase

- []{.object}
  - Device.WiFi.AccessPoint.{i}.AssociatedDevice.{i}.
  -
- - MACAddress
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.STA.{i}.MACAddress
- - LastDataDownlinkRate
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.STA.{i}.LastDataDownlinkRate
- - LastDataUplinkRate
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.STA.{i}.LastDataUplinkRate
- - AssociationTime
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.STA.{i}.LastConnectTime
- - SignalStrength
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.STA.{i}.SignalStrength
- - Noise
  - MultiAP: Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.STA.{i}.MultiAPSTA.Noise
- - Retransmissions
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.STA.{i}.RetransCount

- []{.object}
  - Device.WiFi.AccessPoint.{i}.AssociatedDevice.{i}.Stats.
  -
- - BytesSent
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.STA.{i}.BytesSent
- - BytesReceived
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.STA.{i}.BytesReceived
- - PacketsSent
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.STA.{i}.PacketsSent
- - PacketsReceived
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.STA.{i}.PacketsReceived
- - ErrorsSent
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.STA.{i}.ErrorsSent
- - ErrorsReceived
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.STA.{i}.ErrorsReceived
- - RetransCount
  - Device.WiFi.DataElements.Network.Device.{i}.Radio.{i}.BSS.{i}.STA.{i}.RetransCount

:::

## Incorporating Wi-Fi Data Elements into TR-181 {.appendix .same-file}

This section discusses the Theory of Operation for representing the Wi-Fi Alliance (WFA) Data Elements (DE) data model [@DataElements] using the Device.WiFi.DataElements object. The WFA DE specification provides a data model that can be used to represent a single access point or a multi access point network.

### Data Sources for Wi-Fi Data Elements

The DataElements object may be populated by data from any of the following sources:

* IEEE 1905.1 implementation
* WFA DE Agent implementation (for information from the local device, only)
* WFA Multi Access Point Controller implementation
* Network interface card device drivers (for information from the local device, only)
* Application (e.g., a topology database application) that gets data from any of the above sources

Whatever source is used to acquire the data, the data will be represented according to the DE specification [@DataElements].

### Mapping new Wi-Fi Data Elements objects and parameters

The YANG representation of WFA DE is considered the normative reference to use for mapping purposes.

For the initial mapping (included in Release 13), the names of YANG grouping nodes were used for the TR-181 object names, instead of the names of the lists and containers that used these groupings. This was done because the names of the groupings were consistent with TR-181 naming conventions and there was a one-to-one mapping of grouping to a list or a container. For subsequent mapping, the names of containers and lists will be used, and not groupings.

Wi-Fi Data Elements objects and parameters will be added according to the following rules when WFA defines new nodes:

* YANG "container" and "list" nodes will be mapped to TR-181 "object" elements within the DataElements object hierarchy.
    * If the YANG name of the container or list complies with TR-181 naming conventions specified in [@TR-106] section 3.1, the exact name will be used for the TR-181 object name. If the name does not comply, the container or list cannot be automatically added, and an appropriate compliant name will need to be identified.
    * The YANG container or list description can be used "as is" for an automated mapping to the object description, but BBF may modify it slightly for grammar preferences, to include bibliographic references, or to add other useful information when the new object is included in a published revision of TR-181. BBF may also use the grouping description used by the container or list, if this is more descriptive.
    * If the YANG "config true" statement is present, the object will be 'access="readWrite"'. Otherwise, the object will be 'access="readOnly"'.
    * For all multi-instance objects, the TR-181 model will include a parameter named "<object name>NumberOfEntries" of type unsignedInt in the parent object.

* YANG "leaf" nodes will be mapped to TR-181 "parameter" elements within the DataElements. hierarchy.
  * Put under the "object" that corresponds to the YANG container or list
  * If the YANG name of the leaf complies with TR-181 naming conventions specified in [@TR-106] section 3.1, the exact name will be used for the TR-181 parameter name. If the name does not comply, the leaf cannot be automatically added, and an appropriate compliant name will need to be identified.
  * The YANG leaf description can be used "as is" for an automated mapping to the parameter description, but BBF may modify it slightly for grammar preferences, to include bibliographic references, or to add other useful information when the new parameter is included in a published revision of TR-181. Descriptions from DE-custom data type definitions are also mapped into the parameter description.
  * "NumberOf<grouping>" leaf nodes are not mapped. See final bullet of above mapping for containers and lists for inclusion of "<object name>NumberOfEntries" parameter in the TR-181 data model.
  * Data Types are mapped as follows:
    * zero-based-counter32 (and any DE-custom data types based on this, such as bytecounter_t, packetcounter_t) to StatsCounter64  [Note that the TR-181 convention is to use StatsCounter64 for all counters.]
    * uint8 (and any DE-custom data types based on this, such as rssi_t, noisepower_t, operatingclass_t, channel_t, utilization_t) to unsignedInt with range indicated by minInclusive and maxInclusive, if identified
    * uint16 (and any DE-custom data types based on this, such as reasoncode_t, statuscode_t, vlanid_t, pcp_t) to unsignedInt with range indicated by minInclusive and maxInclusive, if identified
    * uint32 to unsignedInt with range indicated by minInclusive and maxInclusive, if identified
    * gauge32 (and any DE-custom data types based on this, such as phyrate_t, macrate_t) to unsignedInt
    * int8 (and any DE-custom data types based on this, such as txpower_t) to int with ranges, if identified (e.g., int[-127:127] for txpower_t)
    * string to string with length indicated by maxLength, if identified
    * mac-address to MACAddress
    * binary to base64
    * boolean to boolean
    * ipv4-address to IPv4Address
    * ipv6-address to IPv6Address
    * additional mappings for data types not listed may be defined by WFA or BBF

* YANG "leaf-list" nodes are mapped like "leaf" elements for name and description with syntax of "<list/>". The data type is mapped as described above for leaf nodes.
