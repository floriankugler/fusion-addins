# CircularPatternFeatures.createInput Method

Parent Object: [CircularPatternFeatures](CircularPatternFeatures.md)  

## Description

Creates a CircularPatternFeatureInput object. Use properties and methods on this object to define the circular pattern you want to create and then use the Add method, passing in the CircularPatternFeatureInput object.

## Syntax

"circularPatternFeatures_var" is a variable referencing a [CircularPatternFeatures](CircularPatternFeatures.md) object.

```python
returnValue = circularPatternFeatures_var.createInput(inputEntities, axis)
```

## Return Value

| Type | Description |
|----|----|
| [CircularPatternFeatureInput](CircularPatternFeatureInput.md) | Returns the newly created CircularPatternFeatureInput object or null if the creation failed. |

## Parameters

| Name | Type | Description |
|----|----|----|
| inputEntities | [ObjectCollection](ObjectCollection.md) | The collection can contain faces, features, bodies or occurrences. All of the entities must be of a single type. For example, it can't contain features and occurrences but only features or occurrences. |
| axis | [Base](Base.md) | Input linear entity or the entity has axis that defines axis of circular pattern. This can be a sketch line, linear edge, construction axis, an edge/sketch curve that defines an axis (circle, etc.) or a face that defines an axis (cylinder, cone, torus, etc.). |

## Samples

| Name | Description |
|----|----|
| [circularPatternFeatures.add](circularPatternFeatures_add_Sample.md) | Demonstrates the circularPatternFeatures.add method. To use the sample have a design open that contains at least one body. When you run the script, it will prompt you to select a body, which will be patterned around the base Y-axis. |
| [CircularPattern Feature API Sample](CircularPatternFeatureSample_Sample.md) | Demonstrates creating a new circular pattern feature. |

## Version

Introduced in version November 2014  

