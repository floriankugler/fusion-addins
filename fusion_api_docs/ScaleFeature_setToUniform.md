# ScaleFeature.setToUniform Method

Parent Object: [ScaleFeature](ScaleFeature.md)  

## Description

Calling this method will change to a uniform scale. The isUniform is set to true if successful.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"scaleFeature_var" is a variable referencing a [ScaleFeature](ScaleFeature.md) object.

```python
returnValue = scaleFeature_var.setToUniform(scaleFactor)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| scaleFactor | [ValueInput](ValueInput.md) | A ValueInput object that defines the scale factor. |

## Version

Introduced in version January 2015  

