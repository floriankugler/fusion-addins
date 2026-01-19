# DraftFeatureInput.setSingleAngle Method

Parent Object: [DraftFeatureInput](DraftFeatureInput.md)  

## Description

Defines the draft to be defined so that a single angle is used for all drafts. If the isSymmetric is true then the faces are split along the parting plane and drafted independently using the same angle.

## Syntax

"draftFeatureInput_var" is a variable referencing a [DraftFeatureInput](DraftFeatureInput.md) object.

```python
returnValue = draftFeatureInput_var.setSingleAngle(isSymmetric, angle)
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

## Samples

| Name | Description |
|----|----|
| [draftFeatures.add](draftFeatures_add_Sample.md) | Demonstrates the draftFeatures.add method. To use this sample, have a design open that contains at least one body. When you run the sample, you will be prompted to select the face to draft. Because the pull direction is using the base X-Y plane, you need to select a face that is not parallel to the X-Y plane. |
| [Draft Feature API Sample](DraftFeatureSample_Sample.md) | Demonstrates creating a new draft feature. |

## Version

Introduced in version January 2015  

