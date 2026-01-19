# LoftSection.setSmoothEndCondition Method

Parent Object: [LoftSection](LoftSection.md)  

## Description

Sets the end condition to be smooth to the adjacent face. If the end profile is not defined by a BRepEdge, then this is ignored because there is no face to be smooth to.  

This is only valid on the first or last section.  

If this LoftSection object is associated with a created feature, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"loftSection_var" is a variable referencing a [LoftSection](LoftSection.md) object.

```python
returnValue = loftSection_var.setSmoothEndCondition(weight)
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

