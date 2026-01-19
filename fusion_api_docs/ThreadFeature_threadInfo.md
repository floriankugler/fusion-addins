# ThreadFeature.threadInfo Property

Parent Object: [ThreadFeature](ThreadFeature.md)  

## Description

Gets and sets the thread data. Also can edit the thread through the properties and methods on the ThreadInfo object.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"threadFeature_var" is a variable referencing a ThreadFeature object.  

```python
# Get the value of the property.
propertyValue = threadFeature_var.threadInfo

# Set the value of the property.
threadFeature_var.threadInfo = propertyValue
```

## Property Value

This is a read/write property whose value is a [ThreadInfo](ThreadInfo.md).

## Version

Introduced in version January 2015  

