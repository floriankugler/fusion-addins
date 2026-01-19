# MachineTCPInterpolationMode Enumerator

## Description

Interpolation modes available for TCP motions.  

## Methods

| Name | Value | Description |
|----|----|----|
| MachineTCPInterpolationMode_IndependentAxes | 1 | Moves the axes together, completing the motion simultaneously, although the tool's tip may deviate from the direct line between the start and finish points. |
| MachineTCPInterpolationMode_SynchronizedAxes | 0 | Moves the axes independently at maximum speed, potentially resulting in different completion times for each axis |
| MachineTCPInterpolationMode_ToolTip | 2 | Adjusts the linear axes to keep the tool's tip positioned along the direct line between the start and finish points. |

## Version

Introduced in version September 2025  

