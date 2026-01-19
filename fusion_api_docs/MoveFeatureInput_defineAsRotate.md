# MoveFeatureInput.defineAsRotate Method

Parent Object: [MoveFeatureInput](MoveFeatureInput.md)  

## Description

This method defines a move feature that is described by an axis and rotation angle.

## Syntax

"moveFeatureInput_var" is a variable referencing a [MoveFeatureInput](MoveFeatureInput.md) object.

```python
returnValue = moveFeatureInput_var.defineAsRotate(axisEntity, angle)
```

## Return Value

| Type    | Description                                              |
|---------|----------------------------------------------------------|
| boolean | Returns true if defining the type of move is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| axisEntity | [Base](Base.md) | A linear entity that defines the axis of rotation. This can be a linear BRepEdge, ConstructionAxis, or a SketchLine. The natural direction of the entity defines a right-hand rule for the rotation direction. |
| angle | [ValueInput](ValueInput.md) | A ValueInput object that defines the rotation angle. If the ValueInput is created using a real value, the angle is in radians. If it's defined using a string, the default document units will be used. |

## Version

Introduced in version January 2023  

