# BRepCell.isSelected Property

Parent Object: [BRepCell](BRepCell.md)  

## Description

Gets and sets whether the cell is selected. For a Trim feature a selected cell is removed, whereas for a boundary fill feature, a selected cell is kept and used in the feature operation.

## Syntax

"bRepCell_var" is a variable referencing a BRepCell object.  

```python
# Get the value of the property.
propertyValue = bRepCell_var.isSelected

# Set the value of the property.
bRepCell_var.isSelected = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Samples

| Name | Description |
|----|----|
| [boundaryFillFeatures.add](boundaryFillFeatures_add_Sample.md) | Demonstrates the boundaryFill.add method. To use this sample you need to have two existing overlapping bodies. You'll be prompted to select the bodies when running the script. |
| [Boundary Fill Feature API Sample](BoundaryFillFeatureSample_Sample.md) | Demonstrates creating a new boundary fill feature. |
| [Trim Feature API Sample](TrimFeatureSample_Sample.md) | Demonstrates creating a new trim feature. |

## Version

Introduced in version June 2015  

