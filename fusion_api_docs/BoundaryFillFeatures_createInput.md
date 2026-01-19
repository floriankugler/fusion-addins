# BoundaryFillFeatures.createInput Method

Parent Object: [BoundaryFillFeatures](BoundaryFillFeatures.md)  

## Description

Creates a BoundaryFillFeatureInput object. Use properties and methods on this object to define the boundary fill you want to create and then use the Add method, passing in the BoundaryFillFeatureInput object.  

To determine the possible boundaries and allow you to choose which cells to keep, the boundary fill feature does a partial compute when the input object is created. To do this it starts a boundary fill feature transaction and completes the transaction when you call the add method. If you don't call the add method to finish the transaction it leaves Fusion in a bad state and there will be undo problems and possibly a crash. If you have created a BoundFillFeatureInput object and don't want to finish the feature creation, you need to call the cancel method on the BoundaryFillFeatureInput object to safely abort the current boundary fill transaction.

## Syntax

"boundaryFillFeatures_var" is a variable referencing a [BoundaryFillFeatures](BoundaryFillFeatures.md) object.

```python
returnValue = boundaryFillFeatures_var.createInput(tools, operation)
```

## Return Value

| Type | Description |
|----|----|
| [BoundaryFillFeatureInput](BoundaryFillFeatureInput.md) | Returns the newly created BoundaryFillFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| tools | [ObjectCollection](ObjectCollection.md) | A collection of one or more construction planes and open or closed BRepBody objects that will be used in calculating the possible closed boundaries. |
| operation | [FeatureOperations](FeatureOperations.md) | The operation type to perform. |

## Samples

| Name | Description |
|----|----|
| [boundaryFillFeatures.add](boundaryFillFeatures_add_Sample.md) | Demonstrates the boundaryFill.add method. To use this sample you need to have two existing overlapping bodies. You'll be prompted to select the bodies when running the script. |
| [Boundary Fill Feature API Sample](BoundaryFillFeatureSample_Sample.md) | Demonstrates creating a new boundary fill feature. |

## Version

Introduced in version June 2015  

