# ChamferEdgeSet.deleteMe Method

Parent Object: [ChamferEdgeSet](ChamferEdgeSet.md)  

## Description

Deletes the chamfer edge set from the chamfer.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"chamferEdgeSet_var" is a variable referencing a [ChamferEdgeSet](ChamferEdgeSet.md) object.

```python
returnValue = chamferEdgeSet_var.deleteMe()
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Version

Introduced in version December 2020  

