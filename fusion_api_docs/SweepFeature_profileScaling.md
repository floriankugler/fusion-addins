# SweepFeature.profileScaling Property

Parent Object: [SweepFeature](SweepFeature.md)  

## Description

Gets and sets the sweep profile scaling option. It defaults to SweepProfileScaleOption. This property is only used when a guide rail has been specified.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"sweepFeature_var" is a variable referencing a SweepFeature object.  

```python
# Get the value of the property.
propertyValue = sweepFeature_var.profileScaling

# Set the value of the property.
sweepFeature_var.profileScaling = propertyValue
```

## Property Value

This is a read/write property whose value is a [SweepProfileScalingOptions](SweepProfileScalingOptions.md).

## Version

Introduced in version November 2015  

