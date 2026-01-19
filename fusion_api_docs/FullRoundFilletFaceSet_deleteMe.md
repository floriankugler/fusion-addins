# FullRoundFilletFaceSet.deleteMe Method

Parent Object: [FullRoundFilletFaceSet](FullRoundFilletFaceSet.md)  

## Description

Deletes the full round fillet face set from the fillet.  

When this face set is associated with an existing fillet feature, to use this method you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True).

## Syntax

"fullRoundFilletFaceSet_var" is a variable referencing a [FullRoundFilletFaceSet](FullRoundFilletFaceSet.md) object.

```python
returnValue = fullRoundFilletFaceSet_var.deleteMe()
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Version

Introduced in version September 2025  

