# ConstructionPlane.deriveFeature Property

Parent Object: [ConstructionPlane](ConstructionPlane.md)  

## Description

Returns the DeriveFeature if this construction plane is derived from another design. This property returns null if the construction plane is not derived from another design (i.e. isDerived property returns false).

## Syntax

"constructionPlane_var" is a variable referencing a ConstructionPlane object.  

```python
# Get the value of the property.
propertyValue = constructionPlane_var.deriveFeature
```

## Property Value

This is a read only property whose value is a [DeriveFeature](DeriveFeature.md).

## Version

Introduced in version January 2026  

