# BoundaryFillFeature.applyCellChanges Method

Parent Object: [BoundaryFillFeature](BoundaryFillFeature.md)  

## Description

After making any changes to the set of selected cells you must call this method to indicate all changes have been made and to apply those changes to the feature.

## Syntax

"boundaryFillFeature_var" is a variable referencing a [BoundaryFillFeature](BoundaryFillFeature.md) object.

```python
returnValue = boundaryFillFeature_var.applyCellChanges()
```

## Return Value

| Type    | Description                               |
|---------|-------------------------------------------|
| boolean | Returns true if the apply was successful. |

## Version

Introduced in version June 2015  

