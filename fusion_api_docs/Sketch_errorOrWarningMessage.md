# Sketch.errorOrWarningMessage Property

Parent Object: [Sketch](Sketch.md)  

## Description

Returns the error or warning message in the case where the healthState property returns either WarningFeatureHealthState or ErrorFeatureHealthState. Otherwise this property returns an empty string.

## Syntax

"sketch_var" is a variable referencing a Sketch object.  

```python
# Get the value of the property.
propertyValue = sketch_var.errorOrWarningMessage
```

## Property Value

This is a read only property whose value is a string.

## Samples

| Name | Description |
|----|----|
| [Sketch Point API Sample](SketchPointSample_Sample.md) | Demonstrates creating a new sketch point. |

## Version

Introduced in version July 2016  

