# Occurrence.bRepBodies Property

Parent Object: [Occurrence](Occurrence.md)  

## Description

Returns the body proxies for the B-Rep bodies in the component referenced by this occurrence. For example if you get the occurrences from the root component and then use this property to get the bodies from those occurrences, the bodies returned will return information in the context of the root component, not the component they actually exist in.

## Syntax

"occurrence_var" is a variable referencing an Occurrence object.  

```python
# Get the value of the property.
propertyValue = occurrence_var.bRepBodies
```

## Property Value

This is a read only property whose value is a [BRepBodies](BRepBodies.md).

## Version

Introduced in version August 2016  

