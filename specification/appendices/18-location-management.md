# Location Management {.appendix .same-file}

This section discusses the Theory of Operation for Location Management using CWMP [@TR-069] or USP [@TR-369] and the Location object defined in the <rootobject>.DeviceInfo data model.

## Overview

The Location object defined in this document is a multi-instance object that can be used by any device that needs to be able to acquire and/or express its "location."

This Location object is a multi instance object to account for the fact that a Device can acquire location information in more than one way. Location info can be acquired by:

* GPS/A-GPS, i.e., provided by specific on-board circuitry such as GPS or A-GPS;
* Manual, i.e., manually configured via the Device local GUI
* External, i.e., remotely configured via a number of protocols, including e.g., TR-069

Location objects can be created autonomously by the device, based on the location information it receives by CWMP or USP. When the Location object is created autonomously by the device, the device itself will fill the DataObject parameter with location data coming from GPS/AGPS, local GUI or an external protocol (not CWMP). When created by CWMP or USP, it is up to the CWMP or USP protocol to configure the DataObject parameter. Regardless of how a Location object is created, the device is responsible for populating the values of all of the location metadata (i.e., all parameters except the DataObject that contains the location information and the AcquiredTime) not writable by any external mechanism.

When a Location object is updated, the object can only be updated through the same mechanism that created it. The device will update the AcquiredTime as necessary and place the updated location data in the DataObject.

When a Location object is deleted, the object can only be deleted through the same mechanism that created it.

## Multiple Instances of Location Data

Devices that need to make use of location data will need to have rules around how to deal with multiple instances of location data. These rules are out of scope for CWMP or USP and the Device:2 data model. These rules may need to be specific to a particular application. For example, if a VoIP device chooses to send location data in a SIP message, the device can include all of the instances of DataObject in that message, order the Locations Objects according to the acquisition date and time (parameter AcquiredDateTime, most recent is first) or order the Location objects according to some sort of protocol preference, such as GPS, A-GPS, DHCP, HELD, CWMP, USP, and then all others according to acquisition date and time.

A Femtocell Access Point (FAP) with multiple sources of location can also need rules for use of the Location object. If it must make decisions locally based on location, the FAP will need rules to determine the preferred location. If the FAP must send its location elsewhere, the FAP will need rules to determine whether the FAP sends all of its location data, or selects certain locations based on specific criteria.

## CWMP, USP, Manual, GPS, and AGPS Configured Location

As noted in the description of the Device:2 data model parameter <rootObject>.Location.{i}.DataObject., Manual, GPS, and AGPS mechanisms are formatted by the device according to the following formats specified by the IETF. A Controller that is creating an External:CWMP or an External:USP location will use one of these formats:

#. Geographical coordinates formatted according to the XML syntax specified in IETF RFC 5491 [@RFC5491] (update of RFC 4119 [@RFC4119])

#. Civic addresses according to the XML syntax specified in IETF RFC 5139 [@RFC5139] (update of RFC 4119 [@RFC4119])

Location information in these IETF RFCs is specified within the IETF framework of presence information. While these IETF RFCs specify presence information different from the Location component model assumed in the TR-069 framework, the IETF data format is adopted by BBF independent of these higher level differences.

IETF defines its XML syntax for geographical information as a subset of presence information (<presence> object in the XML example below), generally related to a device (<device> object) or a user (<user> object). IETF location information is represented using a Presence Information Data Format Location Object (PIDF-LO). This is represented as the <geopriv> object in the XML example below.

### Example: Manual, GPS, AGPS, and External:CWMP <rootObject>.Location.{i}.DataObject. Format

This example, modified from an example in RFC5491, explains how to format location information in a <rootObject>.Location.{i}.DataObject. parameter with both geographical coordinates and civic location information according to the above-referenced IETF RFCs. The schema associated with the civic location namespace "urn:ietf:params:xml:ns:pidf:geopriv10:civicAddr" is specified in RFC 5139 [@RFC5139].

    <presence xmlns="urn:ietf:params:xml:ns:pidf"
              xmlns:dm="urn:ietf:params:xml:ns:pidf:data-model"
              xmlns:gp="urn:ietf:params:xml:ns:pidf:geopriv10"
              xmlns:gml="http://www.opengis.net/gml"
              xmlns:cl="urn:ietf:params:xml:ns:pidf:geopriv10:civicAddr"
              entity=" ">
        <dm:device id=" FFFFFF-FAP-123456789 ">
            <gp:geopriv>
                <gp:location-info>
                    <gml:Point srsName="urn:ogc:def:crs:EPSG::4326">
                        <gml:pos>-43.5723 153.21760</gml:pos>
                    </gml:Point>
                    <cl:civicAddress>
                        <cl:FLR>2</cl:FLR>
                    </cl:civicAddress>
                </gp:location-info>
                <gp:usage-rules/>
                <gp:method>Wiremap</gp:method>
            </gp:geopriv>
            <dm:deviceID>mac:8asd7d7d70</dm:deviceID>
            <dm:timestamp>2007-06-22T20:57:29Z</dm:timestamp>
        </dm:device>
    </presence>

### RFC 5491 and RFC 5139 Location Element Definitions

The XML elements are defined as follows by the IETF in RFC 5491 [@RFC5491] and related documents:

