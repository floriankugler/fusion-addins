# PathPatternFeature.suppressedElementsIds Property

Parent Object: [PathPatternFeature](PathPatternFeature.md)  

## Description

Gets and sets the id's of the elements to suppress.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"pathPatternFeature_var" is a variable referencing a PathPatternFeature object.  

```python
# Get the value of the property.
propertyValue = pathPatternFeature_var.suppressedElementsIds

# Set the value of the property.
pathPatternFeature_var.suppressedElementsIds = propertyValue
```

## Property Value

This is a read/write property whose value is an array of type uinteger.

## Version

Introduced in version November 2014  

