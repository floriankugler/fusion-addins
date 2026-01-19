# ThickenFeature.thickenType Property

Parent Object: [ThickenFeature](ThickenFeature.md)  

## Description

Gets and sets the thicken type for the thicken.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"thickenFeature_var" is a variable referencing a ThickenFeature object.  

```python
# Get the value of the property.
propertyValue = thickenFeature_var.thickenType

# Set the value of the property.
thickenFeature_var.thickenType = propertyValue
```

## Property Value

This is a read/write property whose value is a [ThickenTypes](ThickenTypes.md).

## Version

Introduced in version September 2025  

