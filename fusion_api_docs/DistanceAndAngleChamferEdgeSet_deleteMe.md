# DistanceAndAngleChamferEdgeSet.deleteMe Method

Parent Object: [DistanceAndAngleChamferEdgeSet](DistanceAndAngleChamferEdgeSet.md)  

## Description

Deletes the chamfer edge set from the chamfer.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"distanceAndAngleChamferEdgeSet_var" is a variable referencing a [DistanceAndAngleChamferEdgeSet](DistanceAndAngleChamferEdgeSet.md) object.

```python
returnValue = distanceAndAngleChamferEdgeSet_var.deleteMe()
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Version

Introduced in version December 2020  

