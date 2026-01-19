# SweepFeature.guideRail Property

Parent Object: [SweepFeature](SweepFeature.md)  

## Description

Gets and sets the guide rail to create the sweep. This can be set to null to have a path only sweep.  

To use this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"sweepFeature_var" is a variable referencing a SweepFeature object.  

```python
# Get the value of the property.
propertyValue = sweepFeature_var.guideRail

# Set the value of the property.
sweepFeature_var.guideRail = propertyValue
```

## Property Value

This is a read/write property whose value is a [Path](Path.md).

## Version

Introduced in version November 2015  

