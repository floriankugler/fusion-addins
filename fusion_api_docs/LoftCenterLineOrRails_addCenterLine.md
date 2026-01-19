# LoftCenterLineOrRails.addCenterLine Method

Parent Object: [LoftCenterLineOrRails](LoftCenterLineOrRails.md)  

## Description

Adds a centerline. A single centerline can be defined for a loft. If a centerline or rails have already been defined, they will be removed and the input will become the new single centerline.  

If this LoftCenterLineOrRails object is associated with a created feature,

## Syntax

"loftCenterLineOrRails_var" is a variable referencing a [LoftCenterLineOrRails](LoftCenterLineOrRails.md) object.

```python
returnValue = loftCenterLineOrRails_var.addCenterLine(entity)
```

## Return Value

| Type | Description |
|----|----|
| [LoftCenterLineOrRail](LoftCenterLineOrRail.md) | Returns the new LoftCenterLineOrRail object or null in the case of a failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entity | [Base](Base.md) | The entity that defines the center line. This can be a single sketch curve, a single BRepEdge, a Path consisting of connected B-Rep edges or sketch curves. |

## Version

Introduced in version August 2016  

