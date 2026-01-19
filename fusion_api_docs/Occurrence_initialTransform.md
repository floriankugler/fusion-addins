# Occurrence.initialTransform Property

Parent Object: [Occurrence](Occurrence.md)  

## Description

Gets and sets the initial position of the occurrence. Setting the initial transform is not valid for all occurrences. For instance, this operation could fail if the occurrence is created by a pattern among other cases. To determine if setting the initial transform is possible, use the isValidForEditInitialPosition property. If this property returns false, attempting to set the initial transform will result in failure.

## Syntax

"occurrence_var" is a variable referencing an Occurrence object.  

```python
# Get the value of the property.
propertyValue = occurrence_var.initialTransform

# Set the value of the property.
occurrence_var.initialTransform = propertyValue
```

## Property Value

This is a read/write property whose value is a [Matrix3D](Matrix3D.md).

## Version

Introduced in version November 2024  

