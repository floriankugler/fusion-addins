# MoveFeatureInput.defineAsPointToPoint Method

Parent Object: [MoveFeatureInput](MoveFeatureInput.md)  

## Description

This method defines a move feature described by a translation from one point to another.

## Syntax

"moveFeatureInput_var" is a variable referencing a [MoveFeatureInput](MoveFeatureInput.md) object.

```python
returnValue = moveFeatureInput_var.defineAsPointToPoint(originPoint, targetPoint)
```

## Return Value

| Type    | Description                                              |
|---------|----------------------------------------------------------|
| boolean | Returns true if defining the type of move is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| originPoint | [Base](Base.md) | The first point that defines the start position of the move. |
| targetPoint | [Base](Base.md) | The second point that defines the direction and distance of the move. |

## Version

Introduced in version January 2023  

