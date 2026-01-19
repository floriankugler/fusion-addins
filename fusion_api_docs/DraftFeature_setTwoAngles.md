# DraftFeature.setTwoAngles Method

Parent Object: [DraftFeature](DraftFeature.md)  

## Description

Changes the definition of the feature so that the surfaces are split along the draft plane or parting line and the faces on each side of the plane are drafted independently.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"draftFeature_var" is a variable referencing a [DraftFeature](DraftFeature.md) object.

```python
returnValue = draftFeature_var.setTwoAngles(angleOne, angleTwo)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| angleOne | [ValueInput](ValueInput.md) | The ValueInput object that defines the angle for the faces on the first side of the draft plane or parting line. |
| angleTwo | [ValueInput](ValueInput.md) | The ValueInput object that defines the angle for the faces on the second side of the draft plane or parting line. |

## Version

Introduced in version January 2015  

