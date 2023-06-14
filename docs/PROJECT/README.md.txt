<!-- do not edit! this file was created from PROJECT.yaml by project-parser.py -->

# TR-181: Device Data Model for CWMP Endpoints and USP Agents

*TR-181 Documentation and Theory of Operations*

See <https://device-data-model.broadband-forum.org> for the
current TR-181 specification.

TR-181 Issue 2 defines version 2 of the Device data model (Device:2). The
Device:2 data model applies to all types of TR-069 or USP enabled devices,
including End Devices, Residential Gateways, and other Network Infrastructure
Devices.

The Device:2 data model defined in this Technical Report consists of a set of
data objects covering things like basic device information, time-of-day configuration,
network interface and protocol stack configuration, routing and bridging management,
throughput statistics, and diagnostic tests. It also defines a baseline profile that
specifies a minimum level of data model support.

The cornerstone of the Device:2 data model is the interface stacking mechanism. Network
interfaces and protocol layers are modeled as independent data objects that can be stacked,
one on top of the other, into whatever configuration a device might support.
