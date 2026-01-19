# CircularPatternFeature.suppressedElementsIds Property

Parent Object: [CircularPatternFeature](CircularPatternFeature.md)  

## Description

Gets and sets the id's of the elements to suppress.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"circularPatternFeature_var" is a variable referencing a CircularPatternFeature object.  

```python
# Get the value of the property.
propertyValue = circularPatternFeature_var.suppressedElementsIds

# Set the value of the property.
circularPatternFeature_var.suppressedElementsIds = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type uinteger.

## Version

Introduced in version November 2014  

