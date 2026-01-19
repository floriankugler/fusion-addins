# RevolveFeatures.createInput Method

Parent Object: [RevolveFeatures](RevolveFeatures.md)  

## Description

Creates a new RevolveFeatureInput object that is used to specify the input needed to create a new revolve feature.

## Syntax

"revolveFeatures_var" is a variable referencing a [RevolveFeatures](RevolveFeatures.md) object.

```python
returnValue = revolveFeatures_var.createInput(profile, axis, operation)
```

## Return Value

| Type | Description |
|----|----|
| [RevolveFeatureInput](RevolveFeatureInput.md) | Returns the newly created RevolveFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| profile | [Base](Base.md) | The profile argument can be a single Profile, a single planar face, or an ObjectCollection consisting of multiple profiles and planar faces. When an ObjectCollection is used all of the profiles and faces must be co-planar. To create a surface (non-solid) revolution, you can use the createOpenProfile and createBRepEdgeProfile methods of the Component object to create an open profile. You also need to set the isSolid property of the returned RevolveFeatureInput property to False. |
| axis | [Base](Base.md) | The axis can be a sketch line, construction axis, linear edge or a face that defines an axis (cylinder, cone, torus, etc.). If it is not in the same plane as the profile, it is projected onto the profile plane. |
| operation | [FeatureOperations](FeatureOperations.md) | The operation type to perform. |

## Samples

| Name | Description |
|----|----|
| [revolveFeatures.add](revolveFeatures_add_Sample.md) | Demonstrates creating a revolve feature using an angle extent. |
| [Simple Revolve Feature Sample](SimpleRevolveFeatureSample_Sample.md) | Creates a new revolve feature, resulting in a new component. |

## Version

Introduced in version August 2014  

