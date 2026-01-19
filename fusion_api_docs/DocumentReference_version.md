# DocumentReference.version Property

Parent Object: [DocumentReference](DocumentReference.md)  

## Description

Gets and sets the version of the dataFile on A360 that this document currently represents. Setting this property will cause all occurrences referencing this document to update to that version.

## Syntax

"documentReference_var" is a variable referencing a DocumentReference object.  

```python
# Get the value of the property.
propertyValue = documentReference_var.version

# Set the value of the property.
documentReference_var.version = propertyValue
```

## Property Value

This is a read/write property whose value is an integer.

## Version

Introduced in version June 2017  

