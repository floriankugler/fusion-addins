# BendPositionTypes Enumerator

## Description

Bend location types used for creating flanges and hems.  

## Methods

| Name | Value | Description |
|----|----|----|
| InsideBendPositionType | 2 | Reference Plane through other Edge, Material inside |
| LegacyBendPositionType | 0 | Legacy bend location type no longer used. Not tangent to side, same reference plane as eBendInnerVS, but material can flip. |
| OutsideBendPositionType | 1 | Reference Plane through selected Edge, Material outside |
| StartEdgeBendPositionType | 3 | Reference Plane is the Side Face, Bend starts at selected edge |
| TangentToSideBendPositionType | 4 | Reference Plane is the Side Face, Bend Tangent to Ref Plane if angle >= 90 |

## Version

Introduced in version September 2025  

