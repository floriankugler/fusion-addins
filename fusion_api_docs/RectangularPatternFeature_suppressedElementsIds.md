# RectangularPatternFeature.suppressedElementsIds Property

Parent Object: [RectangularPatternFeature](RectangularPatternFeature.md)  

## Description

Gets and sets the ids of the patterns to suppress.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"rectangularPatternFeature_var" is a variable referencing a RectangularPatternFeature object.  

```python
# Get the value of the property.
propertyValue = rectangularPatternFeature_var.suppressedElementsIds

# Set the value of the property.
rectangularPatternFeature_var.suppressedElementsIds = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type uinteger.

## Version

Introduced in version November 2014  

