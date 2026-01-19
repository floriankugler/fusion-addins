# PathEntity.curve Property

Parent Object: [PathEntity](PathEntity.md)  

## Description

Property that returns the geometry of the entity. This is different from the original path curve if the true start point is not the same as the start point of the original path curve.

## Syntax

"pathEntity_var" is a variable referencing a PathEntity object.  

```python
# Get the value of the property.
propertyValue = pathEntity_var.curve
```

## Property Value

This is a read only property whose value is a [Curve3D](Curve3D.md).

## Version

Introduced in version November 2014  

