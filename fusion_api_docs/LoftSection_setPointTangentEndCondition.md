# LoftSection.setPointTangentEndCondition Method

Parent Object: [LoftSection](LoftSection.md)  

## Description

Set the end condition to a tangent condition in the case where the section is a point.  

If this LoftSection object is associated with a created feature, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"loftSection_var" is a variable referencing a [LoftSection](LoftSection.md) object.

```python
returnValue = loftSection_var.setPointTangentEndCondition(weight)
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| weight | [ValueInput](ValueInput.md) | Input ValueInput object that defines the weight or the amount of influence of end condition on the loft. This defaults to a value of 1.0. If the ValueInput object is a string it must be an valid expression that can be evaluated as a unitless value. In any case, the value must be greater than 0. |

## Version

Introduced in version August 2016  

