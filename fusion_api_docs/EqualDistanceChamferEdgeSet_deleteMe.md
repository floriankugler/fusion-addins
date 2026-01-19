# EqualDistanceChamferEdgeSet.deleteMe Method

Parent Object: [EqualDistanceChamferEdgeSet](EqualDistanceChamferEdgeSet.md)  

## Description

Deletes the chamfer edge set from the chamfer.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"equalDistanceChamferEdgeSet_var" is a variable referencing an [EqualDistanceChamferEdgeSet](EqualDistanceChamferEdgeSet.md) object.

```python
returnValue = equalDistanceChamferEdgeSet_var.deleteMe()
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Version

Introduced in version December 2020  

