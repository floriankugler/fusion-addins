# ConstructionAxis.deriveFeature Property

Parent Object: [ConstructionAxis](ConstructionAxis.md)  

## Description

Returns the DeriveFeature if this construction axis is derived from another design. This property returns null if the construction axis is not derived from another design (i.e. isDerived property returns false).

## Syntax

"constructionAxis_var" is a variable referencing a ConstructionAxis object.  

```python
# Get the value of the property.
propertyValue = constructionAxis_var.deriveFeature
```

## Property Value

This is a read only property whose value is a [DeriveFeature](DeriveFeature.md).

## Version

Introduced in version January 2026  

