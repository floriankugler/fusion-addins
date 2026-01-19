# ToEntityExtentDefinition.directionHint Property

Parent Object: [ToEntityExtentDefinition](ToEntityExtentDefinition.md)  

## Description

Gets and sets a direction that is used when the result is ambiguous. For example, if you have a profile in the center of a torus and are extruding to the torus, the extrusion can go in either direction. When needed, this provides the information to tell Fusion which direction to go. In most cases this is not needed and the property will be null.

## Syntax

"toEntityExtentDefinition_var" is a variable referencing a ToEntityExtentDefinition object.  

```python
# Get the value of the property.
propertyValue = toEntityExtentDefinition_var.directionHint

# Set the value of the property.
toEntityExtentDefinition_var.directionHint = propertyValue
```

## Property Value

This is a read/write property whose value is a [Vector3D](Vector3D.md).

## Version

Introduced in version November 2016  

