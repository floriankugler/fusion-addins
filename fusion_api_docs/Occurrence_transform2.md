# Occurrence.transform2 Property

Parent Object: [Occurrence](Occurrence.md)  

## Description

Gets and sets the 3d matrix data that defines this occurrences orientation and position in its assembly context. This property replaces the transform property, which has been retired because there are cases where it returns the incorrect results.

## Syntax

"occurrence_var" is a variable referencing an Occurrence object.  

```python
# Get the value of the property.
propertyValue = occurrence_var.transform2

# Set the value of the property.
occurrence_var.transform2 = propertyValue
```

## Property Value

This is a read/write property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version January 2022  

