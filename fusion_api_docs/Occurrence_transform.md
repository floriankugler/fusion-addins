# Occurrence.transform Property

Parent Object: [Occurrence](Occurrence.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Gets and sets the 3d matrix data that defines this occurrences orientation and position in its assembly context.

## Remarks

This property has been retired and replaced by the transform2 property. This method remains and has the same behavior as before. It returns incorrect results in some cases but some existing programs may be relying on these bad results so this property remains unchanged. It will be best to use the transform2 property.

## Syntax

"occurrence_var" is a variable referencing an Occurrence object.  

```python
# Get the value of the property.
propertyValue = occurrence_var.transform

# Set the value of the property.
occurrence_var.transform = propertyValue
```

## Property Value

This is a read/write property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version August 2014  
Retired in version July 2025  

