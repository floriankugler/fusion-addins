# DraftFeatureInput.setTwoAngles Method

Parent Object: [DraftFeatureInput](DraftFeatureInput.md)  

## Description

Defines both angles to use when the surfaces are split along the draft plane or parting line and the faces on each side of the plane are drafted independently.

## Syntax

"draftFeatureInput_var" is a variable referencing a [DraftFeatureInput](DraftFeatureInput.md) object.

```python
returnValue = draftFeatureInput_var.setTwoAngles(angleOne, angleTwo)
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

