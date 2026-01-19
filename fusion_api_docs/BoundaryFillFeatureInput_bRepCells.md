# BoundaryFillFeatureInput.bRepCells Property

Parent Object: [BoundaryFillFeatureInput](BoundaryFillFeatureInput.md)  

## Description

Returns the collection of the valid cells that have been calculated based on the set of input tools. You use this collection to specify which cells you want included in the output.

## Syntax

"boundaryFillFeatureInput_var" is a variable referencing a BoundaryFillFeatureInput object.  

```python
# Get the value of the property.
propertyValue = boundaryFillFeatureInput_var.bRepCells
```

## Property Value

This is a read only property whose value is a [BRepCells](BRepCells.md).

## Samples

| Name | Description |
|----|----|
| [boundaryFillFeatures.add](boundaryFillFeatures_add_Sample.md) | Demonstrates the boundaryFill.add method. To use this sample you need to have two existing overlapping bodies. You'll be prompted to select the bodies when running the script. |
| [Boundary Fill Feature API Sample](BoundaryFillFeatureSample_Sample.md) | Demonstrates creating a new boundary fill feature. |

## Version

Introduced in version June 2015  

