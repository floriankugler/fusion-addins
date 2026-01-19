# LoftCenterLineOrRails.addRail Method

Parent Object: [LoftCenterLineOrRails](LoftCenterLineOrRails.md)  

## Description

Add a rail to the loft definition. Multiple rails can be defined, so each call of this method adds a new rail.  

If this LoftCenterLineOrRails object is associated with a created feature, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"loftCenterLineOrRails_var" is a variable referencing a [LoftCenterLineOrRails](LoftCenterLineOrRails.md) object.

```python
returnValue = loftCenterLineOrRails_var.addRail(entity)
```

## Return Value

| Type | Description |
|----|----|
| [LoftCenterLineOrRail](LoftCenterLineOrRail.md) | Returns the new LoftCenterLineOrRail object or null in the case of a failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| entity | [Base](Base.md) | The entity that defines the rail. This can be a single sketch curve, a single BRepEdge, or a Path consisting of connected B-Rep edges or sketch curves. |

## Version

Introduced in version August 2016  

