# Sketch.setConstructionState Method

Parent Object: [Sketch](Sketch.md)  

## Description

Method that sets the Construction state for an array of sketch curves.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
returnValue = sketch_var.setConstructionState(sketchCurves, constructionState)
```

## Return Value

| Type    | Description                 |
|---------|-----------------------------|
| boolean | Returns true if successful. |

## Parameters

| Name | Type | Description |
|----|----|----|
| sketchCurves | SketchCurve\[\] | An array of sketch curves to set the construction status. |
| constructionState | [SketchCurveConstructionStates](SketchCurveConstructionStates.md) | Input enum value that specifies if the construction state of the input curves should be toggled, set to construction, or set to normal. |

## Version

Introduced in version March 2024  

