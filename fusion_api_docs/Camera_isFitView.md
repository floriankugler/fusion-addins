# Camera.isFitView Property

Parent Object: [Camera](Camera.md)  

## Description

If this property is true, when this camera is applied to a viewport it will modify the camera such that the entire model is displayed in the viewport. When getting a camera from a viewport or creating a camera using Camera.create(), this property defaults to false.

## Syntax

"camera_var" is a variable referencing a Camera object.  

```python
# Get the value of the property.
propertyValue = camera_var.isFitView

# Set the value of the property.
camera_var.isFitView = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
|----|----|
| [As-Built Joint Sample](AsBuiltJointSample_Sample.md) | Demonstrates creating a new As-Built Joint. |
| [Joint Origin Sample](JointOriginSample_Sample.md) | Demonstrates creating a new Joint Origin. |
| [Rigid Group API Sample](RigidGroupSample_Sample.md) | Demonstrates creating a new Rigid Group. |

## Version

Introduced in version August 2014  

