# BossFeature.assemblyContext Property

Parent Object: [BossFeature](BossFeature.md)  

## Description

Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object.

## Syntax

"bossFeature_var" is a variable referencing a BossFeature object.  

```python
# Get the value of the property.
propertyValue = bossFeature_var.assemblyContext
```

## Property Value

This is a read only property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version October 2022  

