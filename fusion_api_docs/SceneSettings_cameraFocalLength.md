# SceneSettings.cameraFocalLength Property

Parent Object: [SceneSettings](SceneSettings.md)  

## Description

Gets and sets the focal length of the camera, specified in millimeters. Changing the perspective angle of the camera associated with the active viewport will also change the focal length. Focal length and perspective angle are two different ways to control the same setting.

## Syntax

"sceneSettings_var" is a variable referencing a SceneSettings object.  

```python
# Get the value of the property.
propertyValue = sceneSettings_var.cameraFocalLength

# Set the value of the property.
sceneSettings_var.cameraFocalLength = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version May 2023  

