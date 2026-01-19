# SceneSettings.groundRoughness Property

Parent Object: [SceneSettings](SceneSettings.md)  

## Description

Gets and sets the roughness of the ground which controls the sharpness of the reflection. This is only used when the isGroundReflections property is true. This is a value between 0 and 1, where 0 is smooth and 1 is rough.

## Syntax

"sceneSettings_var" is a variable referencing a SceneSettings object.  

```python
# Get the value of the property.
propertyValue = sceneSettings_var.groundRoughness

# Set the value of the property.
sceneSettings_var.groundRoughness = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version May 2023  

