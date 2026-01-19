# ThickenFeature.inputFaces Property

Parent Object: [ThickenFeature](ThickenFeature.md)  

## Description

Gets and sets the ObjectCollection containing the face and/or patch bodies to thicken.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"thickenFeature_var" is a variable referencing a ThickenFeature object.  

```python
# Get the value of the property.
propertyValue = thickenFeature_var.inputFaces

# Set the value of the property.
thickenFeature_var.inputFaces = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version June 2015  

