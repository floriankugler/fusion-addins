# MeasureManager.measureAngle Method

Parent Object: [MeasureManager](MeasureManager.md)  

## Description

Measures the angle between the input geometry.

## Syntax

"measureManager_var" is a variable referencing a [MeasureManager](MeasureManager.md) object.

```python
# Uses no optional arguments.
returnValue = measureManager_var.measureAngle(geometryOne, geometryTwo)

# Uses optional arguments.
returnValue = measureManager_var.measureAngle(geometryOne, geometryTwo, geometryThree)
```

## Return Value

| Type | Description |
|----|----|
| [MeasureResults](MeasureResults.md) | A MeasureResults object that contains the angle and the two points on the geometry that the angle that was measured between them in radians. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| geometryOne | [Base](Base.md) | The first geometry to measure the angle to. This can be any 3D point geometry (Construction Point, Vertex, SketchPoint, or Point3D), any 3D linear geometry (Construction Axis, linear BRepEdge, SketchLine, Line3D, or InfiniteLine3D), or any planar geometry (Construction Plane, planar BRepFace, or Plane). |
| geometryTwo | [Base](Base.md) | The second geometry to measure the angle to. This can be any 3D point geometry (Construction Point, Vertex, SketchPoint, or Point3D), any 3D linear geometry (Construction Axis, linear BRepEdge, SketchLine, Line3D, or InfiniteLine3D), or any planar geometry (Construction Plane, planar BRepFace, or Plane). |
| geometryThree | [Base](Base.md) | The optional third geometry to measure the angle to. This is only used when the first two geometries are points and this defines the third point. When three points define a triangle, the apex of the triangle is defined by the second point. A point can be defined by a Construction Point, Vertex, SketchPoint, or Point3D object. This is an optional argument whose default value is null. |

## Samples

| Name                                       | Description               |
|--------------------------------------------|---------------------------|
| [Measure Sample](MeasureSample_Sample.md) | Measure related functions |

## Version

Introduced in version December 2017  

