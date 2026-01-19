# FlatPatternComponent.allJoints Property

Parent Object: [FlatPatternComponent](FlatPatternComponent.md)  

## Description

Returns all joints in this component and any sub components. The joints returned are all in the context of this component so any joints in sub components will be proxies. This is primarily useful when used from the root component because Fusion flattens the assembly structure, including joints, when manipulating an assembly.

## Syntax

"flatPatternComponent_var" is a variable referencing a FlatPatternComponent object.  

```python
# Get the value of the property.
propertyValue = flatPatternComponent_var.allJoints
```

## Property Value

This is a read only property whose value is an array of type [Joint](Joint.md).

## Version

Introduced in version October 2022  

