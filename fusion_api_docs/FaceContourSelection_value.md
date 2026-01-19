# FaceContourSelection.value Property

Parent Object: [FaceContourSelection](FaceContourSelection.md)  

## Description

Returns the resulting value of the selection. In general, this returns the input selection, but child classes can override the return value if needed. Refer to the child classes comments for further details. The collection may contain duplicates. For OperationInputs, the return value may not be the same as for Operations, as additional geometry selected by child classes is not evaluated for OperationInputs.

## Syntax

"faceContourSelection_var" is a variable referencing a FaceContourSelection object.  

```python
# Get the value of the property.
propertyValue = faceContourSelection_var.value
```

## Property Value

This is a read only property whose value is an array of type [Base](Base.md).

## Version

Introduced in version April 2023  

