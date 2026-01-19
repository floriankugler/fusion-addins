# ConstructionPoint.deriveFeature Property

Parent Object: [ConstructionPoint](ConstructionPoint.md)  

## Description

Returns the DeriveFeature if this construction point is derived from another design. This property returns null if the construction point is not derived from another design (i.e. isDerived property returns false).

## Syntax

"constructionPoint_var" is a variable referencing a ConstructionPoint object.  

```python
# Get the value of the property.
propertyValue = constructionPoint_var.deriveFeature
```

## Property Value

This is a read only property whose value is a [DeriveFeature](DeriveFeature.md).

## Version

Introduced in version January 2026  

