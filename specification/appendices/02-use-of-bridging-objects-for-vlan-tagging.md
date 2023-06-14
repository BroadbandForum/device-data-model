# Use of Bridging Objects for VLAN Tagging {.appendix .same-file}

In the case of an Ethernet upstream Interface or a VDSL2 upstream Interface based on PTM-EFM, 802.1Q Tagging can be used to tag egress traffic. This choice enables a multi-VLAN architecture in order to deploy a multi-service configuration (high speed Internet, VoIP, Video Phone, IPTV, etc.), where one VLAN or a group of VLANs are associated with each service. If 802.1Q tagging on the upstream interface is used, it is necessary to have a way to associate incoming upstream 802.1Q tagged or untagged traffic or internally generated traffic (PPPoE, IPoE connections) to the egress (and vice-versa). The solution is to apply coherent bridging rules.

Regarding different traffic bridging rules, the possible cases are characterized as follows:

* Tagged LAN to tagged WAN traffic (pure VLAN bridging), with VLAN ID translation as a special case
* Untagged LAN to tagged WAN traffic
* Internally generated to tagged WAN traffic

To better understand the different cases, refer to @fig:examples-of-vlan-configuration-based-on-bridging-and-vlan-termination-objects and to the following examples.

![Examples of VLAN configuration based on Bridging and VLAN Termination objects](/images/examples-of-vlan-configuration-based-on-bridging-and-vlan-termination-objects.png)

## Tagged LAN to Tagged WAN Traffic (VLAN Bridging)

Ethernet port 1 (instance Device.Ethernet.Interface.2) might be dedicated to VoIP service, receiving VLAN ID x tagged traffic from a VoIP phone, and this port would be included in the same bridge dedicated to VoIP service on the upstream interface (instance Device.Ethernet.Interface.1), identified with the same VLAN ID x.

To achieve this, an interface-based bridge would be created using the Bridging object. A Bridge table entry would be created with entries for Ethernet port 1 and the upstream interface and for the VLAN ID x associated with VoIP.

The Bridging model is depicted in @fig:bridge-1-model, while the configuration rules for this situation are summarized in @tbl:tagged-lan-to-tagged-wan-configuration.

![Bridge 1 model](/images/bridge-1-model.png)

---
bridge1ModelTableSpec:
  caption: Tagged LAN to tagged WAN configuration
  headers:
    - Description
    - Bridging Configuration!!!!!!!!
  labels:
    - descr
    - config

bridge1ModelTable:
  - descr: |
      Bridge between WAN and LAN 1 interfaces with VLANID=*x*

    config: |
      [Define VLANx]

      | Device.Bridging.Bridge.1.VLAN.1     |
      |-------------------------------------|-----------------------------------
      | Name                                | *VLANx*
      | VLANID                              | *X*

      [Define Ingress Port2-3 -- Create an entry for the upstream and
      downstream port]

      | Device.Bridging.Bridge.1.Port.2     |
      |-------------------------------------|------------------------------------
      | PVID                                | *x*
      | Name                                | *Port2*
      | AcceptableFrameTypes                | AdmitOnlyVLANTagged

      | Device.Bridging.Bridge.1.Port.3     |
      |-------------------------------------|------------------------------------
      | PVID                                | *x*
      | Name                                | *Port3*
      | AcceptableFrameTypes                | AdmitOnlyVLANTagged

      [Associate Egress Port2-3 to VLANx -- Create an entry for the upstream
      and downstream port]

      | Device.Bridging.Bridge.1.VLANPort.1 |
      |-------------------------------------|------------------------------------
      | VLAN                                | *VLANx*
      | Port                                | *Port2*
      | Untagged                            | *false*

      | Device.Bridging.Bridge.1.VLANPort.2 |
      |-------------------------------------|------------------------------------
      | VLAN                                | *VLANx*
      | Port                                | *Port3*
      | Untagged                            | *false*
...

::: {bbfTable=bridge1ModelTable}
:::

## Tagged LAN to Tagged WAN Traffic (Special Case with VLAN ID Translation)

Ethernet port 2 (instance Device.Ethernet.Interface.3) might be dedicated to Video Phone service, receiving VLAN ID y tagged traffic from a Video phone, and this port would be included in the same bridge dedicated to Video Phone service on the upstream interface (instance Device.Ethernet.Interface.1), identified by a different VLAN ID (VLAN ID z). In this case a VLAN translation needs to be performed.

To achieve this, a bridge would be created using the Bridging object. A Bridge table entry would be created along with two associated Filter object entries for {Ethernet port 2/VLAN ID z} and {upstream interface/VLAN ID y}. The Filter identifies the ingress interface and causes the ingress frames to be bridged to the egress VLAN, permitting VLAN-ID translation.

