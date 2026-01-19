# DraftFeature.setSingleAngle Method

Parent Object: [DraftFeature](DraftFeature.md)  

## Description

Changes the definition of the feature so that a single angle is used for all drafts. If the isSymmetric is true then the faces are split along the parting plane and drafted independently using the same angle.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"draftFeature_var" is a variable referencing a [DraftFeature](DraftFeature.md) object.

```python
returnValue = draftFeature_var.setSingleAngle(isSymmetric, angle)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| isSymmetric | boolean | Set to true if the faces are to be split along the plane or parting line and drafted symmetrically. This will have the side effect of setting the isSymmetric property to the same value. |
| angle | [ValueInput](ValueInput.md) | The ValueInput object that defines the angle of the draft. This can be a positive or negative value which will affect the direction of the draft along with the isDirectionFlipped property. |

## Version

Introduced in version January 2015  

