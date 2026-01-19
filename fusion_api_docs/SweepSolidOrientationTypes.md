# SweepSolidOrientationTypes Enumerator

## Description

The various orientation types when doing a solid sweep.  

## Methods

| Name | Value | Description |
|----|----|----|
| AlignedSolidOrientationType | 2 | Keep the orientation of the tool body aligned to a direction vector. The tool may rotate around this vector as it is swept along the path. |
| PerpendicularSolidOrientationType | 0 | Maintain the orientation of the tool body relative to the sweep path. As the tool body sweeps along the path, it will rotate to maintain the same relative angle to the path. |
| RigidSolidOrientationType | 1 | The orientation of the tool body does not change as it is swept along the path. The tool will be translated but not rotated. |

## Version

Introduced in version May 2024  