The Bridging model is depicted in @fig:bridge-2-model, while the configuration rules for this situation are summarized in @tbl:tagged-lan-to-tagged-wan-configuration-vlan-id-translation.

![Bridge 2 model](/images/bridge-2-model.png)

---
bridge2ModelTableSpec:
  caption: Tagged LAN to tagged WAN configuration (VLAN ID translation)
  headers:
    - Description
    - Bridging Configuration!!!!!!!!
  labels:
    - descr
    - config

bridge2ModelTable:
  - descr: |
      Tagged LAN 2 to tagged WAN traffic (and vice versa) (special case with VLAN ID translation)

      upstream VLAN-ID=z

      downstream VLAN-ID=y

    config: |
      [Define VLANy and VLANz]

      | Device.Bridging.Bridge.2.VLAN.1     |
      |-------------------------------------|------------------------------------
      | Name                                | *VLANy*
      | VLANID                              | *y*

      | Device.Bridging.Bridge.2.VLAN.2     |
      |-------------------------------------|------------------------------------
      | Name                                | *VLANz*
      | VLANID                              | *z*

      [Define Ingress Port2 -- Create an entry for upstream port]

      | Device.Bridging.Bridge.2.Port.2     |
      |-------------------------------------|------------------------------------
      | PVID                                | *Z*
      | Name                                | *Port2*
      | AcceptableFrameTypes                | AdmitOnlyVLANTagged

      [Define Ingress Port3 -- Create an entry for the downstream port]

      | Device.Bridging.Bridge.2.Port.3     |
      |-------------------------------------|------------------------------------
      | PVID                                | *y*
      | Name                                | *Port3*
      | AcceptableFrameTypes                | AdmitOnlyVLANTagged

      [Associate Egress Port2 to VLANz - Create an entry for upstream port]

      | Device.Bridging.Bridge.2.VLANPort.1 |
      |-------------------------------------|------------------------------------
      | VLAN                                | *VLANz*
      | Port                                | *Port2*
      | Untagged                            | *false*

      [Associate Egress Port3 to VLANy - Create an entry for each downstream port]

      | Device.Bridging.Bridge.2.VLANPort.2 |
      |-------------------------------------|------------------------------------
      | VLAN                                | *VLANy*
      | Port                                | *Port3*
      | Untagged                            | *false*

      [Define filter on upstream: ingress from Port 2 is associated with VLANy]

      | Device.Bridging.Filter.1.           |
      |-------------------------------------|------------------------------------
      | Bridge                              | *VLANy*
      | Interface                           | *Port2*

      [Define filter on downstream: ingress from Port 3 is associated with VLANz]

      | Device.Bridging.Filter.2.           |
      |-------------------------------------|------------------------------------
      | Bridge                              | *VLANz*
      | Interface                           | *Port3*
...

::: {bbfTable=bridge2ModelTable}
:::

## Untagged LAN to Tagged WAN Traffic

Ethernet port 3 (instance Device.Ethernet.Interface.4) might be dedicated to IPTV service, receiving untagged traffic from a STB, and this port would be included in the same bridge dedicated to IPTV service on the upstream interface (instance Device.Ethernet.Interface.1), identified with the VLAN ID k.

To achieve this, an interface-based bridge would be created using the Bridging object. A Bridge table entry would be created, associating in the same bridge untagged frames on Ethernet port 3 with tagged frames on the upstream interface.

The Bridging model is depicted in @fig:bridge-3-model, while the configuration rules for this situation are summarized in @tbl:untagged-lan-to-tagged-wan-configuration.

![Bridge 3 model](/images/bridge-3-model.png)

---
bridge3ModelTableSpec:
  caption: Untagged LAN to tagged WAN configuration
  headers:
    - Description
    - Bridging Configuration!!!!!!!!
  labels:
    - descr
    - config

bridge3ModelTable:
  - descr: |
      Untagged LAN 3 to tagged WAN (VLAN-ID=k) traffic

    config: |
      [Define VLANk]

      | Device.Bridging.Bridge.3.VLAN.1     |
      |-------------------------------------|------------------------------------
      | Name                                | *VLANk*
      | VLANID                              | *k*

      [Define Ingress Port2 -- Create an entry for upstream port]

      | Device.Bridging.Bridge.3.Port.2     |
      |-------------------------------------|------------------------------------
      | PVID                                | *k*
      | Name                                | *Port2*
      | AcceptableFrameTypes                | AdmitOnlyVLANTagged

      [Define Ingress Port3 -- Create an entry for the downstream port]

      | Device.Bridging.Bridge.3.Port.3     |
      |-------------------------------------|------------------------------------
      | Name                                | *Port3*
      | AcceptableFrameTypes                | AdmitAll

      [Associate Egress Port2 to VLANk - Create an entry for upstream port]

      | Device.Bridging.Bridge.3.VLANPort.1 |
      |-------------------------------------|------------------------------------
      | VLAN                                | *VLANk*
      | Port                                | *Port2*
      | Untagged                            | *false*

      [Associate Egress Port3 to VLANk - Create an entry for each downstream port]

      | Device.Bridging.Bridge.3.VLANPort.2 |
      |-------------------------------------|------------------------------------
      | VLAN                                | *VLANk*
      | Port                                | *Port3*
      | Untagged                            | *true*
