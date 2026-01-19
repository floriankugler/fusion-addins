# Sketch.offset Method

Parent Object: [Sketch](Sketch.md)  

## Description

This function is retired. See more information in the 'Remarks' section below.  

Creates offset curves for the set of input curves. If the offset distance is not provided, the offset distance is defined by the direction point.

## Remarks

To access the full capabilities supported by offset, you should use the createOffsetInput and addOffset2 methods.

## Syntax

"sketch_var" is a variable referencing a [Sketch](Sketch.md) object.

```python
# Uses no optional arguments.
returnValue = sketch_var.offset(curves, directionPoint)

# Uses optional arguments.
returnValue = sketch_var.offset(curves, directionPoint, offset)
```

## Return Value

| Type | Description |
|----|----|
| [ObjectCollection](ObjectCollection.md) | A collection of the new offset sketch curves created |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| curves | [ObjectCollection](ObjectCollection.md) | A set of end connected curves. The Sketch.FindConnectedCurves method is a convenient way to get this set of curves. |
| directionPoint | [Point3D](Point3D.md) | Defines which side of the input curves to create the offset on |
| offset | double | The distance to offset the curves in centimeters. This is an optional argument whose default value is 0.0. |

## Samples

| Name | Description |
|----|----|
| [Sketch fillet and offset API Sample](SketchFilletAndOffset_Sample.md) | Demonstrates the creation of a fillet in a sketch and offset a set of curves. |

## Version

Introduced in version August 2014  
Retired in version September 2024  

