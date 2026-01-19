# MoveFeature.redefineAsTranslateAlongEntity Method

Parent Object: [MoveFeature](MoveFeature.md)  

## Description

Redefines the move feature to be a translation along a specified entity.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"moveFeature_var" is a variable referencing a [MoveFeature](MoveFeature.md) object.

```python
returnValue = moveFeature_var.redefineAsTranslateAlongEntity(linearEntity, distance)
```

## Return Value

| Type    | Description                                     |
|---------|-------------------------------------------------|
| boolean | Returns true if the redefinition is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| linearEntity | [Base](Base.md) | A linear entity that defines the direction of the move. This can be a linear BRepEdge, ConstructionAxis, or a SketchLine. The entity defines the direction, not the distance. The natural direction of the entity defines the translation direction. |
| distance | [ValueInput](ValueInput.md) | A ValueInput object that defines the offset distance. If the ValueInput is created using a real value, the distance is in centimeters. If it's defined using a string, the default document units will be used. |

## Version

Introduced in version January 2023  

