# SweepFeature.orientation Property

Parent Object: [SweepFeature](SweepFeature.md)  

## Description

Gets and sets the sweep orientation. It defaults to PerpendicularOrientationType. This property is ignored if sweeping a solid or a guide rail or surface has been specified.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"sweepFeature_var" is a variable referencing a SweepFeature object.  

```python
# Get the value of the property.
propertyValue = sweepFeature_var.orientation

# Set the value of the property.
sweepFeature_var.orientation = propertyValue
```

## Property Value

This is a read/write property whose value is a [SweepOrientationTypes](SweepOrientationTypes.md).

## Version

Introduced in version November 2014  

