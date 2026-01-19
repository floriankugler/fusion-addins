# Decal.deriveFeature Property

Parent Object: [Decal](Decal.md)  

## Description

Returns the DeriveFeature if this decal is derived from another design. This property returns null if the decal is not derived from another design (i.e. isDerived property returns false).

## Syntax

"decal_var" is a variable referencing a Decal object.  

```python
# Get the value of the property.
propertyValue = decal_var.deriveFeature
```

## Property Value

This is a read only property whose value is a [DeriveFeature](DeriveFeature.md).

## Version

Introduced in version January 2026  

