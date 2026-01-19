# RevolveFeature.setTwoSideAngleExtent Method

Parent Object: [RevolveFeature](RevolveFeature.md)  

## Description

Changes the extent of the revolve to be defined as a two sided angle extent.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"revolveFeature_var" is a variable referencing a [RevolveFeature](RevolveFeature.md) object.

```python
returnValue = revolveFeature_var.setTwoSideAngleExtent(angleOne, angleTwo)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
|----|----|----|
| angleOne | [ValueInput](ValueInput.md) | ValueInput object that defines the first angle. This can be a string or a value. If it's a string it is interpreted using the current document units and can include equations. For example all of the following are valid as long as they result in angle units; "45", "45 deg", "a1 / 2". If a value is input it is interpreted as radians. |
| angleTwo | [ValueInput](ValueInput.md) | ValueInput object that defines the second angle. This can be a string or a value. If it's a string it is interpreted using the current document units and can include equations. For example all of the following are valid as long as they result in angle units; "45", "45 deg", "a1 / 2". If a value is input it is interpreted as radians. |

## Version

Introduced in version August 2014  

