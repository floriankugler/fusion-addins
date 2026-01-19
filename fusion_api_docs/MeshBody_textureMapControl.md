# MeshBody.textureMapControl Property

Parent Object: [MeshBody](MeshBody.md)  

## Description

Returns the TextureMapControl object associated with this body when there is an appearance assigned to the body that has a texture associated with it. If there isn't a texture, this property will return null. If there is a texture, you can use the returned object to query and modify how the texture is applied to the body.

## Syntax

"meshBody_var" is a variable referencing a MeshBody object.  

```python
# Get the value of the property.
propertyValue = meshBody_var.textureMapControl
```

## Property Value

This is a read only property whose value is a [TextureMapControl](TextureMapControl.md).

## Version

Introduced in version May 2022  

