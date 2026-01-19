# Occurrence.documentReference Property

Parent Object: [Occurrence](Occurrence.md)  

## Description

When the component this occurrence references is an external reference (the isReferencedComponent property returns true), this will return the object that represents that reference. Through the DocumentReference object you can modify the version and get other information associated with the reference.  

This property will fail if the occurrence is not referencing an external component.

## Syntax

"occurrence_var" is a variable referencing an Occurrence object.  

```python
# Get the value of the property.
propertyValue = occurrence_var.documentReference
```

## Property Value

This is a read only property whose value is a [DocumentReference](DocumentReference.md).

## Version

Introduced in version November 2022  

