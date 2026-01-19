# Component.allTangentRelationships Property

Parent Object: [Component](Component.md)  

## Description

Returns all tangent relationships in this component and any sub components. The tangent relationships returned are all in the context of this component so any tangent relationships in sub components will be proxies. This is primarily useful when used from the root component because Fusion flattens the assembly structure, including tangent relationships, when manipulating an assembly.

## Syntax

"component_var" is a variable referencing a Component object.  

```python
# Get the value of the property.
propertyValue = component_var.allTangentRelationships
```

## Property Value

This is a read only property whose value is an array of type [TangentRelationship](TangentRelationship.md).

## Version

Introduced in version May 2022  

