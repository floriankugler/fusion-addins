# ThreadFeature.hole Property

Parent Object: [ThreadFeature](ThreadFeature.md)  

## Description

If this thread feature is was created as the result of creating a tapped hole, this property will return the associated hole feature. If this is a standard thread feature, this property will return null.

## Syntax

"threadFeature_var" is a variable referencing a ThreadFeature object.  

```python
# Get the value of the property.
propertyValue = threadFeature_var.hole
```

## Property Value

This is a read only property whose value is a [HoleFeature](HoleFeature.md).

## Version

Introduced in version September 2025  

