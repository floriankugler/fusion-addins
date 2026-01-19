# Occurrence.deriveFeature Property

Parent Object: [Occurrence](Occurrence.md)  

## Description

Returns the DeriveFeature if this occurrence is derived from another design. This property returns null if the occurrence is not derived from another design (i.e. isDerived property returns false).

## Syntax

"occurrence_var" is a variable referencing an Occurrence object.  

```python
# Get the value of the property.
propertyValue = occurrence_var.deriveFeature
```

## Property Value

This is a read only property whose value is a [DeriveFeature](DeriveFeature.md).

## Version

Introduced in version January 2026  

