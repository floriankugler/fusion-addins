# ThreadFeature.threadOffset Property

Parent Object: [ThreadFeature](ThreadFeature.md)  

## Description

Gets the parameter that controls the offset value of the thread. The offset is the distance along the axis of the cylinder from the edge to the start of the thread, it is only used in the case where the isFullLength property is false. Returns nothing in the case where the feature is non-parametric.

## Syntax

"threadFeature_var" is a variable referencing a ThreadFeature object.  

```python
# Get the value of the property.
propertyValue = threadFeature_var.threadOffset
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version January 2015  

