# RevolveFeatureInput.setAngleExtent Method

Parent Object: [RevolveFeatureInput](RevolveFeatureInput.md)  

## Description

Defines the extent of the revolution to be at a specified angle. An angle and whether the extent is symmetric or only in one direction is specified. If it's not symmetric a positive or negative angle can be used to control the direction. If symmetric, the angle is the angle on one side so the entire angle of the revolution will be twice the specified angle. Use an angle of 360 deg or 2 pi radians to create a full revolve.

## Syntax

"revolveFeatureInput_var" is a variable referencing a [RevolveFeatureInput](RevolveFeatureInput.md) object.

```python
returnValue = revolveFeatureInput_var.setAngleExtent(isSymmetric, angle)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| isSymmetric | boolean | Set to 'true' for a revolve symmetrical about the profile plane |
| angle | [ValueInput](ValueInput.md) | The ValueInput object that defines the angle of the revolution |

## Samples

| Name | Description |
|----|----|
| [revolveFeatures.add](revolveFeatures_add_Sample.md) | Demonstrates creating a revolve feature using an angle extent. |
| [Simple Revolve Feature Sample](SimpleRevolveFeatureSample_Sample.md) | Creates a new revolve feature, resulting in a new component. |

## Version

Introduced in version August 2014  

