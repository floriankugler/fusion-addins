# Camera.viewExtents Property

Parent Object: [Camera](Camera.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Defines the area that's visible by the camera. This value is the radius of a sphere centered at the target point. The camera will display everything within that sphere and everything in front of and behind the sphere. Additional geometry outside of the sphere will also be visible depending on the shape of the window. Setting this value can cause the eye and/or perspective angle to be modified when the camera type is perspective.

## Remarks

This property has been replaced by the getExtents and setExtents methods.

## Syntax

"camera_var" is a variable referencing a Camera object.  

```python
# Get the value of the property.
propertyValue = camera_var.viewExtents

# Set the value of the property.
camera_var.viewExtents = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version August 2014  
Retired in version October 2023  

