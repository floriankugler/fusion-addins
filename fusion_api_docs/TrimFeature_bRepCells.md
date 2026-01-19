# TrimFeature.bRepCells Property

Parent Object: [TrimFeature](TrimFeature.md)  

## Description

Gets the set of valid cells that have been calculated based on the current inputs. To get this collection the model must be in the state it was when the feature was initially computed, which means the timeline marker must be positioned to immediately before this feature.  

After changing any selected cells you must call the applyCellChanges method to update the feature with the changes.

## Syntax

"trimFeature_var" is a variable referencing a TrimFeature object.  

```python
# Get the value of the property.
propertyValue = trimFeature_var.bRepCells
```

## Property Value

This is a read only property whose value is a [BRepCells](BRepCells.md).

## Version

Introduced in version July 2015  

