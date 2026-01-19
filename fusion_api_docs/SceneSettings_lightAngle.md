# SceneSettings.lightAngle Property

Parent Object: [SceneSettings](SceneSettings.md)  

## Description

Specifies the rotation of the lighting. The angle is specified in Radians.  

When the isGroundFlattened property is true, this also controls the angle of the texture that is applied to the ground. When the background is an environment, this controls the rotation of the environment relative to the model.

## Syntax

"sceneSettings_var" is a variable referencing a SceneSettings object.  

```python
# Get the value of the property.
propertyValue = sceneSettings_var.lightAngle

# Set the value of the property.
sceneSettings_var.lightAngle = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version May 2023  

