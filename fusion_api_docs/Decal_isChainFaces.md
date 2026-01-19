# Decal.isChainFaces Property

Parent Object: [Decal](Decal.md)  

## Description

Returns if the decal is limited to a specified set of faces or wraps onto all faces in the body. If this property is True, a single face has been specified and the decal can wrap onto other faces of the body. If False, the decal is limited to the set of specified faces.  

To change this setting, use the redefine method.

## Syntax

"decal_var" is a variable referencing a Decal object.  

```python
# Get the value of the property.
propertyValue = decal_var.isChainFaces
```

## Property Value

This is a read only property whose value is a boolean.

## Version

Introduced in version September 2024  

