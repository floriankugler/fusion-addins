# ConstantRadiusFilletEdgeSet.deleteMe Method

Parent Object: [ConstantRadiusFilletEdgeSet](ConstantRadiusFilletEdgeSet.md)  

## Description

Deletes the fillet edge set from the fillet.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"constantRadiusFilletEdgeSet_var" is a variable referencing a [ConstantRadiusFilletEdgeSet](ConstantRadiusFilletEdgeSet.md) object.

```python
returnValue = constantRadiusFilletEdgeSet_var.deleteMe()
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Version

Introduced in version November 2022  

