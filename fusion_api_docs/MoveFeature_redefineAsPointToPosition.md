# MoveFeature.redefineAsPointToPosition Method

Parent Object: [MoveFeature](MoveFeature.md)  

## Description

Redefines a move feature to be described by a point and an offset. The distances define offsets in the X, Y, and Z directions in either design or component space. To not move the input entities at all the offset distances should be set to the current location of the point in either design or component space. Adding or subtracting to those values will then move the entities that distance. It's best to experiment with the command interactively to understand the behavior.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"moveFeature_var" is a variable referencing a [MoveFeature](MoveFeature.md) object.

```python
returnValue = moveFeature_var.redefineAsPointToPosition(point, xDistance, yDistance, zDistance, isDesignSpace)
```

## Return Value

| Type    | Description                                     |
|---------|-------------------------------------------------|
| boolean | Returns true if the redefinition is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| point | [Base](Base.md) | An entity that defines a point in space. This can be a sketch point, a construction point, or a BRepVertex. |
| xDistance | [ValueInput](ValueInput.md) | A ValueInput object that defines the offset in the X direction. If the ValueInput is created using a real value, the distance is in centimeters. If it's defined using a string, the default document units will be used. |
| yDistance | [ValueInput](ValueInput.md) | A ValueInput object that defines the offset in the Y direction. If the ValueInput is created using a real value, the distance is in centimeters. If it's defined using a string, the default document units will be used. |
| zDistance | [ValueInput](ValueInput.md) | A ValueInput object that defines the offset in the Z direction. If the ValueInput is created using a real value, the distance is in centimeters. If it's defined using a string, the default document units will be used. |
| isDesignSpace | boolean | Defines if the translation is defined with respect to the design or component space. Design space is the same as the root component space. |

## Version

Introduced in version January 2023  

