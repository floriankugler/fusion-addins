# RectangularPatternFeature.isSymmetricInDirectionTwo Property

Parent Object: [RectangularPatternFeature](RectangularPatternFeature.md)  

## Description

Gets and sets if the pattern in direction two is in one direction or symmetric.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"rectangularPatternFeature_var" is a variable referencing a RectangularPatternFeature object.  

```python
# Get the value of the property.
propertyValue = rectangularPatternFeature_var.isSymmetricInDirectionTwo

# Set the value of the property.
rectangularPatternFeature_var.isSymmetricInDirectionTwo = propertyValue
```

## Property Value

This is a read/write property whose value is a boolean.

## Version

Introduced in version January 2015  

