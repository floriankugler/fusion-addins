# SplitBodyFeature.splittingTool Property

Parent Object: [SplitBodyFeature](SplitBodyFeature.md)  

## Description

Gets the entity that defines the splitting tool. The splitting tool is a single entity that can be either a solid body, open body, plane, sketch curve or face that partially or fully intersects the bodyToSplit.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"splitBodyFeature_var" is a variable referencing a SplitBodyFeature object.  

```python
# Get the value of the property.
propertyValue = splitBodyFeature_var.splittingTool
```

## Property Value

This is a read only property whose value is a [Base](Base.md).

## Version

Introduced in version June 2015  

