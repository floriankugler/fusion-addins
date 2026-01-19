# ArrangeFeatures.createInput Method

Parent Object: [ArrangeFeatures](ArrangeFeatures.md)  

## Description

Creates a new ArrangeFeatureInput object. An ArrangeFeatureInput object is the logical equivalent to the command dialog when creating an Arrange feature. It provides access to the various options and collects all the required input when creating an Arrange feature. Once fully defined, you pass this into the add method to create the Arrange feature.

## Syntax

"arrangeFeatures_var" is a variable referencing an [ArrangeFeatures](ArrangeFeatures.md) object.

```python
returnValue = arrangeFeatures_var.createInput(solverType)
```

## Return Value

| Type | Description |
|----|----|
| [ArrangeFeatureInput](ArrangeFeatureInput.md) | Returns an ArrangeFeatureInput object or null in the case of failure. |

## Parameters

| Name | Type | Description |
|----|----|----|
| solverType | [ArrangeSolverTypes](ArrangeSolverTypes.md) | Specify if the input will be used to define a "2D True Shape", "2D Rectangular", or "3D" type of arrange feature. |

## Version

Introduced in version January 2025  

