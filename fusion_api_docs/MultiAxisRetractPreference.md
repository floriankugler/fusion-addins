# MultiAxisRetractPreference Enumerator

## Description

Enumeration of the multi-axis retract preferences that can be used in MultiAxisRetractAndReconfigureSettings.  

## Methods

| Name | Value | Description |
|----|----|----|
| MultiAxisRetractPreference_RetractAtApex | 0 | Always retract when repositioning rotary axes. |
| MultiAxisRetractPreference_StayAtApex | 1 | Allows the tool to stay down without retracting when the rotary axes are repositioned. The tool must be perpendicular to the rotary axis rotational vector (so that only one rotary axis will move) and TCP must be enabled for this axis. |

## Version

Introduced in version September 2025  

