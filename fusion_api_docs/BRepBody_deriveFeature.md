# BRepBody.deriveFeature Property

Parent Object: [BRepBody](BRepBody.md)  

## Description

Returns the DeriveFeature if this BRepBody is derived from another design. This property returns null if the BRepBody is not derived from another design (i.e. isDerived property returns false).

## Syntax

"bRepBody_var" is a variable referencing a BRepBody object.  

```python
# Get the value of the property.
propertyValue = bRepBody_var.deriveFeature
```

## Property Value

This is a read only property whose value is a [DeriveFeature](DeriveFeature.md).

## Version

Introduced in version January 2026  

