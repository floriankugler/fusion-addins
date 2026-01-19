# SketchPoint.connectedEntities Property

Parent Object: [SketchPoint](SketchPoint.md)  

## Description

Returns the set of sketch entities that are directly connected to this point. For example any entities that use this point as their start point or end point will be returned and any circle, arc or ellipse who have this point as a center point will be returned. This does not include entities that are related to the point through a constraint.

## Syntax

"sketchPoint_var" is a variable referencing a SketchPoint object.  

```python
# Get the value of the property.
propertyValue = sketchPoint_var.connectedEntities
```

## Property Value

This is a read only property whose value is a [SketchEntityList](SketchEntityList.md).

## Version

Introduced in version June 2015  

