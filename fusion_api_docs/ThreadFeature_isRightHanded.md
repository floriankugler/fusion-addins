# ThreadFeature.isRightHanded Property

Parent Object: [ThreadFeature](ThreadFeature.md)  

## Description

Gets and sets if the thread is right or left-handed thread. A value of true indicates a right-handed thread. It defaults to true.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"threadFeature_var" is a variable referencing a ThreadFeature object.  

```python
# Get the value of the property.
propertyValue = threadFeature_var.isRightHanded

# Set the value of the property.
threadFeature_var.isRightHanded = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2015  

