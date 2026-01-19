# CircularPatternFeature.isSymmetric Property

Parent Object: [CircularPatternFeature](CircularPatternFeature.md)  

## Description

Gets and sets if the angle extent is in one direction or symmetric.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"circularPatternFeature_var" is a variable referencing a CircularPatternFeature object.  

```python
# Get the value of the property.
propertyValue = circularPatternFeature_var.isSymmetric

# Set the value of the property.
circularPatternFeature_var.isSymmetric = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version November 2014  

