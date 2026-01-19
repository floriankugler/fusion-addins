# WorkingModel.physicalProperties Method

Parent Object: [WorkingModel](WorkingModel.md)  

## Description

Returns the PhysicalProperties object that has properties for getting the area, density, mass, volume, moments, etc for a collection of 3D solid objects.

## Syntax

"workingModel_var" is a variable referencing a [WorkingModel](WorkingModel.md) object.

```python
# Uses no optional arguments.
returnValue = workingModel_var.physicalProperties(inputs)

# Uses optional arguments.
returnValue = workingModel_var.physicalProperties(inputs, accuracy)
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| inputs | [ObjectCollection](ObjectCollection.md) | A collection of one or more 3D solid input objects to perform the calculations on. Supported input object types are Components, Occurrences and BRepBodies. Calculation results reflect the sums of the input objects (i.e. total volume of multiple bodies) |
| accuracy | [CalculationAccuracy](CalculationAccuracy.md) | Specifies the desired level of computational accuracy of the property calculations. The default value of 'LowCalculationAccuracy' returns results within a +/- 1% error margin. This is an optional argument whose default value is CalculationAccuracy.LowCalculationAccuracy. |

## Version

Introduced in version January 2024  

