# Camera.isSmoothTransition Property

Parent Object: [Camera](Camera.md)  

## Description

This property controls if Fusion will perform a smooth transition animation from the current camera position to the new position. If this property is set to true, it will smoothly transition. If false, the camera will jump to the position defined by the camera without any animated transition.  

When a camera is obtained from a Viewport or created using the Camera.create() method, this property defaults to false.

## Syntax

"camera_var" is a variable referencing a Camera object.  

```python
# Get the value of the property.
propertyValue = camera_var.isSmoothTransition

# Set the value of the property.
camera_var.isSmoothTransition = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2014  

