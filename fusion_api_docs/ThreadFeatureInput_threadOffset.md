# ThreadFeatureInput.threadOffset Property

Parent Object: [ThreadFeatureInput](ThreadFeatureInput.md)  

## Description

Gets and sets the thread offset. The offset is the distance along the axis of the cylinder from the edge to the start of the thread. It is only used in the case where the isFullLength property is false. Returns nothing in the case where the feature is non-parametric.

## Syntax

"threadFeatureInput_var" is a variable referencing a ThreadFeatureInput object.  

```python
# Get the value of the property.
propertyValue = threadFeatureInput_var.threadOffset

# Set the value of the property.
threadFeatureInput_var.threadOffset = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Version

Introduced in version January 2015  

