# CircularPatternFeatures.add Method

Parent Object: [CircularPatternFeatures](CircularPatternFeatures.md)  

## Description

Creates a new circular pattern feature.

## Syntax

"circularPatternFeatures_var" is a variable referencing a [CircularPatternFeatures](CircularPatternFeatures.md) object.

```python
returnValue = circularPatternFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [CircularPatternFeature](CircularPatternFeature.md) | Returns the newly created CircularPatternFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [CircularPatternFeatureInput](CircularPatternFeatureInput.md) | A CircularPatternFeatureInput object that defines the desired circular pattern. Use the createInput method to create a new CircularPatternFeatureInput object and then use methods on it (the CircularPatternFeatureInput object) to define the circular pattern. |

## Samples

| Name | Description |
|----|----|
| [circularPatternFeatures.add](circularPatternFeatures_add_Sample.md) | Demonstrates the circularPatternFeatures.add method. To use the sample have a design open that contains at least one body. When you run the script, it will prompt you to select a body, which will be patterned around the base Y-axis. |
| [CircularPattern Feature API Sample](CircularPatternFeatureSample_Sample.md) | Demonstrates creating a new circular pattern feature. |

## Version

Introduced in version November 2014  

