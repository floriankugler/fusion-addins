# OffsetCornerTypes Enumerator

## Description

Specifies the different types of corners that can be created when offsetting a wire body. These settings are used when the curves are offset outwards, which creates a gap at the corner. These represent the three ways the gap is filled.  

## Methods

| Name | Value | Description |
|----|----|----|
| CircularOffsetCornerType | 0 | Creates an arc at the corner to fill the gap. This is similar to filleting the corner with a fillet that is the same radius as the offset. |
| ExtendedOffsetCornerType | 2 | Extends the offset curves so the connect at the corner. |
| LinearOffsetCornerType | 1 | Creates lines that are tangent to the offset curves and connect at the corner. |

## Version

Introduced in version December 2017  

