# ThreadFeature.threadLength Property

Parent Object: [ThreadFeature](ThreadFeature.md)  

## Description

Gets the parameter that controls the depth of the thread. Even though the parameter for the thread depth is always created and accessible through this property, it is only used in the case where the isFullLength property is false. Returns nothing in the case where the feature is non-parametric.

## Syntax

"threadFeature_var" is a variable referencing a ThreadFeature object.  

```python
# Get the value of the property.
propertyValue = threadFeature_var.threadLength
```

## Property Value

This is a read only property whose value is a [ModelParameter](ModelParameter.md).

## Version

Introduced in version January 2015  

