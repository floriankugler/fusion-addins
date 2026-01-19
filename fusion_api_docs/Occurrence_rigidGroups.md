# Occurrence.rigidGroups Property

Parent Object: [Occurrence](Occurrence.md)  

## Description

Returns the rigid groups that this occurrence is a member of. If the occurrence is a proxy, the joints returned will also be proxies in the same context as the occurrence.

## Syntax

"occurrence_var" is a variable referencing an Occurrence object.  

```python
# Get the value of the property.
propertyValue = occurrence_var.rigidGroups
```

## Property Value

This is a read only property whose value is a [RigidGroupList](RigidGroupList.md).

## Version

Introduced in version January 2016  

