# AsBuiltJoint.assemblyContext Property

Parent Object: [AsBuiltJoint](AsBuiltJoint.md)  

## Description

Returns the assembly occurrence (i.e. the occurrence) of this object in an assembly. This is only valid in the case where this is acting as a proxy in an assembly. Returns null in the case where the object is not in the context of an assembly but is already the native object.

## Syntax

"asBuiltJoint_var" is a variable referencing an AsBuiltJoint object.  

```python
# Get the value of the property.
propertyValue = asBuiltJoint_var.assemblyContext
```

## Property Value

This is a read only property whose value is an [Occurrence](Occurrence.md).

## Version

Introduced in version September 2015  

