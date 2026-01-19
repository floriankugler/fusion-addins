# MoveFeature.redefineAsRotate Method

Parent Object: [MoveFeature](MoveFeature.md)  

## Description

Redefines the move feature to be described by an axis and rotation angle.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"moveFeature_var" is a variable referencing a [MoveFeature](MoveFeature.md) object.

```python
returnValue = moveFeature_var.redefineAsRotate(axisEntity, angle)
```

## Return Value

| Type    | Description                                     |
|---------|-------------------------------------------------|
| boolean | Returns true if the redefinition is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| axisEntity | [Base](Base.md) | A linear entity that defines the axis of rotation. This can be a linear BRepEdge, ConstructionAxis, or a SketchLine. The natural direction of the entity defines a right-hand rule for the rotation direction. |
| angle | [ValueInput](ValueInput.md) | A ValueInput object that defines the rotation angle. If the ValueInput is created using a real value, the angle is in radians. If it's defined using a string, the default document units will be used. |

## Version

Introduced in version January 2023  

