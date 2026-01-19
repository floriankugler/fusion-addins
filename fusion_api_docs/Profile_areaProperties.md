# Profile.areaProperties Method

Parent Object: [Profile](Profile.md)  

## Description

Calculates the area properties for the profile.

## Syntax

"profile_var" is a variable referencing a [Profile](Profile.md) object.

```python
# Uses no optional arguments.
returnValue = profile_var.areaProperties()

# Uses optional arguments.
returnValue = profile_var.areaProperties(accuracy)
```

## Return Value

| Type | Description |
|----|----|
| [AreaProperties](AreaProperties.md) | Returns the AreaProperties object that has properties for getting the area, perimeter, centroid, etc of this profile. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| accuracy | [CalculationAccuracy](CalculationAccuracy.md) | Specifies the desired level of computational accuracy of the property calculations. The default value of 'LowCalculationAccuracy' returns results within a +/- 1% error margin. This is an optional argument whose default value is CalculationAccuracy.LowCalculationAccuracy. |

## Samples

| Name | Description |
|----|----|
| [API Sample for AreaProperties](AreaPropertiesSample_Sample.md) | Demonstrates how to use AreaProperties |
| [Patch Feature API Sample](PatchFeatureSample_Sample.md) | Demonstrates creating a new patch feature. |

## Version

Introduced in version March 2016  

