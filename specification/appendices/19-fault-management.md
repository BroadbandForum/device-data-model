# Fault Management {.appendix .same-file}

This section discusses the Theory of Operation for Fault Management using CWMP [@TR-069] or USP [@TR-369] and the FaultMgmt object defined in the Root data model.

## Overview

There are four types of alarm event handling:

|                 |
|-----------------|--------------------------------------------------------------
| Expedited Event | Alarm event is immediately notified to the Controller with the use of Active Notification mechanism
| Queued Event    | Alarm event is notified to the Controller at the next opportunity with the use of Passive Notification mechanism
| Logged Event    | The CPE stores the alarm event locally but does not notify the Controller
| Disabled Event  | The CPE ignores the alarm event and takes no action

Note that all Fault Management tables are cleared when the device reboots.

@tbl:fm-object-definition shows the multi-instance objects for FM to manage the alarm events.

:FM Object Definition

| Object name (*<rootobject>.FaultMgmt.*) | Table size | Content        | Purpose and usage
|-----------------------|-----------|----------------|--------------------------------------------------------------
| SupportedAlarm.{i}.   | Fixed     | Static & fixed content | Defines all alarms that the CPE supports. *ReportedMechanism* defines how the alarm is to be handled within the CPE: *0 -- Expedited, 1 -- Queued, 2 -- Logged, 3 -- Disabled*\
\
The table size is fixed and its content is static in order to drive the alarm handling behavior in the CPE.
| ExpeditedEvent.{i}.   | Fixed     | Dynamically updated | Contains all *"Expedited"* type alarm events since the last device initialization. This includes events that are already reported or not yet reported to the Controller. One entry exists for each event. In other words, raising and clearing of the same alarm are two separate entries. As the table size is fixed (vendor defined), new alarm event overwrites the oldest entry in FIFO fashion after the table becomes full.
| QueuedEvent.{i}.      | Fixed     | Dynamically updated | Contains all *"Queued"* type alarm events since the last device initialization. This includes events that are already reported or not yet reported to the Controller. One entry exists for each event. In other words, raising and clearing of the same alarm are two separate entries.\
\
As the table size is fixed (vendor defined), new alarm event overwrites the oldest entry in FIFO fashion after the table becomes full.
| CurrentAlarm.{i}.     | Variable  | Dynamically updated | Contains all the currently active alarms (i.e., outstanding alarms that are not yet cleared) since the last device initialization. When an outstanding alarm is cleared, that entry is deleted from this table. Therefore, only 1 entry exists for a given unique alarm.\
\
A Controller can retrieve the content of this table to get the entire view of the currently outstanding alarms.\
\
As this is a variable size table, the size changes as alarm event is raised and cleared.\
\
If maximum entries for this table are reached, the next event overrides the object with instance number 1. Subsequent entries override objects at sequentially increasing instance numbers. This logic provides for automatic "rolling" of records.\
\
When a new alarm replaces an existing alarm, then all parameter values for that instance are considered as changed for the purposes of value change notifications to the Controller (even if their new values are identical to those of the prior alarm).
| HistoryEvent.{i}.     | Fixed     | Dynamically updated | Contains all alarm events as a historical record keeping purpose. One entry exists for each event. In other words, raising and clearing of the same alarm are two separate entries.\
\
The Controller can retrieve the content of this table to get the entire chronological history of the alarm events on the CPE.\
\
As the table size is fixed (vendor defined), new alarm event overwrites the oldest entry in FIFO fashion after the table becomes full.

