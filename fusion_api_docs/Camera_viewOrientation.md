# Camera.viewOrientation Property

Parent Object: [Camera](Camera.md)  

## Description

Sets the camera to a standard orientation. If this is set, it will result in resetting all the camera values except the camera type. The orientation is based on the current orientation defined by the ViewCube. This means, that the view orientations cannot be expected to be consistent from one view to another.

## Syntax

"camera_var" is a variable referencing a Camera object.  

```python
# Get the value of the property.
propertyValue = camera_var.viewOrientation

# Set the value of the property.
camera_var.viewOrientation = propertyValue
```

## Property Value

This is a read/write property whose value is a [ViewOrientations](ViewOrientations.md).

## Version

Introduced in version August 2014  

