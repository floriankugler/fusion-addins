# Design.setGroundPlaneOffset Method

Parent Object: [Design](Design.md)  

## Description

Sets the offset of the ground plane. If the isAdpativeGroundPlane property is true, setting the offset will change isAdaptiveGroundPlane to false. The offset value is an offset relative to the current position of the ground plane.  

One example of how this method can be used is to set the isAdaptiveGroundPlane property to true, which will position the ground plane at the bottom of the part. By doing this, you know the current position of the ground plane. Then calling this method with a value of -2.0 will reposition the ground plane 2 cm below the part. If you called this method again with a value of -1.0 the ground plane will be moved an additional 1 cm away from the geometry, since this is defining an offset relative to the current position.

## Syntax

"design_var" is a variable referencing a [Design](Design.md) object.

```python
returnValue = design_var.setGroundPlaneOffset(offset)
```

## Return Value

| Type    | Description                                        |
|---------|----------------------------------------------------|
| boolean | Returns true if setting the offset was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| offset | double | Defines the relative offset based on the current position of the ground plane. The offset is in centimeters, and a positive value will move it towards the design geometry and a negative value away from the geometry. |

## Version

Introduced in version November 2025  

