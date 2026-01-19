# FlatPatternComponent.allAsBuiltJoints Property

Parent Object: [FlatPatternComponent](FlatPatternComponent.md)  

## Description

Returns all joint origins in this component and any sub components. The joint origins returned are all in the context of this component so any joint origins in sub components will be proxies. This is primarily useful when used from the root component because Fusion flattens the assembly structure, including joint origins, when manipulating an assembly.

## Syntax

"flatPatternComponent_var" is a variable referencing a FlatPatternComponent object.  

```python
# Get the value of the property.
propertyValue = flatPatternComponent_var.allAsBuiltJoints
```

## Property Value

This is a read only property whose value is an array of type [AsBuiltJoint](AsBuiltJoint.md).

## Version

Introduced in version October 2022  

