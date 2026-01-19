# FlatPattern.getBendInfo Method

Parent Object: [FlatPattern](FlatPattern.md)  

## Description

Returns bend information for the specified bend.

## Syntax

"flatPattern_var" is a variable referencing a [FlatPattern](FlatPattern.md) object.  

```python
(returnValue, isBendUp, bendAngle) = flatPattern_var.getBendInfo(bendEdge)
```

## Return Value

| Type    | Description                                                     |
|---------|-----------------------------------------------------------------|
| boolean | Returns true if the bend information was successfully returned. |

## Parameters

| Name | Type | Description |
|----|----|----|
| bendEdge | [BRepEdge](BRepEdge.md) | The wire BrepEdge that represents a bend line in the model. The edges are obtained from the wire body returned by the bendLinesBody property. |
| isBendUp | boolean | Indicates if the bend is in the natural direction of the bend line or in the opposite direction. Returns true if the bend is in the same direction as the input bend line. |
| bendAngle | double | Returns the bend angle of the bend in radians. |

## Version

Introduced in version October 2022  

