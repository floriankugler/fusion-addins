# TrimFeature.applyCellChanges Method

Parent Object: [TrimFeature](TrimFeature.md)  

## Description

After making any changes to the set of selected cells you must call this method to indicate all changes have been made and to apply those changes to the feature.

## Syntax

"trimFeature_var" is a variable referencing a [TrimFeature](TrimFeature.md) object.

```python
returnValue = trimFeature_var.applyCellChanges()
```

## Return Value

| Type    | Description                               |
|---------|-------------------------------------------|
| boolean | Returns true if the apply was successful. |

## Version

Introduced in version July 2015  

