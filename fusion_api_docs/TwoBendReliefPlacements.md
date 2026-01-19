# TwoBendReliefPlacements Enumerator

## Description

The placement options for a two-bend relief.  

## Methods

| Name | Value | Description |
|----|----|----|
| IntersectionTwoBendReliefPlacement | 1 | Specifies that the center point of the two-bend relief shape is located at the intersection of the bend center lines. This is the only valid placement option for square two-bend relief shapes. For round shapes, this and tangent placement is valid. |
| NoTwoBendReliefPlacement | 0 | Specifies that no two-bend relief placement is defined. This is returned for all two-bend relief shapes except for round and square shapes. |
| TangentTwoBendReliefPlacement | 2 | Specifies that the shape of the two-bend relief is tangential to the flange sides. This is only used for round to bend relief shapes where this or intersection placement is valid. |

## Version

Introduced in version November 2022  

