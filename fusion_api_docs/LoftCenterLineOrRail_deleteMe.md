# LoftCenterLineOrRail.deleteMe Method

Parent Object: [LoftCenterLineOrRail](LoftCenterLineOrRail.md)  

## Description

Deletes the centerline or rail.  

If this LoftCenterLineOrRail object is associated with a created feature, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"loftCenterLineOrRail_var" is a variable referencing a [LoftCenterLineOrRail](LoftCenterLineOrRail.md) object.

```python
returnValue = loftCenterLineOrRail_var.deleteMe()
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Version

Introduced in version August 2016  

