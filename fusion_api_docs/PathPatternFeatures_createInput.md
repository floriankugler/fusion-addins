# PathPatternFeatures.createInput Method

Parent Object: [PathPatternFeatures](PathPatternFeatures.md)  

## Description

Creates a PathPatternFeatureInput object. Use properties and methods on this object to define the path pattern you want to create and then use the Add method, passing in the PathPatternFeatureInput object.

## Syntax

"pathPatternFeatures_var" is a variable referencing a [PathPatternFeatures](PathPatternFeatures.md) object.

```python
returnValue = pathPatternFeatures_var.createInput(inputEntities, path, quantity, distance, patternDistanceType)
```

## Return Value

| Type | Description |
|----|----|
| [PathPatternFeatureInput](PathPatternFeatureInput.md) | Returns the newly created PathPatternFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| inputEntities | [ObjectCollection](ObjectCollection.md) | The collection can contain faces, features, bodies or occurrences. All of the entities must be of a single type. For example, it can't contain features and occurrences but only features or occurrences. |
| path | [Path](Path.md) | The Path object that represents a single set of connected curves along which to drive the pattern. |
| quantity | [ValueInput](ValueInput.md) | Specifies the number of instances in the first direction. |
| distance | [ValueInput](ValueInput.md) | Specifies the distance. How this value is used depends on the value of the PatternDistanceType property. A negative value can be used to change the direction. If the value is ExtentPatternDistanceType then it defines the total distance of the pattern. If the value is SpacingPatternDistanceType then it defines the distance between each element. |
| patternDistanceType | [PatternDistanceType](PatternDistanceType.md) | Specifies how the distance between elements is computed. |

## Samples

| Name | Description |
|----|----|
| [pathPatternFeatures.add](pathPatternFeatures_add_Sample.md) | Demonstrates the pathPatternFeatures.add method using a selected body and sketch curve as the path. |

## Version

Introduced in version November 2014  

