# PathPatternFeatures.add Method

Parent Object: [PathPatternFeatures](PathPatternFeatures.md)  

## Description

Creates a new path pattern feature.

## Syntax

"pathPatternFeatures_var" is a variable referencing a [PathPatternFeatures](PathPatternFeatures.md) object.

```python
returnValue = pathPatternFeatures_var.add(input)
```

## Return Value

| Type | Description |
|----|----|
| [PathPatternFeature](PathPatternFeature.md) | Returns the newly created PathPatternFeature object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| input | [PathPatternFeatureInput](PathPatternFeatureInput.md) | A PathPatternFeatureInput object that defines the desired path pattern. Use the createInput method to create a new PathPatternFeatureInput object and then use methods on it (the PathPatternFeatureInput object) to define the path pattern. |

## Samples

| Name | Description |
|----|----|
| [pathPatternFeatures.add](pathPatternFeatures_add_Sample.md) | Demonstrates the pathPatternFeatures.add method using a selected body and sketch curve as the path. |

## Version

Introduced in version November 2014  

