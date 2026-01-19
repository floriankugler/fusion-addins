# MoveFeature.redefineAsTranslateXYZ Method

Parent Object: [MoveFeature](MoveFeature.md)  

## Description

Redefines the move feature to be described by a translation in X, Y, and Z.  

To use this method, you need to position the timeline marker to immediately before this feature. This can be accomplished using the following code: thisFeature.timelineObject.rollTo(True)

## Syntax

"moveFeature_var" is a variable referencing a [MoveFeature](MoveFeature.md) object.

```python
returnValue = moveFeature_var.redefineAsTranslateXYZ(xDistance, yDistance, zDistance, isDesignSpace)
```

## Return Value

| Type    | Description                                      |
|---------|--------------------------------------------------|
| boolean | Returns true if the re-definition is successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| xDistance | [ValueInput](ValueInput.md) | A ValueInput object that defines the offset in the X direction. If the ValueInput is created using a real value, the distance is in centimeters. If it's defined using a string, the default document units will be used. |
| yDistance | [ValueInput](ValueInput.md) | A ValueInput object that defines the offset in the Y direction. If the ValueInput is created using a real value, the distance is in centimeters. If it's defined using a string, the default document units will be used. |
| zDistance | [ValueInput](ValueInput.md) | A ValueInput object that defines the offset in the Z direction. If the ValueInput is created using a real value, the distance is in centimeters. If it's defined using a string, the default document units will be used. |
| isDesignSpace | boolean | Defines if the translation is defined with respect to the design or component space. Design space is the same as the root component space. |

## Version

Introduced in version January 2023  

