# MeshBody.isLightBulbOn Property

Parent Object: [MeshBody](MeshBody.md)  

## Description

Is the light bulb (as displayed in the browser) on. A mesh body will only be visible if the light bulb is switched on. However, the light bulb can be on and the mesh body is still invisible if the light bulb for all bodies or the owning component is off.

## Syntax

"meshBody_var" is a variable referencing a MeshBody object.  

```python
# Get the value of the property.
propertyValue = meshBody_var.isLightBulbOn

# Set the value of the property.
meshBody_var.isLightBulbOn = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name                                          | Description                 |
|-----------------------------------------------|-----------------------------|
| [Mesh Body Sample](MeshBodySample_Sample.md) | Mesh body related functions |

## Version

Introduced in version August 2014  

