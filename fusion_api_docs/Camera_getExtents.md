# Camera.getExtents Method

Parent Object: [Camera](Camera.md)  

## Description

Gets the extents of the camera. This is only used for orthographic cameras. The extents of a perspective camera is defined by a combination of the position of the eye point (how close the eye is to the model) and the perspective angle.

## Syntax

"camera_var" is a variable referencing a [Camera](Camera.md) object.  

```python
(returnValue, width, height) = camera_var.getExtents()
```

## Return Value

| Type | Description |
|----|----|
| boolean | Returns true if successful. This will fail in the case it is used for a perspective camera. |

## Parameters

| Name   | Type   | Description                              |
|--------|--------|------------------------------------------|
| width  | double | The width of the extent in centimeters.  |
| height | double | The height of the extent in centimeters. |

## Version

Introduced in version October 2023  

