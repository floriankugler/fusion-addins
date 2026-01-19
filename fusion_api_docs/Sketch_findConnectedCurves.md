# Sketch.findConnectedCurves Method

Parent Object: [Sketch](Sketch.md)  

## Description

Finds the sketch curves that are end connected to the input curve. This can be useful for many cases but is especially useful in gathering the input when creating an offset.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
returnValue = sketch_var.findConnectedCurves(curve)
```

## Return Value

| Type | Description |
|----|----|
| [ObjectCollection](ObjectCollection.md) | A collection of the connected curves. They are returned in their connected order with the original input curve being one of the curves. |

## Parameters

| Name | Type | Description |
|----|----|----|
| curve | [SketchCurve](SketchCurve.md) | The initial sketch curve that will be used to find the connected curves. |

## Samples

| Name | Description |
|----|----|
| [Sketch fillet and offset API Sample](SketchFilletAndOffset_Sample.md) | Demonstrates the creation of a fillet in a sketch and offset a set of curves. |

## Version

Introduced in version August 2014  

