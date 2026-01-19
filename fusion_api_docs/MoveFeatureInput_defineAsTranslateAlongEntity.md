# MoveFeatureInput.defineAsTranslateAlongEntity Method

Parent Object: [MoveFeatureInput](MoveFeatureInput.md)  

## Description

This method will define a move feature that defines a translation along a specified entity.

## Syntax

"moveFeatureInput_var" is a variable referencing a [MoveFeatureInput](MoveFeatureInput.md) object.

```python
returnValue = moveFeatureInput_var.defineAsTranslateAlongEntity(linearEntity, distance)
```

## Return Value

| Type    | Description                                              |
|---------|----------------------------------------------------------|
| boolean | Returns true if defining the type of move is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| linearEntity | [Base](Base.md) | A linear entity that defines the direction of the move. This can be a linear BRepEdge, ConstructionAxis, or a SketchLine. The entity defines the direction, not the distance. The natural direction of the entity defines the translation direction. |
| distance | [ValueInput](ValueInput.md) | A ValueInput object that defines the offset distance. If the ValueInput is created using a real value, the distance is in centimeters. If it's defined using a string, the default document units are used. |

## Version

Introduced in version January 2023  