...

::: {bbfTable=bridge3ModelTable}
:::

## Internally Generated to Tagged WAN Traffic

A CPE PPPoE internal session (instance Device.PPP.Interface.1) might be dedicated to Management service and this logical interface would encapsulate/de-encapsulate its outgoing or incoming traffic in the VLAN ID j, dedicated to Management service.

To achieve this, instead of using a bridging object, a VLAN Termination interface would be created (Device.Ethernet.VLANTermination.1). The Bridging model is depicted in @fig:vlan-termination-model, while the configuration rules for this situation are summarized in @tbl:internally-generated-to-tagged-wan-configuration.

![VLAN Termination model](/images/vlan-termination-model.png)

---
vlanTerminationModelTableSpec:
  caption: Internally generated to tagged WAN configuration
  headers:
    - Description
    - Bridging Configuration!!!!!!!!
  labels:
    - descr
    - config

vlanTerminationModelTable:
  - descr: |
      Internal to tagged WAN (VLAN-ID=j) traffic

    config: |
      [DefineVLAN Termination on top of Ethernet Link]

      | Device.Ethernet.VLANTermination.1  |
      |------------------------------------|-------------------------------------
      | VLANID                             | *j*
      | LowerLayers                        | Ethernet.Link.1
...

::: {bbfTable=vlanTerminationModelTable}
:::

## Other Issues

The previous rules can be applied to allow all combinations of traffic. If the subscriber's services are modified, the Bridging configuration might need to be modified accordingly.

It can be interesting to detail the configuration of three special cases:

* More than one downstream interface in a bridge
* 802.1D (re-)marking
* More than one VLAN ID tag for the same downstream interface

### More than one Downstream Interface in a Bridge

Referring to the example in *[Tagged LAN to tagged WAN traffic (VLAN bridging)]*, consider adding other Ethernet interfaces (e.g., Ethernet ports 3 and 4 = instance Device.Ethernet.Interface.3/4) to the Video Phone service. The behavior is the same as for the existing Ethernet port 2 (instance Device.Ethernet.Interface.2).

To achieve this, new entries need to be added for interface Eth-3 and Eth-4. The Bridging model is depicted in @fig:bridge-1-model-additional-ethernet-interfaces, while the configuration rules for this situation are summarized in @tbl:tagged-lan-to-tagged-wan-configuration and @tbl:configuration-to-be-added-to-tagged-lan-to-tagged-wan-configuration-table.

![Bridge 1 model (additional Ethernet interfaces)](/images/bridge-1-model-additional-ethernet-interfaces.png)

---
bridge1ModelPlusTableSpec:
  caption: Configuration to be added to "Tagged LAN to tagged WAN configuration" table
  headers:
    - Description
    - Bridging Configuration!!!!!!!!
  labels:
    - descr
    - config

bridge1ModelPlusTable:
  - descr: |
      Bridge between WAN and LAN 2/LAN 3 interfaces with VLANID=*x*
      *(Configuration to be added to @tbl:tagged-lan-to-tagged-wan-configuration)*

    config: |
      [Define Ingress Port4-5 -- Create an entry for the other downstream ports]

      | Device.Bridging.Bridge.1.Port.4     |
      |-------------------------------------|------------------------------------
      | PVID                                | *x*
      | Name                                | *Port4*
      | AcceptableFrameTypes                | AdmitOnlyVLANTagged

      | Device.Bridging.Bridge.1.Port.5     |
      |-------------------------------------|------------------------------------
      | PVID                                | *x*
      | Name                                | *Port5*
      | AcceptableFrameTypes                | AdmitOnlyVLANTagged

      [Associate Egress Port4-5 to VLANx - Create an entry for the downstream ports]

      | Device.Bridging.Bridge.1.VLANPort.3 |
      |-------------------------------------|------------------------------------
      | VLAN                                | *VLANx*
      | Port                                | *Port4*
      | Untagged                            | *false*

      | Device.Bridging.Bridge.1.VLANPort.4 |
      |-------------------------------------|------------------------------------
      | VLAN                                | *VLANx*
      | Port                                | *Port5*
      | Untagged                            | *false*
...

::: {bbfTable=bridge1ModelPlusTable}
:::

### 802.1D (Re)-marking {#sec:802.1d-re-marking}

