# CombineFeature.isKeepToolBodies Property

Parent Object: [CombineFeature](CombineFeature.md)  

## Description

Gets and sets a boolean value for whether or not the tool bodies are retrained after the combine results.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"combineFeature_var" is a variable referencing a CombineFeature object.  

```python
# Get the value of the property.
propertyValue = combineFeature_var.isKeepToolBodies

# Set the value of the property.
combineFeature_var.isKeepToolBodies = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2014  

