# WorkingModel.areaProperties Method

Parent Object: [WorkingModel](WorkingModel.md)  

## Description

Returns the AreaProperties object that has properties for getting the area, perimeter, centroid, etc for a collection of 2D sketch profiles and/or planar surfaces that all lie on the same plane.

## Syntax

"workingModel_var" is a variable referencing a [WorkingModel](WorkingModel.md) object.

```python
# Uses no optional arguments.
returnValue = workingModel_var.areaProperties(inputs)

# Uses optional arguments.
returnValue = workingModel_var.areaProperties(inputs, accuracy)
```

## Return Value

| Type | Description |
|----|----|
| [AreaProperties](AreaProperties.md) | Returns an AreaProperties object that can be used to examine the area results. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| inputs | [ObjectCollection](ObjectCollection.md) | A collection of one or more 2D sketch profile and/or planar surface input objects to perform the calculations on. Supported input object types are 2D closed sketch profiles and planar surfaces. Object must all lie on the same plane. Calculation results reflect the sums of the input objects (i.e. total area of multiple sketch profiles) |
| accuracy | [CalculationAccuracy](CalculationAccuracy.md) | Specifies the desired level of computational accuracy of the property calculations. The default value of 'LowCalculationAccuracy' returns results within a +/- 1% error margin. This is an optional argument whose default value is CalculationAccuracy.LowCalculationAccuracy. |

## Version

Introduced in version January 2024  

