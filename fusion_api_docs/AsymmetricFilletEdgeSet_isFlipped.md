# AsymmetricFilletEdgeSet.isFlipped Property

Parent Object: [AsymmetricFilletEdgeSet](AsymmetricFilletEdgeSet.md)  

## Description

Gets and sets if offsets are reversed. If false, offsetOne is applied to the first direction and offsetTwo to the second direction. Setting to true reverses this.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"asymmetricFilletEdgeSet_var" is a variable referencing an AsymmetricFilletEdgeSet object.  

```python
# Get the value of the property.
propertyValue = asymmetricFilletEdgeSet_var.isFlipped

# Set the value of the property.
asymmetricFilletEdgeSet_var.isFlipped = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2025  