The 802.1Q Tag includes the 802.1D user priority bits field. All the previous cases can also be extended to mark (or re-mark) this 802.1D field. To achieve this, there are different configuration options; one of them is to use the DefaultUserPriority or PriorityRegeneration fields in the Bridge Port object. For untagged frames, more complex rules can be defined referring to the QoS Classification, using the PriorityTagging value. The Bridging configuration rules for marking egress traffic on the upstream interface are summarized in @tbl:802.1d-re-marking]. Compare it with @tbl:tagged-lan-to-tagged-wan-configuration.

---
bridgeRemarkingTableSpec:
  caption: 802.1D (re-)marking
  headers:
    - Description
    - Bridging Configuration!!!!!!!!
  labels:
    - descr
    - config

bridgeRemarkingTable:
  - descr: |
      802.1D (re-)marking

      Remark all WAN egress traffic

    config: |
      [Mark the ingress frames with Default user Priority, in this case *0*]

      | Device.Bridging.Bridge.1.Port.2.   |
      |------------------------------------|-------------------------------------
      | DefaultUserPriority                | *0*

      [Remark each ingress priority value (0,1,2,3,4,5,6,7) with the priority
      regeneration string, in this case *(0,0,0,0,4,4,4,4)*]

      | Device.Bridging.Bridge.1.Port.2.   |
      |------------------------------------|-------------------------------------
      | PriorityRegeneration               | *0,0,0,0,4,4,4,4*

      [In case of ingress untagged frames, for more complex classification, QoS
      object are referred. In this case remark with *0*]

      | Device.Bridging.Bridge.1.Port.2.   |
      |------------------------------------|-------------------------------------
      | PriorityTagging                    | *true*

      | Device.QoS.Classification.{i}.     |
      |------------------------------------|-------------------------------------
      | EthernetPriorityMark               | *0*
...

::: {bbfTable=bridgeRemarkingTable}
:::

### More than one VLAN ID Tag Admitted on the Same Downstream Interface

Another scenario that can be further detailed is the case of more than one VLAN ID tag admitted on the same downstream interface. A practical example would be a 2 box scenario, with a User Device generating traffic segregated in multiple VLANs (e.g., a router offering services to the customer), and a Residential Gateway, providing upstream connectivity to the Access Network, with the connection between the two pieces of equipment using an Ethernet interface.

In this case, we assume the User Device is able to tag the different traffic flows, segregating the different services (Voice, Video, ...) into different VLANs. The Residential Gateway needs, on the same downstream interface, to be able to receive different VLAN ID and correctly forward or translate to the upstream interface (and vice versa). To achieve this, appropriate Bridging objects need to be configured.

![Example of VLAN configuration in a 2 box scenario](/images/example-of-vlan-configuration-in-a-2-box-scenario.png)

Referring to @fig:example-of-vlan-configuration-in-a-2-box-scenario as an example, assume the case of three VLANs (VLAN ID=x,y,z) offered by a User Device to the Residential Gateway on the same downstream interface (Eth #1). The Residential Gateway bridges two of them (VLAN ID=x,y) and translates the other one (VLAN ID=z) to the upstream interface (VLAN ID=k).

On the Residential Gateway, this can be achieved using a combination of the Bridging objects detailed in the preceding sections, with 3 bridge entries and their related entries. Refer to @fig:bridge-123-model for the Bridging model and @tbl:more-than-one-vlan-id-tag-admitted-on-the-same-downstream-interface for the global configuration.

![Bridge 1,2,3 model](/images/bridge-123-model.png)

---
bridge123ModelTableSpec:
  caption: More than one VLAN ID tag admitted on the same Downstream interface
  headers:
    - Description
    - Bridging Configuration!!!!!!!!
  labels:
    - descr
    - config

bridge123ModelTable:
  - descr: |
      More than one VLAN ID tag admitted on the same downstream interface

    config: |
      The configuration is the sum of *[Tagged LAN to Tagged
      WAN Traffic VLAN Bridging]* and *[Tagged LAN to Tagged WAN Traffic
      Special Case with VLAN ID Translation]*, but on the downstream side the
      lower layer to be configured for each Bridge Port is always:
      Ethernet.Interface.2

      | Device.Bridging.Bridge.1.Port.3.   |
      |------------------------------------|-------------------------------------
      | LowerLayers                        | *Ethernet.Interface.2*

      | Device.Bridging.Bridge.2.Port.3.   |
      |------------------------------------|-------------------------------------
      | LowerLayers                        | *Ethernet.Interface.2*

      | Device.Bridging.Bridge.3.Port.3.   |
      |------------------------------------|-------------------------------------
      | LowerLayers                        | *Ethernet.Interface.2*
...

::: {bbfTable=bridge123ModelTable}
:::

