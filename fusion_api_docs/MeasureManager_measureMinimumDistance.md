# MeasureManager.measureMinimumDistance Method

Parent Object: [MeasureManager](MeasureManager.md)  

## Description

Measures the minimum distance between the two input geometries.

## Syntax

"measureManager_var" is a variable referencing a [MeasureManager](MeasureManager.md) object.

```python
returnValue = measureManager_var.measureMinimumDistance(geometryOne, geometryTwo)
```

## Return Value

| Type | Description |
|----|----|
| [MeasureResults](MeasureResults.md) | A MeasureResults object that contains the distance and the two points on the geometry that the distance that was measured between them in centimeters. |

## Parameters

| Name | Type | Description |
|----|----|----|
| geometryOne | [Base](Base.md) | The first geometry to measure from. This can be an Occurrence, BRepBody, BRepFace, BRepEdge, BRepVertex, ConstructionPlane, ConstructionAxis, ConstructionPoint, and any sketch entity. The only temporary geometry supported is the Plane object. |
| geometryTwo | [Base](Base.md) | The first geometry to measure from. This can be an Occurrence, BRepBody, BRepFace, BRepEdge, BRepVertex, ConstructionPlane, ConstructionAxis, ConstructionPoint, and any sketch entity. The only temporary geometry supported is the Plane object. |

## Samples

| Name                                       | Description               |
|--------------------------------------------|---------------------------|
| [Measure Sample](MeasureSample_Sample.md) | Measure related functions |

## Version

Introduced in version December 2017  

