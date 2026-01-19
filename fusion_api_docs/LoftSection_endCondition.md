# LoftSection.endCondition Property

Parent Object: [LoftSection](LoftSection.md)  

## Description

Returns the current end condition. This is only valid for the first and last section and when the result is not closed. In other cases this will return null. This returns one of the several objects derived from LoftEndCondition and represents the current end condition. You can edit the existing condition using properties on the returned object. You can change the end condition using one of the set methods on the LoftSection object.  

If this LoftSection object is associated with a created feature, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"loftSection_var" is a variable referencing a LoftSection object.  

```python
# Get the value of the property.
propertyValue = loftSection_var.endCondition
```

## Property Value

This is a read only property whose value is a [LoftEndCondition](LoftEndCondition.md).

## Version

Introduced in version August 2016  

