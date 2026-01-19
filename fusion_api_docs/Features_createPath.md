# Features.createPath Method

Parent Object: [Features](Features.md)  

## Description

Method that creates a Path used to define the shape of a Sweep feature. A Path is a contiguous set of curves that can be a combination of sketch curves and model edges.

## Syntax

"features_var" is a variable referencing a [Features](Features.md) object.

```python
# Uses no optional arguments.
returnValue = features_var.createPath(curve)

# Uses optional arguments.
returnValue = features_var.createPath(curve, isChain)
```

## Return Value

| Type             | Description                     |
|------------------|---------------------------------|
| [Path](Path.md) | Returns the newly created Path. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| curve | [Base](Base.md) | A SketchCurve or an ObjectCollection containing multiple sketch entities and/or BRepEdge objects. If a single sketch curve or edge is input the isChain argument is checked to determine if connected curves (they do not need to be tangent) should be automatically found. If multiple curves are provided the isChain argument is always treated as false so you must provide all of the curves in the object collection that you want included in the path. The provided curves must all connect together in a single path. The input curves can be from multiple sketches and bodies and they need to geometrically connect for a valid path to be created. |
| isChain | boolean | Optional argument, that defaults to true. If this argument is set to true, all curves and edges that are end point connected to the single input curve will be found and used to create the path. This argument is only used when the first argument is a single SketchCurve/BRepEdge object. This is an optional argument whose default value is True. |

## Samples

| Name | Description |
|----|----|
| [Sweep with guide rail Feature API Sample](SweepWithGuideRailFeatureSample_Sample.md) | Demonstrates creating a new Sweep feature that uses a guide rail along with a profile. |

## Version

Introduced in version November 2014  

