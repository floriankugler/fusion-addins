# RevolveFeatureInput.setTwoSideAngleExtent Method

Parent Object: [RevolveFeatureInput](RevolveFeatureInput.md)  

## Description

Defines the angle of the revolve to be to applied to both sides of the profile at the specified angles.

## Syntax

"revolveFeatureInput_var" is a variable referencing a [RevolveFeatureInput](RevolveFeatureInput.md) object.

```python
returnValue = revolveFeatureInput_var.setTwoSideAngleExtent(angleOne, angleTwo)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| angleOne | [ValueInput](ValueInput.md) | The ValueInput object that defines the angle for the first side of the revolution |
| angleTwo | [ValueInput](ValueInput.md) | The ValueInput object that defines the angle for the second side of the revolution |

## Version

Introduced in version August 2014  

