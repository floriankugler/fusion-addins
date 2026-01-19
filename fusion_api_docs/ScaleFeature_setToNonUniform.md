# ScaleFeature.setToNonUniform Method

Parent Object: [ScaleFeature](ScaleFeature.md)  

## Description

Calling this method will change to a non-uniform scale. Fails of the inputEntities collection contains sketches or components. The isUniform is set to false if successful.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"scaleFeature_var" is a variable referencing a [ScaleFeature](ScaleFeature.md) object.

```python
returnValue = scaleFeature_var.setToNonUniform(xScale, yScale, zScale)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| xScale | [ValueInput](ValueInput.md) | A ValueInput object that defines the scale in the X direction. |
| yScale | [ValueInput](ValueInput.md) | A ValueInput object that defines the scale in the Y direction. |
| zScale | [ValueInput](ValueInput.md) | A ValueInput object that defines the scale in the Z direction. |

## Version

Introduced in version January 2015  

