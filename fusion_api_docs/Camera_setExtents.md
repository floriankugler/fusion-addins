# Camera.setExtents Method

Parent Object: [Camera](Camera.md)  

## Description

Sets the extents of the camera. This is only used for orthographic cameras. The extents of a perspective camera is defined by a combination of the position of the eye point (how close the eye is to the model) and the perspective angle.  

When the camera is assigned to a viewport, typically only the width or the height is used depending on the aspect ratio of the viewport. For example, if the width and height are both 10, but the viewport is twice as wide as it is tall (2:1 aspect ratio). The height extent will be 10 and the width extent will be recomputed to be 20 to match the viewport.

## Syntax

"camera_var" is a variable referencing a [Camera](Camera.md) object.

```python
returnValue = camera_var.setExtents(width, height)
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

