# LoftSection.setDirectionEndCondition Method

Parent Object: [LoftSection](LoftSection.md)  

## Description

Sets the end condition to be defined by a direction and weight.  

This is valid for sections defined with sketch curves.  

If this LoftSection object is associated with a created feature, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"loftSection_var" is a variable referencing a [LoftSection](LoftSection.md) object.

```python
# Uses no optional arguments.
returnValue = loftSection_var.setDirectionEndCondition()

# Uses optional arguments.
returnValue = loftSection_var.setDirectionEndCondition(angle, weight)
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| angle | [ValueInput](ValueInput.md) | Input ValueInput object that specifies the direction by using an angle. This defaults to an angle of 0.0. If the ValueInput object is a string it must be an valid expression that can be evaluated as an angle. If the ValueInput is a value then it is in radians. This is an optional argument whose default value is null. |
| weight | [ValueInput](ValueInput.md) | Input ValueInput object that defines the weight or the amount of influence of end condition on the loft. This defaults to a value of 1.0. If the ValueInput object is a string it must be an valid expression that can be evaluated as a unitless value. In any case, the value must be greater than 0. This is an optional argument whose default value is null. |

## Version

Introduced in version August 2016  

