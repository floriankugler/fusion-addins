# SceneSettings.groundOffset Property

Parent Object: [SceneSettings](SceneSettings.md)  

## Description

Gets and sets the distance of the ground from the bottom of the model. A value of 0 is at the bottom of the model and a positive value moves the plane up and negative down. The value is in centimeters.  

If the isGroundFlattened property is true, and a texture is being applied to the ground, the groundPosition property can be used to change both the offset and location of the texture on the ground. The lightAngle property controls the orientation of the texture.

## Syntax

"sceneSettings_var" is a variable referencing a SceneSettings object.  

```python
# Get the value of the property.
propertyValue = sceneSettings_var.groundOffset

# Set the value of the property.
sceneSettings_var.groundOffset = propertyValue
```

## Property Value

This is a read/write property whose value is a double.

## Version

Introduced in version May 2023  

