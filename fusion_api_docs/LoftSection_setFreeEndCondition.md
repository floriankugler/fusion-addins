# LoftSection.setFreeEndCondition Method

Parent Object: [LoftSection](LoftSection.md)  

## Description

Sets the end condition to be a "Free" end condition. This is the default end condition when a new section is added.  

This is valid for sections defined with all curve types.  

If this LoftSection object is associated with a created feature, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"loftSection_var" is a variable referencing a [LoftSection](LoftSection.md) object.

```python
returnValue = loftSection_var.setFreeEndCondition()
```

## Return Value

| Type    | Description                                   |
|---------|-----------------------------------------------|
| boolean | Returns true if the operation was successful. |

## Version

Introduced in version August 2016  

