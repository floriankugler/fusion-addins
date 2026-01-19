# Occurrence.asBuiltJoints Property

Parent Object: [Occurrence](Occurrence.md)  

## Description

Returns the as-built joints that affect the position of this occurrence. If the occurrence is a proxy, the as-built joints returned will also be proxies in the same context as the occurrence.

## Syntax

"occurrence_var" is a variable referencing an Occurrence object.  

```python
# Get the value of the property.
propertyValue = occurrence_var.asBuiltJoints
```

## Property Value

This is a read only property whose value is an [AsBuiltJointList](AsBuiltJointList.md).

## Version

Introduced in version January 2016  

