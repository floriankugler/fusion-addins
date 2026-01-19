# SketchArcs.addByCenterStartEnd Method

Parent Object: [SketchArcs](SketchArcs.md)  

## Description

Creates a sketch arc that is centered at the specified point and between the two input points.

## Remarks

Sketch arcs always exist in a counterclockwise direction. Even though you can provide the start and end points that define an arc that will have a clockwise direction, the result will still be a counterclockwise arc. This means if you query the created sketch arc, the start and end points may be opposite of what you expect.

## Syntax

"sketchArcs_var" is a variable referencing a [SketchArcs](SketchArcs.md) object.

```python
# Uses no optional arguments.
returnValue = sketchArcs_var.addByCenterStartEnd(centerPoint, startPoint, endPoint)

# Uses optional arguments.
returnValue = sketchArcs_var.addByCenterStartEnd(centerPoint, startPoint, endPoint, normal)
```

## Return Value

| Type | Description |
|----|----|
| [SketchArc](SketchArc.md) | Returns the newly created SketchArc or null in the case of a failure. |

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| centerPoint | [Base](Base.md) | The center point of the arc. This can be either an existing SketchPoint or a Point3D object. |
| startPoint | [Base](Base.md) | The start point of the arc. This can be either an existing SketchPoint or a Point3D object. |
| endPoint | [Base](Base.md) | The end point of the arc. This can be either an existing SketchPoint or a Point3D object. If the end point does not lie on the arc, a new point would be created such that it lies on the arc. |
| normal | [Vector3D](Vector3D.md) | An optional argument that specifies the normal of the plane the arc will be created on. If not supplied, a vector in the positive Z direction will be used, which results in the creation of an arc that is parallel to the X-Y plane of the sketch. However, you can specify a normal vector to orient the arc in any orientation. The normal also helps to control the sweep direction of the arc, where the sweep direction is always counterclockwise from the start to the end point, where counterclockwise is defined using the right-hand rule around the normal vector. This is an optional argument whose default value is null. |

## Version

Introduced in version January 2024  

