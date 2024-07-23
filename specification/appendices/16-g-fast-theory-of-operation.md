# G.fast Theory of Operation {.appendix .same-file}

G.fast (hereafter referred to as FAST) is a DSL communications technology defined by ITU-T G.9700, G.9701, and G.997.2.

Devices that support both DSL and FAST (both interfaces' objects are administratively Enabled) have the capability to switch from one mode to another. If the device is connected in xDSL mode (DSL.Line.{i}.status is "Up"), FAST interface is down (FAST.Line.{i}.status is "Not Present" or "Down"). The InterfaceStack Table needs to reflect the relationship between the PTM interface and DSL interface as seen in @fig:ptm-link-for-dsl-mode-line. The PTM's LowerLayers points to DSL.Channel instance whose status is "Up".

![PTM Link for DSL mode Line](/images/ptm-link-for-dsl-mode-line.png){typst-scale=0.4}

In the case when the device is connected in FAST mode, the DSL line is down. The InterfaceStack Table needs to show that the PTM's LowerLayers points to the FAST.Line interface as below:

![PTM Link for FAST mode Line](/images/ptm-link-for-fast-mode-line.png){typst-scale=0.4}

The same fall back mechanism applies to the bonding of FAST and DSL interfaces. PTM's interface is to be stacked on two bonding groups as they are both administrative "Enable". However, in the InterfaceStack Table, the PTM interface's LowerLayers points to the bonding group that has Operational Status "Up". In the diagram below, PTM's LowerLayers points to the bonding group of FAST.Line, which is currently "Up". The DSL bonding group instance corresponding to DSL channels is "Down".

![PTM Link Bonding Groups for FAST mode Lines](/images/ptm-link-bonding-groups-for-fast-mode-lines.png){typst-scale=0.4}

In the case where DSL Bonding group is "Up" for non-FAST mode lines, the diagram below shows PTM's LowerLayers pointing to the bonding group of DSL.Channel, which is currently "Up". The DSL bonding group instance corresponding to FAST Lines is "Down" here.

![PTM Link Bonding Groups for DSL mode Lines](/images/ptm-link-bonding-groups-for-dsl-mode-lines.png){typst-scale=0.4}
