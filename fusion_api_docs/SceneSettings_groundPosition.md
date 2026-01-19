# SceneSettings.groundPosition Property

Parent Object: [SceneSettings](SceneSettings.md)  

## Description

Gets and sets the origin of the projection of the environment onto the textured ground plane. This lets you position the environment relative to the model. This is only used when the isGroundFlattened property is true.  

If the isGroundFlattened property is true, and a texture is being applied to the ground, the groundPosition property can be used to change both the offset and location of the texture on the ground. The lightAngle property controls the orientation of the texture.

## Syntax

"sceneSettings_var" is a variable referencing a SceneSettings object.  

```python
# Get the value of the property.
propertyValue = sceneSettings_var.groundPosition

# Set the value of the property.
sceneSettings_var.groundPosition = propertyValue
```

## Property Value

This is a read/write property whose value is a [Point3D](Point3D.md).

## Version

Introduced in version May 2023  

