# SweepFeature.solidOrientation Property

Parent Object: [SweepFeature](SweepFeature.md)  

## Description

Gets and sets the sweep solid orientation. It defaults to PerpendicularSolidOrientationType. Setting the solid orientation to AlignedSolidOrientationType requires the solid aligned axis to be set. This property is ignored if sweeping a profile.  

To set this property, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"sweepFeature_var" is a variable referencing a SweepFeature object.  

```python
# Get the value of the property.
propertyValue = sweepFeature_var.solidOrientation

# Set the value of the property.
sweepFeature_var.solidOrientation = propertyValue
```

## Property Value

This is a read/write property whose value is a [SweepSolidOrientationTypes](SweepSolidOrientationTypes.md).

## Version

Introduced in version May 2024  

