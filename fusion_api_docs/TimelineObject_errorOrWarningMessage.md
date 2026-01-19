# TimelineObject.errorOrWarningMessage Property

Parent Object: [TimelineObject](TimelineObject.md)  

## Description

Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.

## Syntax

"timelineObject_var" is a variable referencing a TimelineObject object.  

```python
# Get the value of the property.
propertyValue = timelineObject_var.errorOrWarningMessage
```

## Property Value

This is a read only property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [Extrude Feature API Sample](ExtrudeFeatureSample_Sample.md) | Demonstrates creating a new extrude feature. |
| [Ruled Surface Feature API Sample](RuledSurfaceFeatureSample_Sample.md) | Demonstrates creating a new ruled surface feature. |

## Version

Introduced in version July 2016  

