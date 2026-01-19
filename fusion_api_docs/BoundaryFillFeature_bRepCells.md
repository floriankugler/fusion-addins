# BoundaryFillFeature.bRepCells Property

Parent Object: [BoundaryFillFeature](BoundaryFillFeature.md)  

## Description

Gets the set of closed boundaries that have been calculated based on the current set of tools. To get this collection the model must be in the state it was when the feature was initially computed, which means the timeline marker must be positioned to immediately before this feature.  

After changing any selected cells you must call the applyCellChanges method to update the feature with the changes.

## Syntax

"boundaryFillFeature_var" is a variable referencing a BoundaryFillFeature object.  

```python
# Get the value of the property.
propertyValue = boundaryFillFeature_var.bRepCells
```

## Property Value

This is a read only property whose value is a [BRepCells](BRepCells.md).

## Version

Introduced in version June 2015  

