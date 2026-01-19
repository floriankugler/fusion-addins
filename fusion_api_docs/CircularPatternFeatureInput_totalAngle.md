# CircularPatternFeatureInput.totalAngle Property

Parent Object: [CircularPatternFeatureInput](CircularPatternFeatureInput.md)  

## Description

Gets and sets total angle. A negative angle can be used to reverse the direction. An angle of 360 degrees or 2 pi radians will create a full circular pattern.

## Syntax

"circularPatternFeatureInput_var" is a variable referencing a CircularPatternFeatureInput object.  

```python
# Get the value of the property.
propertyValue = circularPatternFeatureInput_var.totalAngle

# Set the value of the property.
circularPatternFeatureInput_var.totalAngle = propertyValue
```

## Property Value

This is a read/write property whose value is a [ValueInput](ValueInput.md).

## Samples

| Name | Description |
|----|----|
| [circularPatternFeatures.add](circularPatternFeatures_add_Sample.md) | Demonstrates the circularPatternFeatures.add method. To use the sample have a design open that contains at least one body. When you run the script, it will prompt you to select a body, which will be patterned around the base Y-axis. |
| [CircularPattern Feature API Sample](CircularPatternFeatureSample_Sample.md) | Demonstrates creating a new circular pattern feature. |

## Version

Introduced in version November 2014  

