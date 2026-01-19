# Occurrence.appearance Property

Parent Object: [Occurrence](Occurrence.md)  

## Description

Read-write property that gets and sets the appearance override for this occurrence. This property can return null indicating there is no override appearance and that the contents of the occurrence are displayed using there defined appearance. Setting the property to null will remove any override appearance for this occurrence.

## Syntax

"occurrence_var" is a variable referencing an Occurrence object.  

```python
# Get the value of the property.
propertyValue = occurrence_var.appearance

# Set the value of the property.
occurrence_var.appearance = propertyValue
```

## Property Value

This is a read/write property whose value is an [Appearance](Appearance.md).

## Version

Introduced in version August 2014  

