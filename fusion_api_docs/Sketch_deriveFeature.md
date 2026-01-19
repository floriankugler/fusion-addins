# Sketch.deriveFeature Property

Parent Object: [Sketch](Sketch.md)  

## Description

Returns the DeriveFeature if this sketch is derived from another design. This property returns null if the sketch is not derived from another design (i.e. isDerived property returns false).

## Syntax

"sketch_var" is a variable referencing a Sketch object.  

```python
# Get the value of the property.
propertyValue = sketch_var.deriveFeature
```

## Property Value

This is a read only property whose value is a [DeriveFeature](DeriveFeature.md).

## Version

Introduced in version January 2026  