#.  <presence> (RFC 5491 [@RFC5491])

    The <presence> element MUST have an 'entity' attribute. The value of the 'entity' attribute is the 'pres' URL of the presentity publishing this presence document.

    The <presence> element MUST contain a namespace declaration ('xmlns') to indicate the namespace on which the presence document is based. The presence document compliant to this specification MUST have the namespace 'urn:ietf:params:xml:ns:pidf:'. It MAY contain other namespace declarations for the extensions used in the presence XML document.

#.  <device> (RFC 5491 [@RFC5491])

    The <device> element [...] can appear as a child to <presence>. There can be zero or more occurrences of this element per document. Each <device> element has a mandatory "id" attribute, which contains the occurrence identifier for the device. In the TR-069 framework the id attribute will contain the CWMP Identifier of the device, in the form OUI-ProductClass-SerialNumber.

#.  <geopriv> (RFC 5491 [@RFC5491], RFC 5139 [@RFC5139])

    Location information in a PIDF-LO can be described in a geospatial manner based on a subset of Geography Markup Language (GML) 3.1.1 or as civic location information specified in  RFC 5139 [@RFC5139]. The PIDF-LO Geodetic Shapes specification provides a specific GML profile for expressing commonly used shapes using simple GML representations. This profile defines eight shape types, the simplest ones being a 2-D and a 3-D Point. The  PIDF-LO Geodetic Shapes specification also mandates the use of the World Geodetic System 1984 (WGS84) coordinate reference system and the usage of European Petroleum Survey Group (EPSG) code 4326 (as identified by the URN urn:ogc:def:crs:EPSG::4326) for two-dimensional (2d) shape representations and EPSG 4979 (as identified by the URN urn:ogc:def:crs:EPSG::4979) for three-dimensional (3d) volume representations.

    Each <geopriv> element must contain at least the following two child elements: <location-info> element and <usage-rules> element. One or more elements containing location information are contained inside a <location-info> element.

    #. <location-info> element can contain one or more elements bearing location information.
        #. <Point> element contains geographical data in the coordinate system specified by its srsName attribute. In the example above (WGS84/EPSG 4326), the syntax is latitude, longitude expressed in degrees
        #. Civic information elements are specified by IETF and can be added to the geographical data, though mixing information is not recommended.
        #. <relative-location> element is being proposed by IETF

    #. <usage-rules> can contain the following optional elements:
        #. <retransmission-allowed>: When the value of this element is 'no', the recipient of this Location Object is not permitted to share the enclosed Location Information, or the object as a whole, with other parties. RFC 4119 [@RFC4119] specifies that "by default, the value MUST be assumed to be 'no'".
        #. <retention expires>: This field specifies an absolute date at which time the Recipient is no longer permitted to possess the location information
        #. <external ruleset>: This field contains a URI that indicates where a fuller ruleset of policies, related to this object, can be found
        #. <notewell>: This field contains a block of text containing further generic privacy directives.

    #. <method> is an optional element that describes the way that the location information was derived or discovered. Values allowed by RFC 4119 [@RFC4119] are stored in the IANA registry as "Method Tokens" [@IANA-Method-Tokens]. The "Wiremap" value listed in the example is described as "Location determined using wiremap correlations to circuit identifiers "

#. <deviceID> element is mandatory. It contains a globally unique identifier, in the form of a URN, for each of the presentity devices (RFC 4479 [@RFC4479])

#. <timestamp> is optional (RFC 4479 [@RFC4479])

### Use of RFC 5491 and RFC 5139 Location XML Elements in CWMP or USP

#. <presence>\
The entity attribute conveys no useful information and its value should be conventionally set to an empty string.

#. <device>\
In RFC 5491 [@RFC5491] this is one of the devices associated to the presentity. Devices are identified in the presence document by means of an instance identifier specified in the id attribute.

#. <geopriv>
    #. <location-info>\
    2-D geographical coordinates with no additional civic information are sufficient in the simplest case.
        * <Point>\
        For 2-D applications the value of the srsName attribute should be set to the specified value "urn:ogc:def:crs:EPSG::4326"
    #. <usage-rules>
        * <retransmission-allowed>\
        Note that this field is not intended as instruction to the device whose location this is. Rather, it is intended to provide instruction to other systems that the device sends its location to (via SIP or other mechanisms). Therefore, the device will need to maintain its own policy (no standardized TR-069 data model is provided for this) as to when and where to send its location to others, and how to set this parameter when transmitting this location information. The device can choose to set this parameter to "yes" or to "no" when sending its location to others. RFC 4119 [@RFC4119] specifies that this element's default value is "no".
    #. <method>\
    If this location object is being created by the device as a result of GPS, A-GPS, or Manual mechanisms, the <method> parameter will be populated with "GPS", "A-GPS", or "Manual", respectively. If the location object is being created by External:CWMP, then this parameter will not be used or populated by the Controller.

#. <deviceID> It contains a globally unique identifier, in the form of a URN, for each of the presentity devices (RFC 4479 [@RFC4479]).

#. <timestamp> is optional. The device (GPS, A-GPS, Manual), ACS (External:CWMP) or USP-Controller (External:USP) can set this to the time the location was set or acquired.

