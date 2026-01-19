# UnstitchFeature.inputFaces Property

Parent Object: [UnstitchFeature](UnstitchFeature.md)  

## Description

Gets the faces that were input to be unstitched.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"unstitchFeature_var" is a variable referencing a UnstitchFeature object.  

```python
# Get the value of the property.
propertyValue = unstitchFeature_var.inputFaces
```

## Property Value

This is a read only property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version July 2015  

