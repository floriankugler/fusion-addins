# RevolveFeature.setAngleExtent Method

Parent Object: [RevolveFeature](RevolveFeature.md)  

## Description

Defines the extent of the revolution to be at a defined angle.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"revolveFeature_var" is a variable referencing a [RevolveFeature](RevolveFeature.md) object.

```python
returnValue = revolveFeature_var.setAngleExtent(isSymmetric, angle)
```

## Return Value

| Type    | Description                |
|---------|----------------------------|
| boolean | Returns true if successful |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| isSymmetric | boolean | Boolean that specifies if the extent is symmetric or not. |
| angle | [ValueInput](ValueInput.md) | ValueInput object that defines the angle. This can be a string or a value. If it's a string it is interpreted using the current document units and can include equations. For example all of the following are valid as long as they result in angle units; "45", "45 deg", "a1 / 2". If a value is input it is interpreted as radians. If isSymmetric is false a positive or negative angle can be used to control the direction. If isSymmetric is true, the angle is the extent in one direction so the entire angle of the revolution will be twice the specified angle. Use an angle of 360 deg or 2 pi radians to create a full revolve. |

## Version

Introduced in version August 2014  

