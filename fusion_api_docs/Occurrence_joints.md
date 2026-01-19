# Occurrence.joints Property

Parent Object: [Occurrence](Occurrence.md)  

## Description

Returns the joints that affect the position of this occurrence. For example, if a joint has been created between this occurrence and another occurrence, this property will return that joint. If the occurrence is a proxy, the joints returned will also be proxies in the same context as the occurrence.

## Syntax

"occurrence_var" is a variable referencing an Occurrence object.  

```python
# Get the value of the property.
propertyValue = occurrence_var.joints
```

## Property Value

This is a read only property whose value is a [JointList](JointList.md).

## Version

Introduced in version January 2016  

