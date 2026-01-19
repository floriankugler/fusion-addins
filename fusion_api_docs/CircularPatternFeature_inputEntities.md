# CircularPatternFeature.inputEntities Property

Parent Object: [CircularPatternFeature](CircularPatternFeature.md)  

## Description

Gets and sets the input entities. The collection can contain faces, features, bodies or occurrences. All of the entities must be of a single type. For example, it can't contain features and occurrences but only features or occurrences.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"circularPatternFeature_var" is a variable referencing a CircularPatternFeature object.  

```python
# Get the value of the property.
propertyValue = circularPatternFeature_var.inputEntities

# Set the value of the property.
circularPatternFeature_var.inputEntities = propertyValue
```

## Property Value

This is a read/write property whose value is an [ObjectCollection](ObjectCollection.md).

## Version

Introduced in version November 2014  

