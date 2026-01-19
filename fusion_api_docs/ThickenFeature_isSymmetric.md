# ThickenFeature.isSymmetric Property

Parent Object: [ThickenFeature](ThickenFeature.md)  

## Description

Gets and sets whether to add thickness symmetrically or only on one side of the face/s to thicken.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"thickenFeature_var" is a variable referencing a ThickenFeature object.  

```python
# Get the value of the property.
propertyValue = thickenFeature_var.isSymmetric

# Set the value of the property.
thickenFeature_var.isSymmetric = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version June 2015  

